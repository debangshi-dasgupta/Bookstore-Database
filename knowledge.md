# Bookstore Database — Knowledge Base

This document is the authoritative knowledge base for the Bookstore Database Explorer application. The assistant must answer only from this document and only about the bookstore domain: books, authors, publishers, genres, prices, catalog details, inventory, sales, customers, orders, and analytics.

## Application scope

- The app is a read-only explorer for a PostgreSQL bookstore database.
- It provides dashboards, book/author/publisher/customer/order listings, and analytics.
- The assistant helps users find catalog information, publisher details, author details, prices, genres, page counts, publication years, ISBNs, and sales-related facts.
- The assistant must refuse unrelated requests (general knowledge, coding help, news, politics, personal advice, etc.) and redirect the user back to bookstore questions.

## Database schema

- publishers(publisher_id, name, country): companies that publish books.
- authors(author_id, first_name, last_name, country, birth_year): book authors.
- books(book_id, title, isbn, genre, publisher_id, publish_year, price, pages): the catalog.
- book_authors(book_id, author_id): many-to-many link between books and authors.
- customers(customer_id, first_name, last_name, email, city, state, signup_date): registered customers.
- orders(order_id, customer_id, order_date, status): customer orders. Statuses include Pending, Shipped, Delivered, Cancelled.
- order_items(order_item_id, order_id, book_id, quantity, unit_price): line items in an order.

## Catalog summary

- Total books: 120
- Total authors: 40
- Total publishers: 10
- Genres: Children (25), Fantasy (14), Fiction (9), History (14), Mystery (14), Romance (14), Science (14), Self-Help (16)
- Price range: $6.05 to $39.99 (average $22.26)
- Publication years: 1985 to 2025

## Publishers

- Blue Lantern Press (publisher_id 1, USA) publishes 12 titles; average price $17.95.
- Golden Fig Press (publisher_id 7, USA) publishes 12 titles; average price $24.14.
- Harbor Lane Books (publisher_id 6, Australia) publishes 8 titles; average price $26.65.
- Lotus Page (publisher_id 9, India) publishes 12 titles; average price $23.11.
- Maple Leaf Books (publisher_id 2, Canada) publishes 17 titles; average price $23.75.
- Northwind Publishing (publisher_id 8, Canada) publishes 15 titles; average price $24.48.
- Owl and Oak (publisher_id 10, UK) publishes 9 titles; average price $20.78.
- Red Kite Publishing (publisher_id 3, UK) publishes 7 titles; average price $17.18.
- Silver Pine Media (publisher_id 5, USA) publishes 13 titles; average price $23.21.
- Sunrise House (publisher_id 4, India) publishes 15 titles; average price $19.70.

## Authors

- Leo Brooks (author_id 31, USA, born 1954) has 4 book(s) in the catalog: Crimson Storm of Dawn, Forgotten Letter Returns, Quiet Compass, Wild Clock of Dawn.
- Maya Chen (author_id 13, UK, born 1985) has 3 book(s) in the catalog: Crimson River of Dawn, Quiet Harbor, Wild River Returns.
- Aisha Duarte (author_id 29, Australia, born 1954) has 4 book(s) in the catalog: Broken Empire Returns, Broken Garden, Golden Clock Returns, Silent River.
- Omar Duarte (author_id 7, India, born 1974) has 5 book(s) in the catalog: Broken Storm, Crimson Storm of Dawn, Endless Compass of Dawn, Endless River of Dawn, Quiet Harbor Returns.
- Zara Duarte (author_id 38, India, born 1949) has 3 book(s) in the catalog: Forgotten Mountain Returns, Last Letter of Dawn, Wild River of Dawn.
- Diego Haddad (author_id 11, Australia, born 1995) has 4 book(s) in the catalog: Crimson River, Golden Storm of Dawn, Last Garden Returns, Quiet Letter.
- Hana Haddad (author_id 26, UK, born 1950) has 4 book(s) in the catalog: Broken Mountain, Crimson Empire of Dawn, Hidden Compass, Quiet Kingdom.
- Aisha Iyer (author_id 15, UK, born 1989) has 6 book(s) in the catalog: Endless Mountain Returns, Hidden Garden of Dawn, Quiet Storm, Silent Garden Returns, Silent Letter of Dawn, Wild Mountain of Dawn.
- Ava Iyer (author_id 16, Canada, born 1945) has 5 book(s) in the catalog: Forgotten Letter Returns, Last Garden of Dawn, Last River Returns, Last Storm Returns, Quiet Kingdom Returns.
- Diego Keller (author_id 37, India, born 1965) has 2 book(s) in the catalog: Quiet River of Dawn, Wild Compass Returns.
- Hana Keller (author_id 9, USA, born 1975) has 3 book(s) in the catalog: Hidden River of Dawn, Hidden Storm Returns, Silent Kingdom Returns.
- Maya Keller (author_id 2, USA, born 1964) has 1 book(s) in the catalog: Endless Empire.
- Maya Kim (author_id 18, USA, born 1964) has 2 book(s) in the catalog: Quiet Garden of Dawn, Wild Garden Returns.
- Nina Kim (author_id 1, Canada, born 1946) has 5 book(s) in the catalog: Crimson Mountain, Endless Letter of Dawn, Last Kingdom, Quiet Empire of Dawn, Quiet Storm of Dawn.
- Sofia Kim (author_id 24, USA, born 1978) has 1 book(s) in the catalog: Broken Storm.
- Ava Larsen (author_id 23, Canada, born 1984) has 4 book(s) in the catalog: Crimson Garden, Forgotten Mountain Returns, Golden Kingdom Returns, Quiet Compass of Dawn.
- Omar Moreau (author_id 40, UK, born 1987) has 7 book(s) in the catalog: Broken River, Crimson Letter, Forgotten Harbor Returns, Last Compass, Last Empire of Dawn, Last River Returns, Silent Garden of Dawn.
- Diego Murphy (author_id 28, Canada, born 1980) has 4 book(s) in the catalog: Last Letter, Silent Mountain, Wild Clock Returns, Wild Garden of Dawn.
- Hana Murphy (author_id 4, Canada, born 1978) has 3 book(s) in the catalog: Golden Clock Returns, Silent Kingdom of Dawn, Wild River.
- Kofi Murphy (author_id 12, Canada, born 1976) has 4 book(s) in the catalog: Endless Letter Returns, Forgotten Letter of Dawn, Hidden Mountain Returns, Wild Compass Returns.
- Noah Murphy (author_id 39, Canada, born 1948) has 5 book(s) in the catalog: Crimson Kingdom Returns, Crimson River of Dawn, Golden Clock, Last Compass of Dawn, Wild Kingdom of Dawn.
- Omar Murphy (author_id 20, Canada, born 1950) has 3 book(s) in the catalog: Broken Mountain Returns, Endless River, Last Garden Returns.
- Lena Novak (author_id 6, USA, born 1986) has 4 book(s) in the catalog: Endless Mountain Returns, Forgotten Compass, Silent Compass of Dawn, Silent Kingdom.
- Ava Okafor (author_id 34, Canada, born 1944) has 4 book(s) in the catalog: Broken Empire Returns, Endless River of Dawn, Last Harbor of Dawn, Wild Harbor.
- Arjun Patel (author_id 14, USA, born 1942) has 0 book(s) in the catalog: none.
- Ravi Patel (author_id 33, Canada, born 1965) has 2 book(s) in the catalog: Forgotten Kingdom Returns, Wild Kingdom Returns.
- Mei Reyes (author_id 21, Canada, born 1962) has 6 book(s) in the catalog: Forgotten Garden, Forgotten Storm Returns, Golden River of Dawn, Quiet Kingdom of Dawn, Silent Clock Returns, Silent Storm.
- Arjun Rivera (author_id 32, USA, born 1991) has 3 book(s) in the catalog: Crimson Storm, Forgotten Compass, Forgotten Garden.
- Omar Rivera (author_id 25, UK, born 1974) has 2 book(s) in the catalog: Endless Clock, Golden Mountain.
- Priya Rivera (author_id 36, Canada, born 1953) has 3 book(s) in the catalog: Broken Letter of Dawn, Endless Compass, Golden Storm.
- Arjun Silva (author_id 22, UK, born 1982) has 4 book(s) in the catalog: Broken River Returns, Crimson Garden, Forgotten Clock, Silent Compass of Dawn.
- Tariq Silva (author_id 35, UK, born 1976) has 3 book(s) in the catalog: Crimson Garden of Dawn, Endless Clock of Dawn, Last Mountain.
- Ava Singh (author_id 3, USA, born 1962) has 3 book(s) in the catalog: Golden River, Hidden River of Dawn, Quiet Clock Returns.
- Maya Singh (author_id 10, Canada, born 1993) has 8 book(s) in the catalog: Endless Clock, Forgotten Letter, Golden Storm, Last Letter of Dawn, Quiet River Returns, Quiet Storm of Dawn, Silent River, Wild Clock.
- Nina Singh (author_id 27, India, born 1964) has 8 book(s) in the catalog: Broken Letter, Endless River, Golden Kingdom Returns, Hidden Empire of Dawn, Hidden River Returns, Silent Garden Returns, Wild Harbor Returns, Wild River.
- Omar Singh (author_id 30, Canada, born 1993) has 8 book(s) in the catalog: Broken Harbor Returns, Endless Harbor, Endless Mountain of Dawn, Forgotten Storm Returns, Golden Compass, Quiet Compass Returns, Silent Letter, Silent River Returns.
- Ravi Stone (author_id 5, Canada, born 1991) has 4 book(s) in the catalog: Broken Empire of Dawn, Forgotten Letter, Forgotten Mountain of Dawn, Hidden Letter.
- Noah Tanaka (author_id 8, USA, born 1964) has 1 book(s) in the catalog: Crimson Storm.
- Omar Tanaka (author_id 19, Canada, born 1969) has 7 book(s) in the catalog: Broken Letter Returns, Broken Mountain, Broken Storm of Dawn, Crimson Garden of Dawn, Forgotten Kingdom Returns, Hidden Garden of Dawn, Last Kingdom Returns.
- Ava Walsh (author_id 17, UK, born 1995) has 3 book(s) in the catalog: Broken River Returns, Endless Letter of Dawn, Silent Harbor of Dawn.

## Books catalog

Each entry lists the book title, authors, publisher, genre, publication year, price, page count, and ISBN.

- Broken Empire Returns — by Ava Okafor, Aisha Duarte — published by Sunrise House (India) — Mystery — 1995 — $19.81 — 612 pages — ISBN 978-0000000008.
- Broken Empire of Dawn — by Ravi Stone — published by Northwind Publishing (Canada) — Fantasy — 1992 — $21.93 — 431 pages — ISBN 978-0000000119.
- Broken Garden — by Aisha Duarte — published by Lotus Page (India) — Children — 2006 — $17.95 — 584 pages — ISBN 978-0000000097.
- Broken Harbor Returns — by Omar Singh — published by Blue Lantern Press (USA) — History — 2024 — $11.17 — 249 pages — ISBN 978-0000000077.
- Broken Letter — by Nina Singh — published by Owl and Oak (UK) — Mystery — 1989 — $28.95 — 360 pages — ISBN 978-0000000014.
- Broken Letter Returns — by Omar Tanaka — published by Sunrise House (India) — Romance — 1990 — $15.47 — 581 pages — ISBN 978-0000000088.
- Broken Letter of Dawn — by Priya Rivera — published by Sunrise House (India) — Romance — 2000 — $28.67 — 482 pages — ISBN 978-0000000031.
- Broken Mountain — by Omar Tanaka, Hana Haddad — published by Maple Leaf Books (Canada) — Children — 2021 — $14.36 — 160 pages — ISBN 978-0000000015.
- Broken Mountain Returns — by Omar Murphy — published by Maple Leaf Books (Canada) — Romance — 2004 — $23.23 — 538 pages — ISBN 978-0000000044.
- Broken River — by Omar Moreau — published by Red Kite Publishing (UK) — Fantasy — 1989 — $8.02 — 434 pages — ISBN 978-0000000118.
- Broken River Returns — by Ava Walsh, Arjun Silva — published by Red Kite Publishing (UK) — Self-Help — 2014 — $28.69 — 444 pages — ISBN 978-0000000057.
- Broken Storm — by Sofia Kim, Omar Duarte — published by Silver Pine Media (USA) — History — 2003 — $29.89 — 584 pages — ISBN 978-0000000115.
- Broken Storm of Dawn — by Omar Tanaka — published by Sunrise House (India) — History — 2015 — $15.39 — 409 pages — ISBN 978-0000000100.
- Crimson Empire of Dawn — by Hana Haddad — published by Northwind Publishing (Canada) — Children — 2013 — $16.10 — 559 pages — ISBN 978-0000000110.
- Crimson Garden — by Ava Larsen, Arjun Silva — published by Golden Fig Press (USA) — Children — 1996 — $26.92 — 428 pages — ISBN 978-0000000046.
- Crimson Garden of Dawn — by Omar Tanaka, Tariq Silva — published by Harbor Lane Books (Australia) — Fantasy — 1995 — $26.59 — 237 pages — ISBN 978-0000000079.
- Crimson Kingdom Returns — by Noah Murphy — published by Sunrise House (India) — Self-Help — 2007 — $33.12 — 468 pages — ISBN 978-0000000091.
- Crimson Letter — by Omar Moreau — published by Harbor Lane Books (Australia) — Self-Help — 2006 — $31.87 — 508 pages — ISBN 978-0000000073.
- Crimson Mountain — by Nina Kim — published by Blue Lantern Press (USA) — Romance — 2016 — $34.92 — 306 pages — ISBN 978-0000000090.
- Crimson River — by Diego Haddad — published by Harbor Lane Books (Australia) — Fiction — 2022 — $24.78 — 560 pages — ISBN 978-0000000029.
- Crimson River of Dawn — by Maya Chen, Noah Murphy — published by Maple Leaf Books (Canada) — Fiction — 2001 — $12.06 — 391 pages — ISBN 978-0000000039.
- Crimson Storm — by Arjun Rivera, Noah Tanaka — published by Silver Pine Media (USA) — Science — 1995 — $31.19 — 557 pages — ISBN 978-0000000027.
- Crimson Storm of Dawn — by Leo Brooks, Omar Duarte — published by Harbor Lane Books (Australia) — Children — 2025 — $36.30 — 590 pages — ISBN 978-0000000085.
- Endless Clock — by Omar Rivera, Maya Singh — published by Sunrise House (India) — Mystery — 2004 — $13.63 — 323 pages — ISBN 978-0000000051.
- Endless Clock of Dawn — by Tariq Silva — published by Lotus Page (India) — Mystery — 1998 — $23.19 — 255 pages — ISBN 978-0000000020.
- Endless Compass — by Priya Rivera — published by Blue Lantern Press (USA) — Science — 2004 — $18.39 — 160 pages — ISBN 978-0000000030.
- Endless Compass of Dawn — by Omar Duarte — published by Northwind Publishing (Canada) — Mystery — 2011 — $36.12 — 319 pages — ISBN 978-0000000053.
- Endless Empire — by Maya Keller — published by Blue Lantern Press (USA) — Mystery — 2010 — $30.75 — 231 pages — ISBN 978-0000000004.
- Endless Harbor — by Omar Singh — published by Golden Fig Press (USA) — Mystery — 2022 — $25.21 — 443 pages — ISBN 978-0000000016.
- Endless Letter Returns — by Kofi Murphy — published by Blue Lantern Press (USA) — Science — 2001 — $18.88 — 336 pages — ISBN 978-0000000072.
- Endless Letter of Dawn — by Nina Kim, Ava Walsh — published by Sunrise House (India) — History — 2001 — $28.44 — 280 pages — ISBN 978-0000000112.
- Endless Mountain Returns — by Lena Novak, Aisha Iyer — published by Owl and Oak (UK) — Children — 1994 — $37.47 — 362 pages — ISBN 978-0000000032.
- Endless Mountain of Dawn — by Omar Singh — published by Red Kite Publishing (UK) — History — 2020 — $8.54 — 122 pages — ISBN 978-0000000113.
- Endless River — by Omar Murphy, Nina Singh — published by Silver Pine Media (USA) — Children — 2017 — $24.35 — 568 pages — ISBN 978-0000000120.
- Endless River of Dawn — by Omar Duarte, Ava Okafor — published by Northwind Publishing (Canada) — Children — 2010 — $14.29 — 125 pages — ISBN 978-0000000054.
- Forgotten Clock — by Arjun Silva — published by Maple Leaf Books (Canada) — Self-Help — 2021 — $27.39 — 174 pages — ISBN 978-0000000107.
- Forgotten Compass — by Arjun Rivera, Lena Novak — published by Silver Pine Media (USA) — Children — 2014 — $15.69 — 618 pages — ISBN 978-0000000010.
- Forgotten Garden — by Mei Reyes, Arjun Rivera — published by Northwind Publishing (Canada) — Science — 2013 — $14.80 — 373 pages — ISBN 978-0000000059.
- Forgotten Harbor Returns — by Omar Moreau — published by Lotus Page (India) — Fantasy — 2016 — $27.30 — 401 pages — ISBN 978-0000000060.
- Forgotten Kingdom Returns — by Omar Tanaka, Ravi Patel — published by Blue Lantern Press (USA) — Children — 2015 — $13.55 — 591 pages — ISBN 978-0000000035.
- Forgotten Letter — by Maya Singh, Ravi Stone — published by Blue Lantern Press (USA) — Self-Help — 2020 — $14.46 — 244 pages — ISBN 978-0000000056.
- Forgotten Letter Returns — by Leo Brooks, Ava Iyer — published by Harbor Lane Books (Australia) — Children — 2002 — $35.38 — 405 pages — ISBN 978-0000000037.
- Forgotten Letter of Dawn — by Kofi Murphy — published by Golden Fig Press (USA) — History — 1988 — $11.59 — 122 pages — ISBN 978-0000000009.
- Forgotten Mountain Returns — by Ava Larsen, Zara Duarte — published by Golden Fig Press (USA) — Children — 1997 — $8.57 — 368 pages — ISBN 978-0000000081.
- Forgotten Mountain of Dawn — by Ravi Stone — published by Maple Leaf Books (Canada) — Fiction — 2023 — $20.77 — 441 pages — ISBN 978-0000000040.
- Forgotten Storm Returns — by Omar Singh, Mei Reyes — published by Lotus Page (India) — Children — 1985 — $16.32 — 335 pages — ISBN 978-0000000047.
- Golden Clock — by Noah Murphy — published by Maple Leaf Books (Canada) — Fiction — 1989 — $38.12 — 272 pages — ISBN 978-0000000028.
- Golden Clock Returns — by Aisha Duarte, Hana Murphy — published by Silver Pine Media (USA) — Science — 2003 — $26.55 — 471 pages — ISBN 978-0000000024.
- Golden Compass — by Omar Singh — published by Maple Leaf Books (Canada) — History — 1987 — $31.63 — 373 pages — ISBN 978-0000000076.
- Golden Kingdom Returns — by Ava Larsen, Nina Singh — published by Sunrise House (India) — Science — 2003 — $13.39 — 179 pages — ISBN 978-0000000011.
- Golden Mountain — by Omar Rivera — published by Golden Fig Press (USA) — Science — 1996 — $30.94 — 396 pages — ISBN 978-0000000086.
- Golden River — by Ava Singh — published by Owl and Oak (UK) — Fantasy — 2008 — $22.08 — 472 pages — ISBN 978-0000000096.
- Golden River of Dawn — by Mei Reyes — published by Sunrise House (India) — Fantasy — 2005 — $14.11 — 525 pages — ISBN 978-0000000017.
- Golden Storm — by Priya Rivera, Maya Singh — published by Lotus Page (India) — Romance — 2010 — $29.09 — 459 pages — ISBN 978-0000000038.
- Golden Storm of Dawn — by Diego Haddad — published by Blue Lantern Press (USA) — Science — 2017 — $8.71 — 310 pages — ISBN 978-0000000013.
- Hidden Compass — by Hana Haddad — published by Northwind Publishing (Canada) — History — 2021 — $26.74 — 508 pages — ISBN 978-0000000089.
- Hidden Empire of Dawn — by Nina Singh — published by Owl and Oak (UK) — Children — 2017 — $9.92 — 314 pages — ISBN 978-0000000041.
- Hidden Garden of Dawn — by Omar Tanaka, Aisha Iyer — published by Owl and Oak (UK) — Fantasy — 2002 — $24.89 — 649 pages — ISBN 978-0000000092.
- Hidden Letter — by Ravi Stone — published by Silver Pine Media (USA) — Science — 1991 — $25.67 — 439 pages — ISBN 978-0000000080.
- Hidden Mountain Returns — by Kofi Murphy — published by Lotus Page (India) — Self-Help — 1991 — $7.71 — 135 pages — ISBN 978-0000000007.
- Hidden River Returns — by Nina Singh — published by Silver Pine Media (USA) — Romance — 1999 — $13.57 — 317 pages — ISBN 978-0000000036.
- Hidden River of Dawn — by Ava Singh, Hana Keller — published by Blue Lantern Press (USA) — Science — 1987 — $14.31 — 606 pages — ISBN 978-0000000052.
- Hidden Storm Returns — by Hana Keller — published by Silver Pine Media (USA) — Mystery — 1999 — $19.74 — 369 pages — ISBN 978-0000000095.
- Last Compass — by Omar Moreau — published by Northwind Publishing (Canada) — History — 2016 — $21.23 — 137 pages — ISBN 978-0000000094.
- Last Compass of Dawn — by Noah Murphy — published by Harbor Lane Books (Australia) — Children — 2012 — $19.97 — 175 pages — ISBN 978-0000000003.
- Last Empire of Dawn — by Omar Moreau — published by Maple Leaf Books (Canada) — Children — 2019 — $13.63 — 272 pages — ISBN 978-0000000117.
- Last Garden Returns — by Diego Haddad, Omar Murphy — published by Golden Fig Press (USA) — Children — 2022 — $38.16 — 140 pages — ISBN 978-0000000065.
- Last Garden of Dawn — by Ava Iyer — published by Owl and Oak (UK) — Children — 2023 — $28.25 — 596 pages — ISBN 978-0000000048.
- Last Harbor of Dawn — by Ava Okafor — published by Lotus Page (India) — Self-Help — 2004 — $26.79 — 128 pages — ISBN 978-0000000022.
- Last Kingdom — by Nina Kim — published by Maple Leaf Books (Canada) — Self-Help — 2021 — $38.21 — 596 pages — ISBN 978-0000000078.
- Last Kingdom Returns — by Omar Tanaka — published by Golden Fig Press (USA) — Mystery — 2002 — $7.49 — 461 pages — ISBN 978-0000000026.
- Last Letter — by Diego Murphy — published by Silver Pine Media (USA) — Mystery — 2023 — $33.38 — 162 pages — ISBN 978-0000000082.
- Last Letter of Dawn — by Zara Duarte, Maya Singh — published by Lotus Page (India) — Fiction — 1988 — $39.99 — 478 pages — ISBN 978-0000000075.
- Last Mountain — by Tariq Silva — published by Lotus Page (India) — Fiction — 2003 — $29.70 — 249 pages — ISBN 978-0000000103.
- Last River Returns — by Omar Moreau, Ava Iyer — published by Golden Fig Press (USA) — Fantasy — 2001 — $34.38 — 601 pages — ISBN 978-0000000074.
- Last Storm Returns — by Ava Iyer — published by Maple Leaf Books (Canada) — Self-Help — 2003 — $13.96 — 463 pages — ISBN 978-0000000061.
- Quiet Clock Returns — by Ava Singh — published by Northwind Publishing (Canada) — Children — 1985 — $38.04 — 425 pages — ISBN 978-0000000066.
- Quiet Compass — by Leo Brooks — published by Sunrise House (India) — Mystery — 2001 — $32.78 — 322 pages — ISBN 978-0000000116.
- Quiet Compass Returns — by Omar Singh — published by Lotus Page (India) — Romance — 2012 — $28.48 — 190 pages — ISBN 978-0000000083.
- Quiet Compass of Dawn — by Ava Larsen — published by Sunrise House (India) — Self-Help — 2002 — $20.81 — 149 pages — ISBN 978-0000000068.
- Quiet Empire of Dawn — by Nina Kim — published by Golden Fig Press (USA) — Romance — 1989 — $38.25 — 458 pages — ISBN 978-0000000043.
- Quiet Garden of Dawn — by Maya Kim — published by Red Kite Publishing (UK) — Children — 2002 — $21.72 — 197 pages — ISBN 978-0000000006.
- Quiet Harbor — by Maya Chen — published by Blue Lantern Press (USA) — Romance — 2011 — $33.95 — 228 pages — ISBN 978-0000000084.
- Quiet Harbor Returns — by Omar Duarte — published by Lotus Page (India) — Romance — 2014 — $20.13 — 331 pages — ISBN 978-0000000064.
- Quiet Kingdom — by Hana Haddad — published by Northwind Publishing (Canada) — Fiction — 2024 — $39.94 — 222 pages — ISBN 978-0000000019.
- Quiet Kingdom Returns — by Ava Iyer — published by Owl and Oak (UK) — Science — 2019 — $6.91 — 523 pages — ISBN 978-0000000070.
- Quiet Kingdom of Dawn — by Mei Reyes — published by Silver Pine Media (USA) — Science — 2014 — $16.74 — 194 pages — ISBN 978-0000000018.
- Quiet Letter — by Diego Haddad — published by Northwind Publishing (Canada) — Self-Help — 2006 — $12.26 — 172 pages — ISBN 978-0000000105.
- Quiet River Returns — by Maya Singh — published by Maple Leaf Books (Canada) — History — 2020 — $31.98 — 351 pages — ISBN 978-0000000109.
- Quiet River of Dawn — by Diego Keller — published by Northwind Publishing (Canada) — Self-Help — 2012 — $34.06 — 394 pages — ISBN 978-0000000087.
- Quiet Storm — by Aisha Iyer — published by Sunrise House (India) — History — 1997 — $24.22 — 263 pages — ISBN 978-0000000005.
- Quiet Storm of Dawn — by Nina Kim, Maya Singh — published by Golden Fig Press (USA) — Mystery — 1999 — $11.97 — 650 pages — ISBN 978-0000000055.
- Silent Clock Returns — by Mei Reyes — published by Silver Pine Media (USA) — Mystery — 2017 — $28.56 — 463 pages — ISBN 978-0000000050.
- Silent Compass of Dawn — by Lena Novak, Arjun Silva — published by Owl and Oak (UK) — Self-Help — 2017 — $20.50 — 576 pages — ISBN 978-0000000058.
- Silent Garden Returns — by Aisha Iyer, Nina Singh — published by Northwind Publishing (Canada) — Self-Help — 1998 — $23.37 — 293 pages — ISBN 978-0000000049.
- Silent Garden of Dawn — by Omar Moreau — published by Maple Leaf Books (Canada) — Fantasy — 1993 — $14.98 — 229 pages — ISBN 978-0000000023.
- Silent Harbor of Dawn — by Ava Walsh — published by Northwind Publishing (Canada) — Children — 2023 — $21.97 — 153 pages — ISBN 978-0000000114.
- Silent Kingdom — by Lena Novak — published by Owl and Oak (UK) — Fantasy — 2024 — $8.04 — 221 pages — ISBN 978-0000000111.
- Silent Kingdom Returns — by Hana Keller — published by Maple Leaf Books (Canada) — Romance — 2019 — $38.32 — 309 pages — ISBN 978-0000000099.
- Silent Kingdom of Dawn — by Hana Murphy — published by Golden Fig Press (USA) — Children — 2019 — $31.41 — 345 pages — ISBN 978-0000000067.
- Silent Letter — by Omar Singh — published by Red Kite Publishing (UK) — Science — 2021 — $38.26 — 207 pages — ISBN 978-0000000108.
- Silent Letter of Dawn — by Aisha Iyer — published by Lotus Page (India) — Romance — 1990 — $10.69 — 356 pages — ISBN 978-0000000062.
- Silent Mountain — by Diego Murphy — published by Red Kite Publishing (UK) — Children — 1998 — $8.17 — 537 pages — ISBN 978-0000000063.
- Silent River — by Maya Singh, Aisha Duarte — published by Golden Fig Press (USA) — Romance — 2003 — $24.84 — 316 pages — ISBN 978-0000000045.
- Silent River Returns — by Omar Singh — published by Red Kite Publishing (UK) — Science — 2011 — $6.83 — 460 pages — ISBN 978-0000000033.
- Silent Storm — by Mei Reyes — published by Harbor Lane Books (Australia) — Fiction — 1988 — $7.69 — 608 pages — ISBN 978-0000000012.
- Wild Clock — by Maya Singh — published by Sunrise House (India) — Children — 2002 — $11.40 — 230 pages — ISBN 978-0000000034.
- Wild Clock Returns — by Diego Murphy — published by Harbor Lane Books (Australia) — Children — 2010 — $30.61 — 598 pages — ISBN 978-0000000069.
- Wild Clock of Dawn — by Leo Brooks — published by Northwind Publishing (Canada) — Fantasy — 1992 — $33.94 — 530 pages — ISBN 978-0000000106.
- Wild Compass Returns — by Diego Keller, Kofi Murphy — published by Maple Leaf Books (Canada) — Fiction — 2012 — $10.60 — 592 pages — ISBN 978-0000000071.
- Wild Garden Returns — by Maya Kim — published by Silver Pine Media (USA) — History — 2017 — $22.60 — 172 pages — ISBN 978-0000000025.
- Wild Garden of Dawn — by Diego Murphy — published by Northwind Publishing (Canada) — History — 2011 — $12.46 — 219 pages — ISBN 978-0000000002.
- Wild Harbor — by Ava Okafor — published by Maple Leaf Books (Canada) — Self-Help — 1985 — $25.51 — 600 pages — ISBN 978-0000000104.
- Wild Harbor Returns — by Nina Singh — published by Sunrise House (India) — Mystery — 2003 — $13.72 — 303 pages — ISBN 978-0000000101.
- Wild Kingdom Returns — by Ravi Patel — published by Blue Lantern Press (USA) — Fantasy — 2012 — $6.05 — 321 pages — ISBN 978-0000000042.
- Wild Kingdom of Dawn — by Noah Murphy — published by Sunrise House (India) — Self-Help — 2019 — $10.49 — 604 pages — ISBN 978-0000000001.
- Wild Mountain of Dawn — by Aisha Iyer — published by Maple Leaf Books (Canada) — History — 2000 — $30.47 — 620 pages — ISBN 978-0000000093.
- Wild River — by Nina Singh, Hana Murphy — published by Maple Leaf Books (Canada) — Romance — 2000 — $18.55 — 281 pages — ISBN 978-0000000021.
- Wild River Returns — by Maya Chen — published by Blue Lantern Press (USA) — Fantasy — 2019 — $10.29 — 166 pages — ISBN 978-0000000102.
- Wild River of Dawn — by Zara Duarte — published by Silver Pine Media (USA) — Fantasy — 2001 — $13.83 — 317 pages — ISBN 978-0000000098.

## Best-selling books by copies sold

1. Last Storm Returns — 65 copies sold.
2. Crimson Storm of Dawn — 64 copies sold.
3. Hidden Compass — 64 copies sold.
4. Golden Kingdom Returns — 62 copies sold.
5. Silent Harbor of Dawn — 62 copies sold.
6. Broken Storm — 59 copies sold.
7. Crimson River of Dawn — 59 copies sold.
8. Crimson Empire of Dawn — 59 copies sold.
9. Crimson Garden of Dawn — 58 copies sold.
10. Silent Compass of Dawn — 58 copies sold.
11. Silent Storm — 56 copies sold.
12. Last Compass — 56 copies sold.
13. Wild River — 56 copies sold.
14. Silent Kingdom of Dawn — 55 copies sold.
15. Wild Garden of Dawn — 55 copies sold.
16. Broken Mountain — 55 copies sold.
17. Quiet River Returns — 55 copies sold.
18. Quiet Empire of Dawn — 55 copies sold.
19. Broken Letter of Dawn — 53 copies sold.
20. Last Empire of Dawn — 53 copies sold.

## Example questions the assistant can answer

- Which books were written by Ava Singh?
- Who publishes 'Wild Kingdom of Dawn' and what does it cost?
- Show me books in the Fantasy genre.
- Which publisher has the most titles?
- What is the average price of books from Blue Lantern Press?
- Which books are best sellers?
- Tell me about author Omar Duarte.
