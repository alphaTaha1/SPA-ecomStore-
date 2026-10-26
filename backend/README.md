# Ecommerce API

A monolithic Flask backend with SQLite storage for product creation, listing, and order placement.

The single Flask application is organized by responsibility:

- `models/` contains product and order table creation and database queries.
- `services/` contains product and order validation and business operations.
- `controllers/` contains the product and order HTTP endpoints.
- `utility/` contains shared SQLite connection and lifecycle helpers.
- `app.py` creates the Flask app and registers the controller.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run
```

The app creates `products.db` in the current working directory by default. Set `DATABASE_PATH` to use another SQLite file and `FRONTEND_ORIGIN` to configure the allowed browser origin; see [`.env.example`](.env.example).

`GET /health` returns `{"status":"ok"}` for service health checks. The Docker setup and run commands are documented in the [project README](../README.md).

## API

### Create a product

`POST /api/products`

Required JSON fields are `name` and `price`. `description` is optional and defaults to an empty string.

```json
{
  "name": "Desk Lamp",
  "description": "Adjustable",
  "price": 29.99
}
```

Successful response: `201 Created`

```json
{
  "id": 1,
  "name": "Desk Lamp",
  "description": "Adjustable",
  "price": 29.99
}
```

If the JSON body is not an object or is missing `name` or `price`, the endpoint returns `400 Bad Request` with an `error` field.

### List products

`GET /api/products`

Returns all products as a JSON array, ordered by ID. An empty product table returns an empty array.

### Place an order

`POST /api/orders`

Send a non-empty `items` array. Each item contains a positive integer `product_id` and `quantity`. The server looks up current product prices and calculates each subtotal and the order total; client-supplied prices are not accepted.

```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

Successful response: `201 Created`. Orders and their items are stored in SQLite.

```json
{
  "id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 29.99,
      "subtotal": 59.98
    }
  ],
  "total": 59.98
}
```

Invalid order input or an unknown product returns `400 Bad Request` with an `error` field.

## Tests

```powershell
python -m unittest discover -s tests -v
```
