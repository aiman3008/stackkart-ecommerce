# StackKart — Project Explanation

## Overview

StackKart is a Django-based e-commerce web application built as a final-year project. It features a dark storefront, product catalog, shopping cart, checkout flow, order management, and payment placeholders for PKR-based methods (Cash on Delivery, JazzCash, EasyPaisa).

## Tech Stack

- **Backend:** Python, Django 5, Django REST Framework
- **Frontend:** HTML, CSS, JavaScript, Django Templates
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Auth:** Django built-in authentication with Argon2 hashing
- **Payments:** JazzCash / EasyPaisa demo placeholders + COD

## Project Structure

```
stackkart-ecommerce/
├── accounts/     — User auth & customer profiles
├── cart/         — Cart & checkout logic
├── catalog/      — Products, categories, homepage
├── config/       — Django settings & URLs
├── orders/       — Order management
├── payments/     — Payment records & gateways
├── static/       — CSS, JS, images
├── templates/    — HTML templates
└── docs/         — Project documentation
```

## Features

**Customer:** Browse & search products, filter by category, add to cart, update quantities, checkout with delivery details, choose payment method (COD/JazzCash/EasyPaisa), view order confirmation.

**Admin:** Manage products/categories/orders, view customer profiles and carts, export orders as CSV, review payment records.

## Design

Custom dark theme with GitHub-inspired color palette:
- Background: `#0d1117`, Surface: `#161b22`, Accent: `#3fb950`
- Sticky navbar, product grid, floating category badges, live cart preview

## Key Models

- **CustomerProfile** — extends User with phone, address, city
- **Category** — name, slug, parent category
- **Product** — name, description, price, stock, image_url, category
- **Cart / CartItem** — supports both anonymous sessions and logged-in users
- **Order / OrderItem** — tracks status (pending → confirmed → shipped → delivered → cancelled)
- **PaymentRecord** — gateway, reference, amount, status

## API Endpoints

```
GET  /api/v1/products/       — List products
GET  /api/v1/categories/     — List categories
GET  /api/v1/cart/           — View cart
POST /api/v1/cart/add/       — Add to cart
PATCH/DELETE /api/v1/cart/item/<id>/  — Update/remove item
```

Swagger docs available at `/api/docs/`.

## How to Run

```bash
cd stackkart-ecommerce
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations && python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Limitations & Future Work

- JazzCash/EasyPaisa are demo placeholders — need real API integration
- Email verification and password reset not implemented
- Product image upload needs Cloudinary/S3 setup
- Future: wishlist, coupons, invoice PDF, admin analytics, Redis caching
