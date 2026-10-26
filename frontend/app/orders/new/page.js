"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiRequest, formatPrice } from "../../../lib/api";

export default function NewOrderPage() {
  const [products, setProducts] = useState(null);
  const [items, setItems] = useState([]);
  const [quantity, setQuantity] = useState("1");
  const [productId, setProductId] = useState("");
  const [order, setOrder] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    let isCurrent = true;

    apiRequest("/api/products")
      .then((data) => {
        if (isCurrent) {
          setProducts(data);
          setProductId(data.length ? String(data[0].id) : "");
        }
      })
      .catch((requestError) => {
        if (isCurrent) setError(requestError.message);
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  function addItem(event) {
    event.preventDefault();
    setError("");
    setOrder(null);
    const parsedProductId = Number(productId);
    const parsedQuantity = Number(quantity);

    if (!Number.isInteger(parsedProductId) || parsedProductId <= 0) {
      setError("Choose a product before adding it to the order.");
      return;
    }
    if (!Number.isInteger(parsedQuantity) || parsedQuantity <= 0) {
      setError("Quantity must be a positive whole number.");
      return;
    }

    setItems((currentItems) => [
      ...currentItems,
      { product_id: parsedProductId, quantity: parsedQuantity },
    ]);
  }

  async function submitOrder() {
    setError("");
    setIsSubmitting(true);

    try {
      const createdOrder = await apiRequest("/api/orders", {
        method: "POST",
        body: JSON.stringify({ items }),
      });
      setOrder(createdOrder);
      setItems([]);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSubmitting(false);
    }
  }

  const estimatedTotal = items.reduce((total, item) => {
    const product = products?.find((entry) => entry.id === item.product_id);
    return total + (product ? Number(product.price) * item.quantity : 0);
  }, 0);

  return (
    <>
      <section className="page-heading">
        <p className="eyebrow">Make it yours</p>
        <h1>Place an order</h1>
        <p>Choose products and quantities. Your final total is calculated by the store.</p>
      </section>

      {error ? <p className="feedback feedback-error" role="alert">{error}</p> : null}
      {products === null && !error ? (
        <p className="loading-state" role="status">Loading products…</p>
      ) : null}
      {products?.length === 0 ? (
        <section className="empty-state">
          <h2>Nothing to order just yet</h2>
          <p>Add a product to the collection before placing an order.</p>
          <Link className="button" href="/products/new">Create a product</Link>
        </section>
      ) : null}
      {products?.length > 0 ? (
        <div className="order-layout">
          <section className="panel">
            <form className="form-grid" onSubmit={addItem}>
              <div className="field">
                <label htmlFor="order-product">Product</label>
                <select
                  id="order-product"
                  value={productId}
                  onChange={(event) => setProductId(event.target.value)}
                >
                  {products.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name} — {formatPrice(product.price)}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="order-quantity">Quantity</label>
                <input
                  id="order-quantity"
                  type="number"
                  min="1"
                  step="1"
                  required
                  value={quantity}
                  onChange={(event) => setQuantity(event.target.value)}
                />
              </div>
              <button className="button button-secondary" type="submit">Add to order</button>
            </form>
          </section>

          <aside className="order-summary" aria-label="Order summary">
            <h2>Your order</h2>
            {items.length ? items.map((item, index) => {
              const product = products.find((entry) => entry.id === item.product_id);
              return (
                <div className="order-line" key={`${item.product_id}-${index}`}>
                  <span>
                    {product?.name ?? "Product"}
                    <small>Qty {item.quantity}</small>
                  </span>
                  <span>{formatPrice(Number(product?.price ?? 0) * item.quantity)}</span>
                </div>
              );
            }) : <p className="muted">Your order is empty. Add a product to begin.</p>}
            <div className="order-total">
              <span>Estimated total</span>
              <span>{formatPrice(estimatedTotal)}</span>
            </div>
            <p className="muted">The server calculates the final total using current prices.</p>
            <button
              className="button"
              type="button"
              disabled={!items.length || isSubmitting}
              onClick={submitOrder}
            >
              {isSubmitting ? "Placing order…" : "Place order"}
            </button>
          </aside>
        </div>
      ) : null}

      {order ? (
        <section className="panel" aria-live="polite">
          <p className="eyebrow">Order confirmed</p>
          <h2>Thanks for your order</h2>
          <p>Order #{order.id} · Total {formatPrice(order.total)}</p>
          <Link className="text-link" href="/">Return to products</Link>
        </section>
      ) : null}
    </>
  );
}
