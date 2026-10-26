"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { apiRequest, formatPrice } from "../lib/api";

export default function ProductCatalogPage() {
  const [products, setProducts] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    let isCurrent = true;

    apiRequest("/api/products")
      .then((data) => {
        if (isCurrent) setProducts(data);
      })
      .catch((requestError) => {
        if (isCurrent) setError(requestError.message);
      });

    return () => {
      isCurrent = false;
    };
  }, []);

  return (
    <>
      <section className="page-heading">
        <p className="eyebrow">A little more considered</p>
        <h1>Easy Mart</h1>
        <p>
          Explore our Product catalog for useful, well-made things for everyday
          living. Find your next favorite below.
        </p>
      </section>

      <div className="toolbar">
        <h2 className="section-label">Popular Products</h2>
        <Link className="button" href="/products/new">
          Add a product
        </Link>
      </div>

      {error ? <p className="feedback feedback-error" role="alert">{error}</p> : null}
      {products === null && !error ? (
        <p className="loading-state" role="status">Loading products…</p>
      ) : null}
      {products?.length === 0 ? (
        <section className="empty-state">
          <h2>Your collection starts here</h2>
          <p>Add a product to see it in the catalog.</p>
          <Link className="button" href="/products/new">Create a product</Link>
        </section>
      ) : null}
      {products?.length > 0 ? (
        <section className="product-grid" aria-label="Products">
          {products.map((product) => (
            <article className="product-card" key={product.id}>
              <div className="product-art" aria-hidden="true">✳</div>
              <h2>{product.name}</h2>
              <p>{product.description || "A thoughtful find for your everyday."}</p>
              <div className="product-card-bottom">
                <span className="price">{formatPrice(product.price)}</span>
                <Link className="text-link" href="/orders/new">
                  Order item <span aria-hidden="true">→</span>
                </Link>
              </div>
            </article>
          ))}
        </section>
      ) : null}
    </>
  );
}
