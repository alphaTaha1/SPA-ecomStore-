const Database = require('better-sqlite3');

// This creates (or opens) a file named 'ecommerce.db' in your project root
const db = new Database('ecommerce.db');

// Enable Write-Ahead Logging (WAL) mode for better speed & concurrency
db.pragma('journal_mode = WAL');

// Create the tables if they don't already exist
db.exec(`
  CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category TEXT,
    stock INTEGER DEFAULT 10
  );
`);

console.log('✅ SQLite database connected and table created successfully!');

module.exports = db;