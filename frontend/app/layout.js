import "./globals.css";

import Link from "next/link";

export const metadata = {
  title: "Easy Mart",
  description: "Everyday essentials, made easy.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <Link className="brand" href="/">
            <span className="brand-mark" aria-hidden="true">
              E
            </span>
            <span>Easy Mart</span>
          </Link>
          <div className="site-header-actions">
            <Link className="button site-home-button" href="/">Home</Link>
            <nav className="site-nav" aria-label="Main navigation">
              <details className="nav-menu">
                <summary>Menu</summary>
                <div className="nav-menu-list">
                  <Link href="/">Home</Link>
                  <Link href="/products/new">Add product</Link>
                  <Link href="/orders/new">Place order</Link>
                </div>
              </details>
            </nav>
          </div>
        </header>
        <main className="page-shell">{children}</main>
        <footer className="site-footer">
          <span>Everyday essentials, made easy.</span>
          <span>Easy Mart</span>
        </footer>
      </body>
    </html>
  );
}
