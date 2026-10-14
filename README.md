# Ecommerce API

A monolithic Flask backend with SQLite storage for product creation and listing.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
flask --app app run
```

The app creates `products.db` in the current working directory by default.

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

## Tests

```powershell
python -m unittest discover -s tests -v
```
