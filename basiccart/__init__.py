from flask import Flask, g, request

import basiccart.database as db
from basiccart.utils import from_json, to_json


def create_app(name=None, Session=None):
    app = Flask(name or __name__)

    if Session is None:
        engine = db.create_engine()
        Session = db.create_session(engine)

    configure_app(app, Session)
    return app


def configure_app(app, Session):
    session = Session()
    current_user = CurrentUser(session)

    @app.before_request
    def before_request():
        g.session = session
        g.user = current_user

        g.params = {}
        if request.method in ('POST', 'PUT', 'PATCH'):
            content_type = request.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                g.params = from_json(request.data)

    @app.after_request
    def after_request(response):
        response.headers['Content-Type'] = 'application/json'
        return response

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.commit()
        session.close()

    @app.errorhandler(Exception)
    def handle_exception(error):
        return to_json(dict(message=str(error))), 500

    # use the following to simply ignore trailing slash.
    app.url_map.strict_slashes = False

    configure_blueprints(app)


def configure_blueprints(app):
    from basiccart.controllers import users
    app.register_blueprint(users.bp)

    from basiccart.controllers import products
    app.register_blueprint(products.bp)

    from basiccart.controllers import orders
    app.register_blueprint(orders.bp)

    from basiccart.controllers import carts
    app.register_blueprint(carts.bp)


class CurrentUser(object):

    def __init__(self, session):
        query = (
            session
            .query(db.User)
            .order_by('id')
            .limit(1)
        )
        user = query.first()
        self.id = user.id
