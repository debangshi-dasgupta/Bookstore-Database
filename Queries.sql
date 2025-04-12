-- Which 5 books earned the most money?
-- SELECT b.title,
      -- SUM(oi.quantity * oi.unit_price) AS total_revenue
-- FROM order_items oi
-- JOIN books b       ON oi.book_id = b.book_id
-- JOIN orders o      ON oi.order_id = o.order_id
-- WHERE o.status = 'Delivered'
-- GROUP BY b.book_id, b.title
-- ORDER BY total_revenue DESC
-- LIMIT 5;

-- Sales and Revenue

-- 1. What is the total revenue for the whole store?
USE bookstore;
SELECT SUM(quantity * unit_price) AS total_revenue
FROM order_items;
-- 2. What is the revenue per month?
SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS month,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month;
-- 3. What are the top 5 best-selling books by quantity?
SELECT
    b.title,
    SUM(oi.quantity) AS copies_sold
FROM books b
JOIN order_items oi ON b.book_id = oi.book_id
GROUP BY b.book_id, b.title
ORDER BY copies_sold DESC
LIMIT 5;
-- 4. Which genre makes the most money?
SELECT
    b.genre,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM books b
JOIN order_items oi ON b.book_id = oi.book_id
GROUP BY b.genre
ORDER BY revenue DESC
LIMIT 1;
-- 5. What is the average order value?
SELECT ROUND(AVG(order_total), 2) AS average_order_value
FROM (
    SELECT
        order_id,
        SUM(quantity * unit_price) AS order_total
    FROM order_items
    GROUP BY order_id
) AS order_totals;
-- 6. Which year had the highest revenue?
SELECT
    YEAR(o.order_date) AS year,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY YEAR(o.order_date)
ORDER BY revenue DESC
LIMIT 1;
-- Books and Authors
-- 7. How many books does each publisher have?
SELECT
    p.name AS publisher,
    COUNT(b.book_id) AS book_count
FROM publishers p
LEFT JOIN books b ON p.publisher_id = b.publisher_id
GROUP BY p.publisher_id, p.name
ORDER BY book_count DESC;
-- 8. Which author has written the most books?
SELECT
    a.first_name,
    a.last_name,
    COUNT(DISTINCT ba.book_id) AS book_count
FROM authors a
JOIN book_authors ba ON a.author_id = ba.author_id
GROUP BY a.author_id, a.first_name, a.last_name
HAVING COUNT(DISTINCT ba.book_id) = (
    SELECT MAX(book_count)
    FROM (
        SELECT COUNT(DISTINCT book_id) AS book_count
        FROM book_authors
        GROUP BY author_id
    ) AS author_counts
);
-- 9. What is the average price of books in each genre?
SELECT
    genre,
    ROUND(AVG(price), 2) AS average_price
FROM books
GROUP BY genre
ORDER BY average_price DESC;
-- 10. Which books are more expensive than $30?
SELECT title,price
FROM books
WHERE price > 30
ORDER BY price DESC;
-- 11. Which books were published before 1990?
SELECT title, publish_year
FROM books
WHERE publish_year < 1990
ORDER BY publish_year;
-- 12. What is the longest book in the store?
SELECT title, pages
FROM books
WHERE pages = (SELECT MAX(pages) FROM books);
-- Customers
-- 13. Who are our top 10 customers by spending?
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, customer
ORDER BY total_spent DESC
LIMIT 10;
-- 14. How many customers are in each state?
SELECT state, count(*) AS customer_count
FROM customers
GROUP BY state
ORDER BY customer_count DESC;
-- 15. How many customers have never placed an order?
SELECT c.customer_id, c.first_name, c.last_name
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;
-- 16. Which city has the most customers?
SELECT city, COUNT(*) as customer_count
FROM customers
GROUP BY city
ORDER BY customer_count DESC
LIMIT 1;
-- 17. How many customers signed up each year?
SELECT 
     YEAR(signup_date) as signup_year,
     COUNT(*) AS customer_count 
FROM customers     
GROUP BY YEAR(signup_date)
ORDER BY customer_count;	
-- 18. Who placed the most orders?
SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, customer
ORDER BY order_count DESC
LIMIT 1;

-- Orders and Status
-- 19. How many orders are Delivered, Shipped, Cancelled, or Returned?
SELECT status, COUNT(*) AS order_count
FROM orders
GROUP BY status;
-- 20. What percentage of orders were cancelled?
SELECT
    ROUND(
        100.0 * SUM(status = 'Cancelled') / COUNT(*),
        2
    ) AS cancelled_percentage
FROM orders;
-- 21. What percentage of orders were returned?
SELECT
    ROUND(
        100.0 * SUM(status = 'Returned') / COUNT(*),
        2
    ) AS returned_percentage
FROM orders;
-- 22. How many orders had more than 2 different books?
SELECT COUNT(*) AS order_count
FROM (
    SELECT order_id
    FROM order_items
    GROUP BY order_id
    HAVING COUNT(DISTINCT book_id) > 2
) AS multi_book_orders;
-- 23. What is the biggest single order?
SELECT
    order_id,
    SUM(quantity * unit_price) AS order_total
FROM order_items
GROUP BY order_id
ORDER BY order_total DESC
LIMIT 1;

-- Publishers and Countries
-- 24. Which publisher earns the most money?
SELECT
    p.name AS publisher,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
FROM publishers p
JOIN books b ON p.publisher_id = b.publisher_id
JOIN order_items oi ON b.book_id = oi.book_id
GROUP BY p.publisher_id, p.name
ORDER BY revenue DESC
LIMIT 1;
-- 25. Which publisher’s books sell the most copies?
SELECT
    p.name AS publisher,
    SUM(oi.quantity) AS copies_sold
FROM publishers p
JOIN books b ON p.publisher_id = b.publisher_id
JOIN order_items oi ON b.book_id = oi.book_id
GROUP BY p.publisher_id, p.name
ORDER BY copies_sold DESC
LIMIT 1;
-- 26. How many books come from publishers in each country?
SELECT
    p.country,
    COUNT(b.book_id) AS book_count
FROM publishers p
JOIN books b ON p.publisher_id = b.publisher_id
GROUP BY p.country
ORDER BY book_count DESC;

-- Advanced Thinking
-- 27. Which genre is most popular in each state?
WITH state_genre_sales AS (
    SELECT
        c.state,
        b.genre,
        SUM(oi.quantity) AS copies_sold
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN books b ON oi.book_id = b.book_id
    GROUP BY c.state, b.genre
),
ranked_genres AS (
    SELECT *,
        DENSE_RANK() OVER (
            PARTITION BY state
            ORDER BY copies_sold DESC
        ) AS genre_rank
    FROM state_genre_sales
)
SELECT state, genre, copies_sold
FROM ranked_genres
WHERE genre_rank = 1
ORDER BY state;
-- 28. Which books have never been ordered?
SELECT b.book_id, b.title
FROM books b
LEFT JOIN order_items oi ON b.book_id = oi.book_id
WHERE oi.book_id IS NULL;
-- 29. Which authors’ books have the highest average price?
SELECT
    a.first_name,
    a.last_name,
    ROUND(AVG(b.price), 2) AS average_price
FROM authors a
JOIN book_authors ba ON a.author_id = ba.author_id
JOIN books b ON ba.book_id = b.book_id
GROUP BY a.author_id, a.first_name, a.last_name
ORDER BY average_price DESC
LIMIT 1;
-- 30. Find customers who bought books in at least 3 different genres.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(DISTINCT b.genre) AS genre_count
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN books b ON oi.book_id = b.book_id
GROUP BY c.customer_id, c.first_name, c.last_name
HAVING COUNT(DISTINCT b.genre) >= 3
ORDER BY genre_count DESC;