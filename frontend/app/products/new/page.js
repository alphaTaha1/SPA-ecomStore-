"use client";

import Link from "next/link";
import { useState } from "react";

import { apiRequest, formatPrice } from "../../../lib/api";

export default function NewProductPage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [createdProduct, setCreatedProduct] = useState(null);
  const [error, setError] = useState("");
  const [isSaving, setIsSaving] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setCreatedProduct(null);
    setIsSaving(true);

    try {
      const product = await apiRequest("/api/products", {
        method: "POST",
        body: JSON.stringify({ name, description, price: Number(price) }),
      });
      setCreatedProduct(product);
      setName("");
      setDescription("");
      setPrice("");
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setIsSaving(false);
    }
  }

  return (
    <>
      <section className="page-heading">
        <p className="eyebrow">Grow the collection</p>
        <h1>Create a product</h1>
        <p>Add a new item to your catalog. It will be ready to order as soon as it is saved.</p>
      </section>

      <section className="panel">
        <form className="form-grid" onSubmit={handleSubmit}>
          <div className="field">
            <label htmlFor="product-name">Product name</label>
            <input
              id="product-name"
              name="name"
              autoComplete="off"
              maxLength={120}
              placeholder="e.g. Everyday Ceramic Mug"
              required
              value={name}
              onChange={(event) => setName(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="product-description">Description</label>
            <textarea
              id="product-description"
              name="description"
              maxLength={1000}
              placeholder="A few details about this product"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="product-price">Price (USD)</label>
            <input
              id="product-price"
              name="price"
              type="number"
              min="0.01"
              step="0.01"
              placeholder="0.00"
              required
              value={price}
              onChange={(event) => setPrice(event.target.value)}
            />
          </div>
          {error ? <p className="feedback feedback-error" role="alert">{error}</p> : null}
          {createdProduct ? (
            <p className="feedback feedback-success" role="status">
              {createdProduct.name} was added at {formatPrice(createdProduct.price)}.
            </p>
          ) : null}
          <div className="form-actions">
            <button className="button" type="submit" disabled={isSaving}>
              {isSaving ? "Saving…" : "Create product"}
            </button>
            <Link className="text-link" href="/">Back to products</Link>
          </div>
        </form>
      </section>
    </>
  );
}
