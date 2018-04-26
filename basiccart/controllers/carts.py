from flask import g, Blueprint

from basiccart import database as db
from basiccart.utils import to_json, from_json

bp = Blueprint('cart', __name__, url_prefix='/cart')


@bp.route('/')
def get_cart():
    '''
        returns cart of current user.
    '''
    cart_id = find_cart_id()
    cart = (
        g.session.query(db.CartProduct.product_id.label("product_id"), db.Product.name.label("name"))
        .select_from(db.CartProduct)
        .join(db.Product)
        .filter(db.CartProduct.cart_id == cart_id)
    )

    cart_products = [dict(id=c.product_id, name=c.name) for c in cart]
    return to_json(dict(id=cart_id, products=cart_products))


def find_cart_id():
    '''
        helper function for finding cart_id of current user. creates one if none exists.
    '''
    cart = g.session.query(db.Cart) \
                .filter(db.Cart.user_id == g.user.id) \
                .first()
    if not cart:
        cart = db.Cart(user_id=g.user.id)
        g.session.add(cart)
        g.session.flush()
    
    return cart.id


def add_get_products_to_cart(cart_id):
    '''
        helper function for adding products to association table - CartProduct - with id=cart_id.
    '''
    for p in g.params.get('products'):
        p_id = p.get('id', None)
        if not p_id:
            raise ValueError('There is no id supplied')

        product = (
                g.session.query(db.Product)
                .filter_by(id=int(p_id))
                .first()
        )
        if not product:
            raise ValueError('There is no id supplied or there is no product with id "{}"'.format(p_id))
        
        cp = db.CartProduct(cart_id=cart_id, product_id=int(p_id))
        g.session.add(cp)

    g.session.flush()

    cart = (
        g.session.query(db.CartProduct.product_id.label("product_id"), db.Product.name.label("name"))
        .select_from(db.CartProduct)
        .join(db.Product)
        .filter(db.CartProduct.cart_id == cart_id)
    )

    cart_products = [dict(id=c.product_id, name=c.name) for c in cart]
    return cart_products



@bp.route('/', methods=['PUT'])
def add_to_cart():
    '''
        add new products to cart for current user. allows duplicate entries.
    '''
    cart_id = find_cart_id()
    cart_products = add_get_products_to_cart(cart_id)
    return to_json(dict(id=cart_id, products=cart_products))



@bp.route('/', methods=['POST'])
def reset_cart():
    '''
        resets cart with new set of products for current user..
    '''
    cart_id = find_cart_id()

    #delete existing entries in cart
    g.session.query(db.CartProduct) \
        .filter(db.CartProduct.cart_id == cart_id) \
        .delete(synchronize_session=False)

    cart_products = add_get_products_to_cart(cart_id)
    return to_json(dict(id=cart_id, products=cart_products))


@bp.route('/', methods=['DELETE'])
def delete_cart():
    '''
        Deletes cart of current user. Remove cart from carts table.
    '''
    cart_id = find_cart_id()
    
    #delete children in CartProduct first
    g.session.query(db.CartProduct) \
            .filter(db.CartProduct.cart_id == cart_id) \
            .delete(synchronize_session=False)
    #delete cart 
    g.session.query(db.Cart) \
            .filter(db.Cart.id == cart_id) \
            .delete(synchronize_session=False)
    g.session.flush()
    return '<no payload>'





@bp.route('/order', methods=['POST'])
def order():
    '''
        Convert cart of current user to an order.
    '''
    cart_id = find_cart_id()

    #get cart entries
    cart_products = g.session.query(db.CartProduct) \
                .filter(db.CartProduct.cart_id == cart_id) \
                .all()

    #if cart is empty raise error
    if not cart_products:
        raise ValueError("Cannot convert empty cart to an order.")

    #create a new order
    order = db.Order(user_id=g.user.id)
    g.session.add(order)
    g.session.flush()
    order_id = order.id

    #copy cart to order
    for cp in cart_products:
        op = db.OrderProduct(order_id=order_id, product_id=cp.product_id)
        g.session.add(op)
    
    #empty cart of current user
    g.session.query(db.CartProduct) \
            .filter(db.CartProduct.cart_id == cart_id) \
            .delete(synchronize_session=False)

    #commit and return payload
    g.session.flush()    
    order = (
        g.session.query(db.OrderProduct.product_id.label("product_id"), db.Product.name.label("name"))
        .select_from(db.OrderProduct)
        .join(db.Product)
        .filter(db.OrderProduct.order_id == order_id)
    )
    order_products = [dict(id=o.product_id, name=o.name) for o in order]
    return to_json(dict(id=order_id, products=order_products))
