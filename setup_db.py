import os
import re
import psycopg2

from api.index import BASE_DIR, DATABASE_URL

VALUES_FILE = os.path.join(BASE_DIR, ".db", "Values.sql")

SCHEMA = """
CREATE TABLE IF NOT EXISTS publishers (
    publisher_id INT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    country      VARCHAR(50)  NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
    author_id   INT PRIMARY KEY,
    first_name  VARCHAR(50) NOT NULL,
    last_name   VARCHAR(50) NOT NULL,
    country     VARCHAR(50),
    birth_year  INT
);

CREATE TABLE IF NOT EXISTS books (
    book_id      INT PRIMARY KEY,
    title        VARCHAR(200) NOT NULL,
    isbn         VARCHAR(20) UNIQUE,
    genre        VARCHAR(30),
    publisher_id INT REFERENCES publishers(publisher_id),
    publish_year INT,
    price        DECIMAL(6,2),
    pages        INT
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id   INT REFERENCES books(book_id),
    author_id INT REFERENCES authors(author_id),
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id  INT PRIMARY KEY,
    first_name   VARCHAR(50) NOT NULL,
    last_name    VARCHAR(50) NOT NULL,
    email        VARCHAR(100) UNIQUE,
    city         VARCHAR(50),
    state        VARCHAR(50),
    signup_date  DATE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id    INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date  DATE,
    status      VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INT PRIMARY KEY,
    order_id      INT REFERENCES orders(order_id),
    book_id       INT REFERENCES books(book_id),
    quantity      INT,
    unit_price    DECIMAL(6,2)
);
"""


def main():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(SCHEMA)

    cur.execute("SELECT COUNT(*) FROM books")
    if cur.fetchone()[0] > 0:
        print("Database already has data. Nothing to seed.")
        conn.close()
        return

    with open(VALUES_FILE, "r", encoding="utf-8") as f:
        raw = f.read()

    raw = "\n".join(
        line for line in raw.splitlines() if not line.strip().upper().startswith("USE ")
    )
    raw = re.sub(r"--[^\n]*", "", raw)

    cur.execute(raw)
    print("Database schema created and data inserted.")
    conn.close()


if __name__ == "__main__":
    main()
