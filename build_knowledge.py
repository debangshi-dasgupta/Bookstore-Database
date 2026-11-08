"""Generate knowledge.md from the seed data in .db/Values.sql.

Run this whenever the catalog changes:

    python build_knowledge.py

The generated knowledge.md is the source document for the RAG assistant.
"""

import ast
import os
import re
from collections import Counter, defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VALUES_FILE = os.path.join(BASE_DIR, ".db", "Values.sql")
OUTPUT_FILE = os.path.join(BASE_DIR, "knowledge.md")


def _split_values(raw):
    rows = []
    depth = 0
    quote = None
    start = None
    i = 0
    while i < len(raw):
        ch = raw[i]
        if quote:
            if ch == quote:
                if i + 1 < len(raw) and raw[i + 1] == quote:
                    i += 1
                else:
                    quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "(":
            if depth == 0:
                start = i + 1
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0 and start is not None:
                rows.append(raw[start:i])
                start = None
        i += 1
    return rows


def _split_tokens(raw):
    tokens = []
    current = ""
    quote = None
    i = 0
    while i < len(raw):
        ch = raw[i]
        if quote:
            current += ch
            if ch == quote:
                if i + 1 < len(raw) and raw[i + 1] == quote:
                    current += raw[i + 1]
                    i += 1
                else:
                    quote = None
        elif ch in ("'", '"'):
            quote = ch
            current += ch
        elif ch == ",":
            tokens.append(current.strip())
            current = ""
        else:
            current += ch
        i += 1
    if current.strip():
        tokens.append(current.strip())
    return tokens


def _coerce(token):
    token = token.strip()
    if token.upper() == "NULL":
        return None
    try:
        return ast.literal_eval(token)
    except (ValueError, SyntaxError):
        return token


def parse_values(path):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    sql = re.sub(r"--[^\n]*", "", sql)
    tables = defaultdict(list)
    pattern = re.compile(
        r"INSERT\s+INTO\s+(\w+)\s*\(([^)]*)\)\s*VALUES\s*(.*?);",
        re.IGNORECASE | re.DOTALL,
    )
    for match in pattern.finditer(sql):
        table = match.group(1).lower()
        columns = [c.strip() for c in match.group(2).split(",")]
        for row in _split_values(match.group(3)):
            values = [_coerce(t) for t in _split_tokens(row)]
            tables[table].append(dict(zip(columns, values)))
    return tables


def money(value):
    return "${:,.2f}".format(float(value or 0))


def main():
    data = parse_values(VALUES_FILE)
    publishers = {p["publisher_id"]: p for p in data["publishers"]}
    authors = {a["author_id"]: a for a in data["authors"]}

    book_authors = defaultdict(list)
    for link in data["book_authors"]:
        author = authors.get(link["author_id"])
        if author:
            book_authors[link["book_id"]].append(
                "{} {}".format(author["first_name"], author["last_name"])
            )

    author_books = defaultdict(int)
    author_titles = defaultdict(list)
    for link in data["book_authors"]:
        author_books[link["author_id"]] += 1
        book = next((b for b in data["books"] if b["book_id"] == link["book_id"]), None)
        if book:
            author_titles[link["author_id"]].append(book["title"])

    copies = Counter()
    for item in data["order_items"]:
        copies[item["book_id"]] += int(item["quantity"] or 0)

    books = data["books"]
    genre_counts = Counter(b["genre"] for b in books if b.get("genre"))

    lines = []
    lines.append("# Bookstore Database — Knowledge Base")
    lines.append("")
    lines.append(
        "This document is the authoritative knowledge base for the Bookstore "
        "Database Explorer application. The assistant must answer only from "
        "this document and only about the bookstore domain: books, authors, "
        "publishers, genres, prices, catalog details, inventory, sales, "
        "customers, orders, and analytics."
    )
    lines.append("")
    lines.append("## Application scope")
    lines.append("")
    lines.append(
        "- The app is a read-only explorer for a PostgreSQL bookstore database."
    )
    lines.append(
        "- It provides dashboards, book/author/publisher/customer/order "
        "listings, and analytics."
    )
    lines.append(
        "- The assistant helps users find catalog information, publisher "
        "details, author details, prices, genres, page counts, publication "
        "years, ISBNs, and sales-related facts."
    )
    lines.append(
        "- The assistant must refuse unrelated requests (general knowledge, "
        "coding help, news, politics, personal advice, etc.) and redirect the "
        "user back to bookstore questions."
    )
    lines.append("")
    lines.append("## Database schema")
    lines.append("")
    lines.append(
        "- publishers(publisher_id, name, country): companies that publish books."
    )
    lines.append(
        "- authors(author_id, first_name, last_name, country, birth_year): "
        "book authors."
    )
    lines.append(
        "- books(book_id, title, isbn, genre, publisher_id, publish_year, "
        "price, pages): the catalog."
    )
    lines.append(
        "- book_authors(book_id, author_id): many-to-many link between books "
        "and authors."
    )
    lines.append(
        "- customers(customer_id, first_name, last_name, email, city, state, "
        "signup_date): registered customers."
    )
    lines.append(
        "- orders(order_id, customer_id, order_date, status): customer orders. "
        "Statuses include Pending, Shipped, Delivered, Cancelled."
    )
    lines.append(
        "- order_items(order_item_id, order_id, book_id, quantity, unit_price): "
        "line items in an order."
    )
    lines.append("")
    lines.append("## Catalog summary")
    lines.append("")
    lines.append("- Total books: {}".format(len(books)))
    lines.append("- Total authors: {}".format(len(authors)))
    lines.append("- Total publishers: {}".format(len(publishers)))
    lines.append(
        "- Genres: "
        + ", ".join(
            "{} ({})".format(g, n) for g, n in sorted(genre_counts.items())
        )
    )
    prices = [float(b["price"] or 0) for b in books]
    if prices:
        lines.append(
            "- Price range: {} to {} (average {})".format(
                money(min(prices)), money(max(prices)), money(sum(prices) / len(prices))
            )
        )
    years = [int(b["publish_year"]) for b in books if b.get("publish_year")]
    if years:
        lines.append(
            "- Publication years: {} to {}".format(min(years), max(years))
        )
    lines.append("")
    lines.append("## Publishers")
    lines.append("")
    for publisher in sorted(publishers.values(), key=lambda p: p["name"]):
        pub_books = [b for b in books if b["publisher_id"] == publisher["publisher_id"]]
        avg = (
            sum(float(b["price"] or 0) for b in pub_books) / len(pub_books)
            if pub_books
            else 0
        )
        lines.append(
            "- {name} (publisher_id {pid}, {country}) publishes {count} "
            "titles; average price {avg}.".format(
                name=publisher["name"],
                pid=publisher["publisher_id"],
                country=publisher["country"],
                count=len(pub_books),
                avg=money(avg),
            )
        )
    lines.append("")
    lines.append("## Authors")
    lines.append("")
    for author in sorted(
        authors.values(), key=lambda a: (a["last_name"], a["first_name"])
    ):
        titles = sorted(author_titles.get(author["author_id"], []))
        lines.append(
            "- {first} {last} (author_id {aid}, {country}, born {birth}) has "
            "{count} book(s) in the catalog: {titles}.".format(
                first=author["first_name"],
                last=author["last_name"],
                aid=author["author_id"],
                country=author["country"],
                birth=author["birth_year"],
                count=author_books[author["author_id"]],
                titles=", ".join(titles) or "none",
            )
        )
    lines.append("")
    lines.append("## Books catalog")
    lines.append("")
    lines.append(
        "Each entry lists the book title, authors, publisher, genre, "
        "publication year, price, page count, and ISBN."
    )
    lines.append("")
    for book in sorted(books, key=lambda b: b["title"]):
        publisher = publishers.get(book["publisher_id"], {})
        writer_names = ", ".join(book_authors.get(book["book_id"], [])) or "Unknown author"
        lines.append(
            "- {title} — by {writers} — published by {publisher} ({country}) — "
            "{genre} — {year} — {price} — {pages} pages — ISBN {isbn}.".format(
                title=book["title"],
                writers=writer_names,
                publisher=publisher.get("name", "Unknown publisher"),
                country=publisher.get("country", "unknown"),
                genre=book.get("genre") or "Uncategorized",
                year=book.get("publish_year"),
                price=money(book.get("price")),
                pages=book.get("pages"),
                isbn=book.get("isbn"),
            )
        )
    lines.append("")
    lines.append("## Best-selling books by copies sold")
    lines.append("")
    top = copies.most_common(20)
    for rank, (book_id, qty) in enumerate(top, start=1):
        book = next((b for b in books if b["book_id"] == book_id), None)
        if book:
            lines.append(
                "{}. {} — {} copies sold.".format(rank, book["title"], qty)
            )
    lines.append("")
    lines.append("## Example questions the assistant can answer")
    lines.append("")
    lines.append("- Which books were written by Ava Singh?")
    lines.append("- Who publishes 'Wild Kingdom of Dawn' and what does it cost?")
    lines.append("- Show me books in the Fantasy genre.")
    lines.append("- Which publisher has the most titles?")
    lines.append("- What is the average price of books from Blue Lantern Press?")
    lines.append("- Which books are best sellers?")
    lines.append("- Tell me about author Omar Duarte.")
    lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print("Wrote {} ({} lines)".format(OUTPUT_FILE, len(lines)))


if __name__ == "__main__":
    main()
