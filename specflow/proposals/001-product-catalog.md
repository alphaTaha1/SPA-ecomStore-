# 001 — Product catalog API baseline

- **Status:** Proposal documenting the implemented baseline; future scope is
  not approved
- **Owner:** Product owner and engineering
- **Created:** 2026-10-14
- **Last refined:** 2026-10-14

This proposal captures the current product API as the first Specflow record.
The current-state sections describe implemented behavior. The roadmap's
proposed phases describe possible follow-up work and must be approved before
execution.

## 1. Intent

### Vision

Provide the first product-catalog capability for the e-commerce monolith:
create products and retrieve the catalog through an HTTP API.

### Goals

- Create a product and persist it to the application's SQLite database.
- List persisted products in stable ID order.
- Return a clear client error for a negative price.
- Keep the backend as one Flask application with controller, service, model,
  and utility layers.

### Constraints

- Python backend using Flask.
- Single deployable monolith; layers are internal modules, not services.
- SQLite persistence.
- Product fields currently represented by the API: `id`, `name`,
  `description`, `price`, and `stock`.
- Code changes follow the TDD gates in `agents.md`.

### Success criteria

| Criterion | Verification | Current result |
|---|---|---|
| Empty product catalog returns HTTP 200 and `[]` | `test_lists_no_products_when_store_is_empty` | Pass |
| Valid product creation returns HTTP 201 and the saved product fields | `test_creates_product_and_returns_created_product` | Pass |
| Negative price returns HTTP 400 | `test_rejects_product_with_negative_price` | Pass |
| Full current product API test suite passes | `.\.venv\Scripts\python.exe -m pytest -q` from the project directory | Pass: 3 tests |

### Non-goals

- Product updates or deletion.
- Product search, filtering, pagination, or categories.
- Authentication, authorization, carts, checkout, or order management.
- Claims that request validation beyond negative-price rejection is complete.

### Current state

The Flask app factory is `app.main.create_app`. It initializes a SQLite
`products` table and registers the product blueprint.

- `GET /api/products` returns a JSON array of products ordered by ID. With no
  products, it returns HTTP 200 and `[]`.
- `POST /api/products` reads JSON keys `name`, `description`, `price`, and
  `stock`, inserts the product, and returns HTTP 201 with `id` and those
  fields.
- A negative `price` returns HTTP 400 with
  `{"error": "price must be non-negative"}`. SQLite also has a non-negative
  price constraint.
- The database path defaults to `data/ecommerce.db` and can be overridden with
  app config key `DATABASE`.
- Current automated coverage is in `tests/test_product_api.py`; it verifies
  the three criteria above.

The API currently assumes a JSON object with all four creation fields and
does not yet define behavior for missing fields, invalid JSON, non-numeric
prices, negative stock, or blank names. These are gaps, not implied guarantees.

## 2. Roadmap

| Phase | Goal | Deliverables | Depends on | Status |
|---|---|---|---|---|
| 1. Product API baseline | Deliver the existing create/list behavior | Flask app factory, SQLite product table, product model/service/controller, three API tests | None | Implemented baseline |
| 2. Product input contract | Define and implement consistent validation/error responses for malformed or invalid creation requests | Approved field constraints, validation tests, structured 4xx responses | Phase 1; product-owner approval of constraints | Proposed |
| 3. Catalog retrieval contract | Decide and implement listing behavior for larger catalogs, including pagination and optional filters if required | Approved query parameters, response contract, tests | Phase 1; Phase 2 API conventions | Proposed |

Phases 2 and 3 are intentionally proposals only; no behavior or field policy
for them is approved by this document.

## 3. Tasks

| ID | Phase | Task | Owner | Inputs | Output | Depends on | Verification | Status |
|---|---|---|---|---|---|---|---|---|
| T-001 | 1 | Add app factory and SQLite product table | AI | Flask monolith constraint | `app.main`, database utility | None | App can initialize an isolated test database | Complete |
| T-002 | 1 | Add product listing endpoint | AI | Product table | `GET /api/products` | T-001 | Empty-list API test | Complete |
| T-003 | 1 | Add product creation endpoint | AI | Product model and SQLite table | `POST /api/products` | T-001 | Creation API test | Complete |
| T-004 | 1 | Reject negative prices | AI | Current product API | HTTP 400 for negative price | T-003 | Negative-price API test | Complete |
| T-005 | 2 | Agree creation-field constraints and error response format | Human | Current API behavior and documented gaps | Approved validation contract | None | Product-owner approval recorded here | Proposed |
| T-006 | 2 | Add one test per agreed invalid-input behavior and implement validation | AI | Approved T-005 contract | Validated creation endpoint | T-005 | Full pytest suite and new behavior tests | Proposed |
| T-007 | 3 | Decide whether catalog pagination/filtering is needed | Human | Catalog usage and expected product count | Approved listing contract or explicit deferral | None | Decision recorded here | Proposed |
| T-008 | 3 | Implement approved catalog query behavior | AI | Approved T-007 contract | Extended listing API | T-007 | Contract tests and full pytest suite | Proposed |

## 4. Execute

### Decisions

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-10-14 | Use Flask for the API | Requested Python/Flask backend | The app factory and route registration use Flask |
| 2026-10-14 | Keep the application monolithic and layered | Requested monolithic structure | Controllers, services, models, and utilities run in one app |
| 2026-10-14 | Use SQLite for product persistence | Existing implementation and no separate database service requested | Product storage uses a local SQLite database |
| 2026-10-14 | Expose product routes under `/api/products` | Initial product creation/listing API scope | Both create and list use the same resource path |

### Execution evidence

| Task | Files changed | Verification command | Actual result |
|---|---|---|---|
| T-001–T-004 | `app/`, `tests/test_product_api.py`, `requirements.txt` | `.\.venv\Scripts\python.exe -m pytest -q` | `3 passed` |

This evidence describes the existing implementation session. New work must
append fresh evidence rather than treating this row as proof for future tasks.

## 5. Refine

### Acceptance review

| Success criterion | Evidence | Result |
|---|---|---|
| Empty product catalog is listed successfully | `test_lists_no_products_when_store_is_empty` | Pass |
| Valid product can be created and returned | `test_creates_product_and_returns_created_product` | Pass |
| Negative price is rejected | `test_rejects_product_with_negative_price` | Pass |
| Entire current suite is green | Pytest output: `3 passed` | Pass |

### Gaps and follow-up

- Define required/optional fields, types, name/description length limits, and
  stock constraints before broadening input validation.
- Choose a stable error response contract for malformed or invalid requests.
- Decide whether product listing needs pagination, filtering, or sorting
  parameters beyond the existing ID ordering.
- The repository currently has no explicit approval recorded for proposed
  phases 2 and 3.

### Refinement decisions

- Preserve the implemented baseline as the reference behavior for proposal 001.
- Keep validation hardening and catalog enhancements proposed until their
  contracts are approved.

## Approval

- **Decision:** Baseline documented; proposed follow-up phases pending
- **Approver:** Not recorded
- **Date:** Not recorded
- **Notes:** This document records current behavior and does not authorize
  implementation of phases 2 or 3.
