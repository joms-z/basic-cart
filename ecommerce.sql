PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS carts;
DROP TABLE IF EXISTS cart_products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_products;
DROP TABLE IF EXISTS suppliers;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE carts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE cart_products (
    id INTEGER PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES carts(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY (product_id) REFERENCES products(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE order_products (
    id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT,
    FOREIGN KEY (product_id) REFERENCES products(id)
        ON UPDATE RESTRICT ON DELETE RESTRICT
);


INSERT INTO users (id, name) VALUES
    (1, 'Elliot Alderson'),
    (2, 'Angela Moss'),
    (3, 'Tyrell Wellick'),
    (4, 'Darlene Alderson');

INSERT INTO products (name) VALUES
    ('Coffee'),
    ('Bananas'),
    ('Oranges'),
    ('Pears'),
    ('Apples'),
    ('Grapes'),
    ('Cereal'),
    ('Milk'),
    ('Chicken'),
    ('Beef'),
    ('Soap'),
    ('Shampoo'),
    ('Toothpaste'),
    ('Toothbrush');
