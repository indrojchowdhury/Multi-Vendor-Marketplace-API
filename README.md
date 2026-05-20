# Multi-Vendor-Marketplace-API

This is a clean, modular, and scalable Multi-Vendor Marketplace API built with **Django REST Framework (DRF)**. It is designed following REST API principles and includes all the core features needed for a modern e-commerce backend.

---

## 📝 Project Summary

I built this multi-vendor marketplace API to handle different types of users (**Buyers and Sellers**) with secure permissions. The project includes full Product management, a dynamic Cart system, Order handling, secure Payment integration, and strong API security like Throttling. 

To keep the application fast and reliable, I designed a relational database structure with optimized model relationships using **MySQL**. Everything has been thoroughly tested and validated using **Postman** with **Bearer token authentication**.

---

## 🛠️ Tools & Tech Stack Used

* **Backend Framework:** Django & Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JSON Web Tokens)
* **Database:** MySQL (Relational Database with optimized relationships)
* **Search & Filters:** Django-Filter package
* **Payment Gateway:** SSLCommerz API
* **API Testing:** Postman

---

## 🚀 Key Features Implemented

### 1. User Authentication & Roles
* **JWT Authentication:** Secure login and session handling using Bearer tokens.
* **Role-Based Access Control:** Separate features and permissions for **Buyers** and **Sellers**.

### 2. Secure Product Management (CRUD)
* **Clean Endpoints:** Fixed URL trailing slash issues and mapped product list (GET) and creation (POST) to a single root path (`/api/products/`).
* **Owner Protection:** Added a custom `IsProductOwner` permission so a seller can **only** edit or delete their own products.

### 3. Cart & Order Handling
* **Cart System:** Keeps track of user selected items, quantity, and live product availability.
* **Order Management:** Handles the complete workflow from creating an order to processing checkouts.

### 4. Search, Filtering, & Pagination
* **Text Search:** Users can search products by name or description using `?search=Keyboard`.
* **Smart Filtering & Sorting:** Filters items exactly by stock levels and allows dynamic sorting by price or date.
* **Pagination:** Uses `PageNumberPagination` to split large data lists into clean pages with next/previous links.

### 5. API Security (Throttling)
* **Rate Limiting:** Added global `AnonRateThrottle` and `UserRateThrottle` to block bots or hackers from sending too many requests (prevents DDoS attacks).

### 6. Payment Integration
* **SSLCommerz:** Integrated the SSLCommerz payment gateway to handle secure digital payments and checkout validation.

---

## 👑 Core API Roadmap

| Module | Endpoint | Method | Access Control | Description |
| :--- | :--- | :---: | :--- | :--- |
| **Auth** | `/api/auth/register/` | POST | Public | Registers a new Buyer or Seller |
| | `/api/auth/login/` | POST | Public | Gets JWT Access & Refresh Tokens |
| **Products** | `/api/products/` | GET | Public | Lists all products *(With pagination, search, filters)* |
| | `/api/products/` | POST | Seller Only | Allows verified sellers to add new products |
| | `/api/products/update/<id>/` | PUT/PATCH | Seller + Owner | Updates a specific product |
| | `/api/products/delete/<id>/` | DELETE | Seller + Owner | Deletes a product from the database |
| **Payment** | `/api/payment/checkout/` | POST | Authenticated | Starts the SSLCommerz payment session |
