
# Medication Reference API

A small REST API built with **FastAPI** that serves a reference list of medications
and lets you search, filter, and look them up by their PZN (Pharmazentralnummer —
the German central pharmaceutical number).

Built as a learning project to practice FastAPI routing, Pydantic response models,
path/query parameters, and route ordering.

---

## Features

- List all medications
- Look up a single medication by its PZN
- Full-text search across medication name and active ingredient
- Filter by dosage form and/or prescription status
- Aggregate statistics: count of medications per dosage form
- Auto-generated interactive documentation via Swagger UI and ReDoc

---

## Tech Stack

- **Python 3.9+**
- **FastAPI** — web framework
- **Pydantic** — data validation and response models
- **Uvicorn** — ASGI server

---

## Project Structure

```
medication-reference-api/
├── main.py                 # FastAPI application and all route definitions
├── Medications_data.py     # In-memory medication dataset (MEDICATIONS list)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Files Git should ignore
└── LICENSE                 # (optional) license for your code
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/medication-reference-api.git
cd medication-reference-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

---

## Data Model

Each medication is validated against the `Med_fix` Pydantic model:

| Field                | Type            | Description                                      |
|----------------------|-----------------|--------------------------------------------------|
| `pzn`                | `str`           | Central pharmaceutical number (unique ID)        |
| `name`               | `str`           | Product name                                     |
| `active_ingredient`  | `str`           | Active pharmaceutical ingredient                 |
| `dosage_from`        | `str`           | Dosage form (e.g. `tablet`, `IV`)                |
| `strength`           | `str`           | Strength (e.g. `400mg`)                          |
| `prescription_only`  | `bool` (optional) | Whether the medication is prescription-only    |

> **Note:** the field is currently named `dosage_from`. This is a typo for
> `dosage_form` ("form" as in tablet/IV/capsule). It works, but consider renaming
> it consistently across the model, the dataset, and the routes.

---

## API Endpoints

### `GET /`

Welcome message.

**Response**
```json
"Welcome to Medication Reference API"
```

---

### `GET /medications`

Returns the full list of medications.

**Example**
```
http://localhost:8000/medications
```

---

### `GET /medications/query`

Filter medications by dosage form and/or prescription status. Both query
parameters are optional.

**Query parameters**

| Parameter           | Type   | Required | Description                              |
|---------------------|--------|----------|------------------------------------------|
| `dosage_from`       | string | No       | Dosage form to filter by                 |
| `prescription_only` | bool   | No       | `true` / `false` prescription filter     |

**Examples**
```
http://localhost:8000/medications/query
http://localhost:8000/medications/query?dosage_from=tablet
http://localhost:8000/medications/query?prescription_only=false
http://localhost:8000/medications/query?dosage_from=tablet&prescription_only=false
```

> **Known limitation:** the filters do not currently stack. If both parameters
> are supplied, only `prescription_only` is applied (it is evaluated last).
> Also, `dosage_from` matching is case-sensitive on the stored value, so
> `?dosage_from=iv` will not match the stored value `IV`.

---

### `GET /medications/search`

Case-insensitive substring search across `name` and `active_ingredient`.

**Query parameters**

| Parameter | Type   | Required | Description        |
|-----------|--------|----------|--------------------|
| `q`       | string | Yes      | Search term        |

**Example**
```
http://localhost:8000/medications/search?q=ibuprofen
```

---

### `GET /medications/{pzn}`

Look up a single medication by its PZN. Returns `404` if not found.

**Path parameter**

| Parameter | Type   | Description                    |
|-----------|--------|-------------------------------|
| `pzn`     | string | The medication's PZN          |

**Example**
```
http://localhost:8000/medications/03041347
```

**Not found response** (`404`)
```json
{ "detail": "Medication Not Found" }
```

---

### `GET /medications_dosage_from`

Returns a count of medications grouped by dosage form.

**Example**
```
http://localhost:8000/medications_dosage_from
```

**Response**
```json
{
  "tablet": 2,
  "IV": 1
}
```

---

## Important: Route Ordering

FastAPI matches routes **top-to-bottom** and uses the first match. The literal
routes `/medications/query` and `/medications/search` **must be declared before**
the dynamic route `/medications/{pzn}`. Otherwise `query` and `search` get
captured as if they were a `pzn` value. This ordering is already handled correctly
in `main.py` — keep it that way when adding new routes.

**Rule of thumb:** specific/literal paths before parameterized (`/{...}`) paths.

---

## Possible Improvements

- Rename `dosage_from` → `dosage_form` consistently
- Make `/medications/query` filters stack (narrow progressively instead of reassigning)
- Normalize case on both sides when matching `dosage_from`
- Correct data typos (`Iburofen` → Ibuprofen, `Amocicillin` → Amoxicillin)
- Move the dataset to a real database (e.g. SQLite + SQLAlchemy)
- Add automated tests (pytest + httpx)

---

## License

Specify a license here (e.g. MIT). See `LICENSE`.
