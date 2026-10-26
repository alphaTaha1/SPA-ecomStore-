import assert from "node:assert/strict";
import test from "node:test";

const baseUrl = process.env.FRONTEND_URL ?? "http://127.0.0.1:3000";

test("the home page presents the Easy Mart store heading", async () => {
  const response = await fetch(baseUrl);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /<h1[^>]*>Easy Mart<\/h1>/);
});

test("the shared navigation exposes home and every route in a menu", async () => {
  const response = await fetch(baseUrl);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /<summary[^>]*>Menu<\/summary>/);
  assert.match(html, /<a href="\/">Home<\/a>/);
  assert.match(html, /<a href="\/products\/new">Add product<\/a>/);
  assert.match(html, /<a href="\/orders\/new">Place order<\/a>/);
  assert.match(html, /class="brand"[^>]*>[\s\S]*?Easy Mart/);
});

test("the home page introduces its popular products section", async () => {
  const response = await fetch(baseUrl);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /<h2[^>]*>Popular Products<\/h2>/);
});

test("the home page offers product pictures and add-to-cart actions", async () => {
  const response = await fetch(baseUrl);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /<img[^>]+alt="Chair"/);
  assert.match(html, /<h3[^>]*>Chair<\/h3>/);
  assert.match(html, /Add to cart/);
});

test("the home page presents the product catalog", async () => {
  const response = await fetch(baseUrl);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /Product catalog/);
});

test("the product creation page is available", async () => {
  const response = await fetch(`${baseUrl}/products/new`);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /Create a product/);
});

test("the order placement page is available", async () => {
  const response = await fetch(`${baseUrl}/orders/new`);
  const html = await response.text();

  assert.equal(response.status, 200);
  assert.match(html, /Place an order/);
});
