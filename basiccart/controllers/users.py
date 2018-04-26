from flask import g, Blueprint

from basiccart import database as db
from basiccart.utils import to_json, from_json

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/')
def get_user():
    user = (
        g.session.query(db.User)
        .filter_by(id=g.user.id)
        .first()
    )
    return to_json(dict(id=user.id, name=user.name))


@bp.route('/', methods=['PUT'])
def set_user():
    user_id = g.params.get('id')
    user = (
        g.session.query(db.User)
        .filter_by(id=int(user_id))
        .first()
    )
    if not user:
        raise ValueError('There is no user with id "{}".'.format(user_id))
    g.user.id = user.id
    return to_json(dict(id=user.id, name=user.name))
