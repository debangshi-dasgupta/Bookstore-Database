-- create.sql
-- Step 1: Delete old bookstore if it exists, then make a fresh one
DROP DATABASE IF EXISTS bookstore;
CREATE DATABASE bookstore;
USE bookstore;

-- Step 2: Make the tables (the order matters because of the foreign keys)

CREATE TABLE publishers (
    publisher_id INT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    country      VARCHAR(50)  NOT NULL
);

CREATE TABLE authors (
    author_id   INT PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    country     VARCHAR(50),
    birth_year  INT
);

CREATE TABLE books (
    book_id      INT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    isbn         VARCHAR(20) UNIQUE,
    genre        VARCHAR(30),
    publisher_id INT,
    publish_year INT,
    price        DECIMAL(6,2),
    pages        INT,
    FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
);

CREATE TABLE book_authors (
    book_id   INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id)   REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

CREATE TABLE customers (
    customer_id  INT PRIMARY KEY,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    email        VARCHAR(100) UNIQUE,
    city         VARCHAR(50),
    state        VARCHAR(50),
    signup_date  DATE
);

CREATE TABLE orders (
    order_id    INT PRIMARY KEY,
    customer_id INT,
    order_date  DATE,
    status      VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT,
    book_id       INT,
    quantity      INT,
    unit_price    DECIMAL(6,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (book_id)  REFERENCES books(book_id)
);