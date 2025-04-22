import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import psycopg2
import psycopg2.extras

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "public")


def load_env(path=None):
    path = path or os.path.join(BASE_DIR, ".env")
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


load_env()

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_conn():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. Add it to .env locally or to the "
            "Vercel project environment variables."
        )
    return psycopg2.connect(DATABASE_URL)


def query(sql, params=None, one=False):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            rows = cur.fetchall()
        return (rows[0] if rows else None) if one else rows
    finally:
        conn.close()


def dashboard():
    counts = query(
        """
        SELECT
            (SELECT COUNT(*) FROM books)        AS books,
            (SELECT COUNT(*) FROM authors)      AS authors,
            (SELECT COUNT(*) FROM publishers)   AS publishers,
            (SELECT COUNT(*) FROM customers)    AS customers,
            (SELECT COUNT(*) FROM orders)       AS orders,
            (SELECT COUNT(*) FROM order_items)  AS order_items
        """,
        one=True,
    )
    revenue = query(
        "SELECT COALESCE(SUM(quantity * unit_price), 0) AS revenue FROM order_items",
        one=True,
    )
    top_books = query(
        """
        SELECT b.title, SUM(oi.quantity * oi.unit_price) AS revenue
        FROM order_items oi
        JOIN books b ON b.book_id = oi.book_id
        JOIN orders o ON o.order_id = oi.order_id
        WHERE o.status = 'Delivered'
        GROUP BY b.book_id, b.title
        ORDER BY revenue DESC
        LIMIT 5
        """
    )
    recent_orders = query(
        """
        SELECT o.order_id, o.order_date, o.status,
               c.first_name || ' ' || c.last_name AS customer,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        GROUP BY o.order_id, o.order_date, o.status, c.first_name, c.last_name
        ORDER BY o.order_date DESC, o.order_id DESC
        LIMIT 6
        """
    )
    status = query(
        "SELECT status, COUNT(*) AS count FROM orders GROUP BY status ORDER BY count DESC"
    )
    return {
        "counts": counts,
        "revenue": revenue["revenue"],
        "top_books": top_books,
        "recent_orders": recent_orders,
        "status": status,
    }


def books(params):
    where = []
    args = []
    search = params.get("search", [""])[0].strip()
    genre = params.get("genre", [""])[0].strip()
    if search:
        where.append("(b.title ILIKE %s OR b.isbn ILIKE %s)")
        args += [f"%{search}%", f"%{search}%"]
    if genre:
        where.append("b.genre = %s")
        args.append(genre)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    return query(
        f"""
        SELECT b.book_id, b.title, b.isbn, b.genre, b.publish_year, b.price, b.pages,
               p.name AS publisher,
               COALESCE(STRING_AGG(a.first_name || ' ' || a.last_name, ', '), '—') AS authors
        FROM books b
        LEFT JOIN publishers p ON p.publisher_id = b.publisher_id
        LEFT JOIN book_authors ba ON ba.book_id = b.book_id
        LEFT JOIN authors a ON a.author_id = ba.author_id
        {where_sql}
        GROUP BY b.book_id, p.name
        ORDER BY b.book_id
        LIMIT 300
        """,
        args,
    )


def books_meta():
    genres = query("SELECT DISTINCT genre FROM books WHERE genre IS NOT NULL ORDER BY genre")
    publishers = query("SELECT publisher_id, name FROM publishers ORDER BY name")
    return {
        "genres": [r["genre"] for r in genres],
        "publishers": publishers,
    }


def authors(params):
    search = params.get("search", [""])[0].strip()
    where = ""
    args = []
    if search:
        where = "WHERE (a.first_name ILIKE %s OR a.last_name ILIKE %s)"
        args = [f"%{search}%", f"%{search}%"]
    return query(
        f"""
        SELECT a.author_id, a.first_name, a.last_name, a.country, a.birth_year,
               COUNT(ba.book_id) AS book_count
        FROM authors a
        LEFT JOIN book_authors ba ON ba.author_id = a.author_id
        {where}
        GROUP BY a.author_id
        ORDER BY a.last_name, a.first_name
        LIMIT 300
        """,
        args,
    )


def publishers(params):
    return query(
        """
        SELECT p.publisher_id, p.name, p.country,
               COUNT(b.book_id) AS book_count,
               COALESCE(ROUND(AVG(b.price), 2), 0) AS avg_price
        FROM publishers p
        LEFT JOIN books b ON b.publisher_id = p.publisher_id
        GROUP BY p.publisher_id
        ORDER BY p.name
        """
    )


def customers(params):
    search = params.get("search", [""])[0].strip()
    where = ""
    args = []
    if search:
        where = (
            "WHERE (c.first_name ILIKE %s OR c.last_name ILIKE %s "
            "OR c.email ILIKE %s OR c.city ILIKE %s)"
        )
        args = [f"%{search}%"] * 4
    return query(
        f"""
        SELECT c.customer_id, c.first_name, c.last_name, c.email, c.city, c.state,
               c.signup_date,
               COUNT(DISTINCT o.order_id) AS order_count,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_spent
        FROM customers c
        LEFT JOIN orders o ON o.customer_id = c.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        {where}
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT 300
        """,
        args,
    )


def orders(params):
    where = []
    args = []
    search = params.get("search", [""])[0].strip()
    status = params.get("status", [""])[0].strip()
    if search:
        where.append(
            "(c.first_name ILIKE %s OR c.last_name ILIKE %s OR CAST(o.order_id AS TEXT) = %s)"
        )
        args += [f"%{search}%", f"%{search}%", search]
    if status:
        where.append("o.status = %s")
        args.append(status)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""
    return query(
        f"""
        SELECT o.order_id, o.order_date, o.status,
               c.customer_id,
               c.first_name || ' ' || c.last_name AS customer,
               COUNT(oi.order_item_id) AS item_count,
               COALESCE(SUM(oi.quantity), 0) AS copies,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        {where_sql}
        GROUP BY o.order_id, c.customer_id, c.first_name, c.last_name
        ORDER BY o.order_date DESC, o.order_id DESC
        LIMIT 300
        """,
        args,
    )


def order_statuses():
    return query("SELECT DISTINCT status FROM orders ORDER BY status")


def analytics():
    return {
        "revenue_by_month": query(
            """
            SELECT TO_CHAR(o.order_date, 'YYYY-MM') AS month,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM orders o
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY month
            ORDER BY month
            """
        ),
        "top_books_revenue": query(
            """
            SELECT b.title, SUM(oi.quantity) AS copies,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM order_items oi
            JOIN books b ON b.book_id = oi.book_id
            JOIN orders o ON o.order_id = oi.order_id
            WHERE o.status = 'Delivered'
            GROUP BY b.book_id, b.title
            ORDER BY revenue DESC
            LIMIT 5
            """
        ),
        "top_books_copies": query(
            """
            SELECT b.title, SUM(oi.quantity) AS copies
            FROM order_items oi
            JOIN books b ON b.book_id = oi.book_id
            GROUP BY b.book_id, b.title
            ORDER BY copies DESC
            LIMIT 5
            """
        ),
        "genre_revenue": query(
            """
            SELECT b.genre, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM order_items oi
            JOIN books b ON b.book_id = oi.book_id
            GROUP BY b.genre
            ORDER BY revenue DESC
            """
        ),
        "top_customers": query(
            """
            SELECT c.first_name || ' ' || c.last_name AS customer,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
            FROM customers c
            JOIN orders o ON o.customer_id = c.customer_id
            JOIN order_items oi ON oi.order_id = o.order_id
            GROUP BY c.customer_id, c.first_name, c.last_name
            ORDER BY total_spent DESC
            LIMIT 10
            """
        ),
        "publisher_revenue": query(
            """
            SELECT p.name AS publisher,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue,
                   SUM(oi.quantity) AS copies
            FROM publishers p
            JOIN books b ON b.publisher_id = p.publisher_id
            JOIN order_items oi ON oi.book_id = b.book_id
            GROUP BY p.publisher_id, p.name
            ORDER BY revenue DESC
            """
        ),
        "avg_order_value": query(
            """
            SELECT ROUND(AVG(total), 2) AS avg_order_value
            FROM (
                SELECT order_id, SUM(quantity * unit_price) AS total
                FROM order_items
                GROUP BY order_id
            ) t
            """,
            one=True,
        ),
        "status_counts": query(
            "SELECT status, COUNT(*) AS count FROM orders GROUP BY status ORDER BY count DESC"
        ),
        "top_author": query(
            """
            SELECT a.first_name || ' ' || a.last_name AS author,
                   COUNT(DISTINCT ba.book_id) AS book_count
            FROM authors a
            JOIN book_authors ba ON ba.author_id = a.author_id
            GROUP BY a.author_id, a.first_name, a.last_name
            ORDER BY book_count DESC, author
            LIMIT 1
            """,
            one=True,
        ),
    }


def customer_orders(params):
    customer_id = params.get("customer_id", [""])[0].strip()
    if not customer_id:
        return []
    return query(
        """
        SELECT o.order_id, o.order_date, o.status,
               COALESCE(SUM(oi.quantity), 0) AS copies,
               COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total
        FROM orders o
        LEFT JOIN order_items oi ON oi.order_id = o.order_id
        WHERE o.customer_id = %s
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
        """,
        [int(customer_id)],
    )


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, name):
        path = os.path.normpath(os.path.join(STATIC_DIR, name))
        if not path.startswith(STATIC_DIR) or not os.path.isfile(path):
            self.send_error(404)
            return
        ext = os.path.splitext(path)[1]
        types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
        }
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", types.get(ext, "application/octet-stream"))
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def dispatch(self, route, params):
        routes = {
            "dashboard": lambda: dashboard(),
            "books": lambda: books(params),
            "books/meta": lambda: books_meta(),
            "authors": lambda: authors(params),
            "publishers": lambda: publishers(params),
            "customers": lambda: customers(params),
            "customers/orders": lambda: customer_orders(params),
            "orders": lambda: orders(params),
            "order-statuses": lambda: order_statuses(),
            "analytics": lambda: analytics(),
        }
        fn = routes.get(route)
        if fn is None:
            self.send_json({"error": "Not found", "route": route}, 404)
            return
        self.send_json(fn())

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        params = parse_qs(parsed.query)

        try:
            if path.startswith("/api"):
                route = params.get("route", [""])[0].strip("/")
                if not route and path not in ("/api", "/api/index"):
                    route = path[len("/api/"):].strip("/")
                self.dispatch(route, params)
                return

            if path == "/":
                self.send_file("index.html")
            else:
                self.send_file(path.lstrip("/"))
        except Exception as exc:
            self.send_json({"error": str(exc)}, 500)

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


handler = Handler
