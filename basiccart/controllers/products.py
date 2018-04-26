from flask import g, Blueprint

from basiccart import database as db
from basiccart.utils import to_json, from_json

bp = Blueprint('products', __name__, url_prefix='/products')


@bp.route('/<int:product_id>')
def get_product(product_id):
    product = (
        g.session.query(db.Product)
        .filter(db.Product.id==int(product_id))
        .first()
    )
    if not product:
        raise ValueError('There is no product with id "{}".'.format(product_id))
    return to_json(dict(id=product.id, name=product.name))


@bp.route('/')
def get_products():
    products = g.session.query(db.Product).all()
    products = [dict(id=p.id, name=p.name) for p in products]
    return to_json(dict(products=products))
