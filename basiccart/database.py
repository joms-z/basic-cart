import os.path

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
)
from sqlalchemy import and_, not_, or_

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_PATH, 'ecommerce.db')
Base = declarative_base()


def create_engine(uri=None):
    from sqlalchemy import create_engine

    uri = uri or 'sqlite:///{}'.format(DATABASE)
    engine = create_engine(uri, echo=True)
    return engine


def create_session(engine):
    Session = scoped_session(sessionmaker(bind=engine))
    return Session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,
        ForeignKey('users.id'), nullable=False)


class CartProduct(Base):
    __tablename__ = 'cart_products'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer,
        ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer,
        ForeignKey('products.id'), nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,
        ForeignKey('users.id'), nullable=False)


class OrderProduct(Base):
    __tablename__ = 'order_products'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer,
        ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer,
        ForeignKey('products.id'), nullable=False)
