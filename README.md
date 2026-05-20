# Multi-Vendor Marketplace API

A scalable Multi-Vendor Marketplace API built with Django REST Framework (DRF). The project supports Buyers and Sellers with secure authentication, product management, cart handling, order processing, and payment integration by **Python, Django REST Framework (DRF), and MySQL**. Designed following REST API principles, it provides a complete backend solution for modern e-commerce platforms.

---

## 🚀 Features

- **JWT Authentication:** Secure user authentication and session handling using Bearer tokens (SimpleJWT).
- **Role-Based Access:** Dedicated features, workflows, and permissions for both **Buyers** and **Sellers**.
- **Product CRUD:** Standardized endpoints (`/api/products/`) with resolved trailing slash issues for seamless GET/POST requests.
- **Object Ownership:** Custom `IsProductOwner` permission ensuring sellers can only edit or delete their own products.
- **Cart & Orders:** Dynamic cart management tracking live availability and full order processing lifecycles.
- **Search & Filters:** Text search (`?search=`), exact stock filtering (`django-filter`), and dynamic sorting by price/date.
- **Pagination:** Structured API responses using `PageNumberPagination` with page counts and next/previous links.
- **API Security:** Global rate limiting using `AnonRateThrottle` and `UserRateThrottle` to prevent DDoS and brute-force attacks.
- **Payment Gateway:** Secure online payment processing and transaction handling via **SSLCommerz** integration.
- **API Testing:** Clean architectural structure fully tested and validated using **Postman**.

---

## 🛠️ Tech Stack

- **Backend Framework:** Python, Django, Django REST Framework (DRF)
- **Database:** MySQL
- **Tools & Packages:** SimpleJWT, Django-Filter, SSLCommerz SDK, Postman

---

## 🛣️ Core API Roadmap

| Module | Endpoint | Method | Access Control | Description |
| :--- | :--- | :---: | :--- | :--- |
| **Auth** | `/api/auth/register/` | POST | Public | Registers a new Buyer or Seller |
| | `/api/auth/login/` | POST | Public | Obtains JWT Access & Refresh Tokens |
| **Products** | `/api/products/` | GET | Public | Lists all products *(with pagination, search, filters)* |
| | `/api/products/` | POST | Seller Only | Allows verified sellers to add new products |
| | `/api/products/update/<id>/` | PUT/PATCH | Seller + Owner | Updates partial/full details of a specific product |
| | `/api/products/delete/<id>/` | DELETE | Seller + Owner | Permanently removes a product from the database |
| **Orders** | `/api/orders/` | POST | Buyer Only | Places a new order from cart items |
| | `/api/orders/` | GET | Buyer Only | Lists all orders placed by the current buyer |
| **Payment** | `/api/payment/checkout/` | POST | Authenticated | Initializes SSLCommerz payment session |
