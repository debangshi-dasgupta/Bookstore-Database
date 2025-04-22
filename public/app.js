const state = {
  view: "dashboard",
  metaLoaded: false,
  statusesLoaded: false,
  meta: { genres: [], publishers: [] },
};

const titles = {
  dashboard: "Dashboard",
  books: "Books",
  authors: "Authors",
  publishers: "Publishers",
  customers: "Customers",
  orders: "Orders",
  analytics: "Analytics",
};

const $ = (sel) => document.querySelector(sel);

const money = (n) =>
  "$" +
  Number(n || 0).toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

const num = (n) => Number(n || 0).toLocaleString("en-US");

const esc = (v) =>
  String(v === null || v === undefined ? "" : v)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");

function debounce(fn, delay = 300) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

async function api(path) {
  const [rawPath, query = ""] = path.split("?");
  const route = rawPath.replace(/^\/api\/?/, "");
  const url = `/api?route=${encodeURIComponent(route)}${query ? "&" + query : ""}`;
  const res = await fetch(url);
  const contentType = res.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    throw new Error(
      `The API returned a non-JSON response (HTTP ${res.status}). ` +
        "Make sure DATABASE_URL is set in the Vercel project environment variables."
    );
  }
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

function showError(msg) {
  const el = $("#error-banner");
  if (!msg) {
    el.classList.add("hidden");
    return;
  }
  el.textContent = msg;
  el.classList.remove("hidden");
}

function table(rows, columns, emptyText = "No records found.") {
  if (!rows || !rows.length) return `<div class="empty">${emptyText}</div>`;
  const head = columns.map((c) => `<th class="${c.align || ""}">${esc(c.label)}</th>`).join("");
  const body = rows
    .map((row) => {
      const cells = columns
        .map((c) => {
          const value = c.render ? c.render(row) : esc(row[c.key]);
          return `<td class="${c.align || ""}">${value}</td>`;
        })
        .join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");
  return `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function barList(rows, labelKey, valueKey, formatter = money) {
  if (!rows || !rows.length) return `<div class="empty">No data.</div>`;
  const max = Math.max(...rows.map((r) => Number(r[valueKey]) || 0), 1);
  return rows
    .map((r) => {
      const value = Number(r[valueKey]) || 0;
      const pct = Math.max((value / max) * 100, 2);
      return `
        <div class="bar-row">
          <div class="bar-head">
            <span>${esc(r[labelKey])}</span>
            <span class="muted">${formatter(value)}</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${pct}%"></div></div>
        </div>`;
    })
    .join("");
}

function statCards(container, items) {
  $(container).innerHTML = items
    .map(
      (i) => `
      <div class="stat">
        <div class="label">${esc(i.label)}</div>
        <div class="value ${i.neutral ? "neutral" : ""}">${i.value}</div>
      </div>`
    )
    .join("");
}

/* ---------------- Dashboard ---------------- */
async function loadDashboard() {
  showError("");
  const data = await api("/api/dashboard");
  statCards("#stat-cards", [
    { label: "Total revenue", value: money(data.revenue) },
    { label: "Books", value: num(data.counts.books) },
    { label: "Authors", value: num(data.counts.authors) },
    { label: "Publishers", value: num(data.counts.publishers) },
    { label: "Customers", value: num(data.counts.customers) },
    { label: "Orders", value: num(data.counts.orders) },
  ]);

  $("#dash-top-books").innerHTML = barList(
    data.top_books,
    "title",
    "revenue"
  );

  const maxStatus = Math.max(...data.status.map((s) => Number(s.count)), 1);
  $("#dash-status").innerHTML = data.status
    .map(
      (s) => `
      <div class="bar-row">
        <div class="bar-head">
          <span><span class="badge ${esc(s.status)}">${esc(s.status)}</span></span>
          <span class="muted">${num(s.count)} orders</span>
        </div>
        <div class="bar-track"><div class="bar-fill" style="width:${(s.count / maxStatus) * 100}%"></div></div>
      </div>`
    )
    .join("");

  $("#dash-recent").innerHTML = table(
    data.recent_orders,
    [
      { label: "Order", key: "order_id" },
      { label: "Customer", key: "customer" },
      { label: "Date", key: "order_date" },
      { label: "Status", render: (r) => `<span class="badge ${esc(r.status)}">${esc(r.status)}</span>` },
      { label: "Total", align: "num", render: (r) => money(r.total) },
    ],
    "No orders yet."
  );
}

/* ---------------- Books ---------------- */
async function loadMeta() {
  if (state.metaLoaded) return;
  const meta = await api("/api/books/meta");
  state.meta = meta;
  $("#book-genre").innerHTML =
    `<option value="">All genres</option>` +
    meta.genres.map((g) => `<option value="${esc(g)}">${esc(g)}</option>`).join("");
  state.metaLoaded = true;
}

async function loadBooks() {
  showError("");
  await loadMeta();
  const search = encodeURIComponent($("#book-search").value.trim());
  const genre = encodeURIComponent($("#book-genre").value);
  const rows = await api(`/api/books?search=${search}&genre=${genre}`);
  $("#books-table").innerHTML = table(
    rows,
    [
      { label: "#", key: "book_id" },
      { label: "Title", render: (r) => `<strong>${esc(r.title)}</strong>` },
      { label: "Authors", key: "authors" },
      { label: "Genre", render: (r) => `<span class="badge">${esc(r.genre || "—")}</span>` },
      { label: "Publisher", key: "publisher" },
      { label: "Year", key: "publish_year" },
      { label: "Pages", align: "num", render: (r) => num(r.pages) },
      { label: "Price", align: "num", render: (r) => money(r.price) },
    ],
    "No books match your search."
  );
}

/* ---------------- Authors ---------------- */
async function loadAuthors() {
  showError("");
  const search = encodeURIComponent($("#author-search").value.trim());
  const rows = await api(`/api/authors?search=${search}`);
  $("#authors-table").innerHTML = table(
    rows,
    [
      { label: "#", key: "author_id" },
      { label: "Name", render: (r) => `<strong>${esc(r.first_name)} ${esc(r.last_name)}</strong>` },
      { label: "Country", key: "country" },
      { label: "Birth year", key: "birth_year" },
      { label: "Books", align: "num", key: "book_count" },
    ],
    "No authors found."
  );
}

/* ---------------- Publishers ---------------- */
async function loadPublishers() {
  showError("");
  const rows = await api("/api/publishers");
  $("#publishers-table").innerHTML = table(
    rows,
    [
      { label: "#", key: "publisher_id" },
      { label: "Publisher", render: (r) => `<strong>${esc(r.name)}</strong>` },
      { label: "Country", key: "country" },
      { label: "Books", align: "num", key: "book_count" },
      { label: "Avg. price", align: "num", render: (r) => money(r.avg_price) },
    ],
    "No publishers found."
  );
}

/* ---------------- Customers ---------------- */
async function loadCustomers() {
  showError("");
  const search = encodeURIComponent($("#customer-search").value.trim());
  const rows = await api(`/api/customers?search=${search}`);
  $("#customers-table").innerHTML = table(
    rows,
    [
      { label: "#", key: "customer_id" },
      { label: "Name", render: (r) => `<strong>${esc(r.first_name)} ${esc(r.last_name)}</strong>` },
      { label: "Email", key: "email" },
      { label: "City", key: "city" },
      { label: "State", key: "state" },
      { label: "Signed up", key: "signup_date" },
      { label: "Orders", align: "num", key: "order_count" },
      { label: "Spent", align: "num", render: (r) => money(r.total_spent) },
      {
        label: "",
        render: (r) =>
          r.order_count > 0
            ? `<button class="btn" style="padding:5px 10px;font-size:12px" onclick="viewCustomerOrders(${r.customer_id}, '${esc(
                r.first_name
              )} ${esc(r.last_name)}')">Orders</button>`
            : "",
      },
    ],
    "No customers found."
  );
}

window.viewCustomerOrders = async function (id, name) {
  try {
    const rows = await api(`/api/customers/orders?customer_id=${id}`);
    $("#modal-title").textContent = `Orders — ${name}`;
    $("#modal-body").innerHTML = table(
      rows,
      [
        { label: "Order", key: "order_id" },
        { label: "Date", key: "order_date" },
        { label: "Status", render: (r) => `<span class="badge ${esc(r.status)}">${esc(r.status)}</span>` },
        { label: "Copies", align: "num", key: "copies" },
        { label: "Total", align: "num", render: (r) => money(r.total) },
      ],
      "This customer has no orders."
    );
    $("#modal").classList.remove("hidden");
  } catch (e) {
    showError(e.message);
  }
};

/* ---------------- Orders ---------------- */
async function loadStatuses() {
  if (state.statusesLoaded) return;
  const list = await api("/api/order-statuses");
  $("#order-status").innerHTML =
    `<option value="">All statuses</option>` +
    list.map((s) => `<option value="${esc(s)}">${esc(s)}</option>`).join("");
  state.statusesLoaded = true;
}

async function loadOrders() {
  showError("");
  await loadStatuses();
  const search = encodeURIComponent($("#order-search").value.trim());
  const status = encodeURIComponent($("#order-status").value);
  const rows = await api(`/api/orders?search=${search}&status=${status}`);
  $("#orders-table").innerHTML = table(
    rows,
    [
      { label: "#", key: "order_id" },
      { label: "Customer", render: (r) => `<strong>${esc(r.customer)}</strong>` },
      { label: "Date", key: "order_date" },
      { label: "Status", render: (r) => `<span class="badge ${esc(r.status)}">${esc(r.status)}</span>` },
      { label: "Items", align: "num", key: "item_count" },
      { label: "Copies", align: "num", key: "copies" },
      { label: "Total", align: "num", render: (r) => money(r.total) },
    ],
    "No orders match your filters."
  );
}

/* ---------------- Analytics ---------------- */
async function loadAnalytics() {
  showError("");
  const data = await api("/api/analytics");
  const avg = data.avg_order_value ? data.avg_order_value.avg_order_value : 0;
  const author = data.top_author ? data.top_author.author : "—";

  statCards("#analytics-cards", [
    { label: "Avg. order value", value: money(avg) },
    { label: "Top author", value: esc(author), neutral: true },
    { label: "Genres", value: num(data.genre_revenue.length) },
    { label: "Publishers", value: num(data.publisher_revenue.length) },
  ]);

  $("#an-months").innerHTML = barList(data.revenue_by_month, "month", "revenue");
  $("#an-genres").innerHTML = barList(data.genre_revenue, "genre", "revenue");
  $("#an-top-revenue").innerHTML = barList(data.top_books_revenue, "title", "revenue");
  $("#an-top-copies").innerHTML = barList(
    data.top_books_copies,
    "title",
    "copies",
    (v) => num(v) + " copies"
  );
  $("#an-customers").innerHTML = barList(data.top_customers, "customer", "total_spent");
  $("#an-publishers").innerHTML = barList(data.publisher_revenue, "publisher", "revenue");
}

/* ---------------- Navigation ---------------- */
const loaders = {
  dashboard: loadDashboard,
  books: loadBooks,
  authors: loadAuthors,
  publishers: loadPublishers,
  customers: loadCustomers,
  orders: loadOrders,
  analytics: loadAnalytics,
};

async function switchView(view) {
  state.view = view;
  document.querySelectorAll(".nav-btn").forEach((b) =>
    b.classList.toggle("active", b.dataset.view === view)
  );
  document.querySelectorAll(".view").forEach((v) =>
    v.classList.toggle("hidden", v.id !== "view-" + view)
  );
  $("#page-title").textContent = titles[view];
  try {
    await loaders[view]();
    $("#status-pill").textContent = "Connected";
    $("#status-pill").classList.remove("offline");
  } catch (e) {
    showError(e.message);
    $("#status-pill").textContent = "Connection error";
    $("#status-pill").classList.add("offline");
  }
}

document.querySelectorAll(".nav-btn").forEach((btn) => {
  btn.addEventListener("click", () => switchView(btn.dataset.view));
});

$("#book-search").addEventListener("input", debounce(loadBooks));
$("#book-genre").addEventListener("change", loadBooks);
$("#book-refresh").addEventListener("click", loadBooks);
$("#author-search").addEventListener("input", debounce(loadAuthors));
$("#customer-search").addEventListener("input", debounce(loadCustomers));
$("#order-search").addEventListener("input", debounce(loadOrders));
$("#order-status").addEventListener("change", loadOrders);

$("#modal-close").addEventListener("click", () => $("#modal").classList.add("hidden"));
$("#modal").addEventListener("click", (e) => {
  if (e.target.id === "modal") $("#modal").classList.add("hidden");
});

switchView("dashboard");
