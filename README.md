# Mixed Store — Flask Edition

A static HTML store converted to a Python/Flask web app.
The UI is **identical** to the original; Flask now powers all data and form logic.

---

## Project Structure

```
flask-mixed-store/
├── app.py                  ← Flask application (routes + API)
├── requirements.txt        ← Python dependencies (Flask + Gunicorn)
├── Procfile                ← Tells Railway how to start the app
├── runtime.txt             ← Pins the Python version
├── .gitignore               ← Excludes venv, __pycache__, .env, etc.
├── templates/
│   ├── base.html           ← Shared navbar, chat widget, scripts
│   ├── index.html          ← Home page
│   ├── products.html       ← Products page
│   ├── cart.html           ← Cart page
│   └── contact.html        ← Contact page
└── static/
    ├── css/style.css
    ├── js/
    │   ├── theme.js
    │   ├── navbar.js
    │   └── cart.js
    └── images/             ← All product images
```

---

## Setup & Run (Local)

```bash
# 1. Enter the project folder
cd flask-mixed-store

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the dev server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To run it the way production will (via Gunicorn):

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

---

## Deploying to Railway

### 1. Push to GitHub

```bash
cd flask-mixed-store
git init
git add .
git commit -m "Initial commit — Flask Mixed Store"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Deploy on Railway

1. Go to [railway.app](https://railway.app) and sign in with GitHub.
2. Click **New Project → Deploy from GitHub repo**.
3. Select this repository.
4. Railway auto-detects Python via `runtime.txt`, installs `requirements.txt`,
   and starts the app using the `Procfile` (`gunicorn app:app`).
5. Railway injects a `$PORT` environment variable automatically — `app.py`
   already reads it (`os.environ.get("PORT", 5000)`), so no config changes
   are needed.
6. Once deployed, click **Generate Domain** under the service's **Settings →
   Networking** tab to get a public URL.

### 3. Redeploying after changes

Just push to `main` — Railway auto-redeploys on every push:

```bash
git add .
git commit -m "Update something"
git push
```

### Files Railway uses

| File | Role |
|------|------|
| `requirements.txt` | Tells Railway which Python packages to install |
| `Procfile` | Tells Railway the start command (`gunicorn app:app`) |
| `runtime.txt` | Pins the Python version Railway provisions |
| `app.py` | Reads `PORT` from env and binds to `0.0.0.0` — required for Railway |

---

## REST API Endpoints

| Method | Endpoint        | Description                          |
|--------|-----------------|--------------------------------------|
| GET    | `/api/products` | Returns all products as JSON         |
| POST   | `/api/contact`  | Saves a contact-form submission      |
| POST   | `/api/chat`     | Receives a chat message, returns bot reply |
| POST   | `/api/order`    | Places an order, logs it server-side |
| GET    | `/api/orders`   | Lists all placed orders (debug)      |
| GET    | `/api/messages` | Lists all contact messages (debug)   |

### Example — Place an order

```bash
curl -X POST http://127.0.0.1:5000/api/order \
  -H "Content-Type: application/json" \
  -d '{"items": [{"id":1,"name":"Shoes","price":999}]}'
```

---

## What Changed vs the Original

| Feature          | Before (static) | After (Flask)                     |
|------------------|-----------------|-----------------------------------|
| Page routing     | `.html` files   | Flask routes (`/`, `/products` …) |
| Product data     | Hardcoded in JS | Served by `/api/products`         |
| Contact form     | `alert()` only  | POST to `/api/contact`, saved     |
| Order Now        | `alert()` only  | POST to `/api/order`, logged      |
| Support chat     | Frontend only   | POST to `/api/chat`, bot replies  |
| Template sharing | Duplicated HTML | Jinja2 `base.html` inheritance    |

> **Note:** Cart state still uses `localStorage` so it persists across page
> navigations without a database. Orders are logged in-memory and printed to
> the terminal; swap `ORDERS` / `MESSAGES` lists for a database to make them
> permanent.
