from flask import g, Blueprint

from basiccart import database as db
from basiccart.utils import to_json, from_json

import collections

bp = Blueprint('orders', __name__, url_prefix='/orders')


@bp.route('/<int:order_id>')
def get_order(order_id):
    '''
        get order with supplied order_id if current user has access to it.
    '''
    order = (
        g.session.query(db.OrderProduct.product_id.label("product_id"), db.Product.name.label("name"))
        .select_from(db.OrderProduct)
        .join(db.Product)
        .join(db.Order)
        .filter(db.Order.id==int(order_id))
        .filter(db.Order.user_id == g.user.id).all()
    )
   
    if not order:
        raise ValueError('There is no order with id "{}" or you are not authorized to view that order'.format(order_id))
    order_products = [dict(id=o.product_id, name=o.name) for o in order]
    return to_json(dict(id=order_id, products=order_products))


@bp.route('/')
def get_orders():
    '''
        get all orders regardless of current user.
    '''
    orders = (
        g.session.query(db.OrderProduct.order_id.label("order_id"), db.OrderProduct.product_id.label("product_id"), db.Product.name.label("name"))
        .select_from(db.OrderProduct)
        .join(db.Product)
        .order_by(db.OrderProduct.order_id).all()
    )


    #prepare payload
    p_dict = collections.defaultdict(list)
    for o in orders:
        p_dict[o.order_id].append(dict(id=o.product_id, name=o.name))
    p_list = [dict(id=key, products=value) for key, value in p_dict.items()]
    return to_json(dict(orders=p_list))
