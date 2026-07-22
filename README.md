# StackKart — E-Commerce Project

Django e-commerce store with a dark frontend, product catalog, cart API, order management, and Pakistan-ready payment options (JazzCash, EasyPaisa, COD).

## Tech Stack

- **Backend:** Django 5 + Django REST Framework
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Auth:** Django built-in authentication, Argon2 hashing
- **Frontend:** Django Templates + custom dark CSS/JS theme
- **Payments:** JazzCash / EasyPaisa placeholders + COD
- **Currency:** PKR

## Quick Start

```bash
cd stackkart-ecommerce
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Main Routes

| Route | Description |
|---|---|
| `/` | Homepage & product grid |
| `/products/<slug>/` | Product detail |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout page |
| `/accounts/login/` & `/accounts/register/` | Auth pages |
| `/admin/` | Django admin panel |
| `/api/v1/products/` | Products API |
| `/api/v1/cart/` | Cart API |
| `/api/docs/` | Swagger API docs |

## Project Apps

- `accounts` — User auth & customer profiles
- `catalog` — Products, categories, homepage
- `cart` — Cart & checkout logic
- `orders` — Order management
- `payments` — Payment records & gateways

## Deployment

For a student demo, deploy on **Railway** or **Render** with a PostgreSQL addon and Cloudinary for images. Set environment variables (`SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`) and run:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

For production: Ubuntu VPS + Gunicorn + Nginx + PostgreSQL + Redis + HTTPS via Let's Encrypt.
