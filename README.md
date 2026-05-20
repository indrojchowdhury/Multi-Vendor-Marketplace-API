# Multi-Vendor-Marketplace-API

A robust, enterprise-grade Multi-Vendor Marketplace Backend API built using **Django REST Framework (DRF)**. This platform features a scalable multi-vendor architecture, role-based access control, secure transaction lifecycles, and strictly optimized database relationships designed to maintain peak performance and data consistency.

---

## 📖 Project Overview

I built this multi-vendor marketplace API to deliver a clean, modular, and scalable backend architecture following strict **REST API principles**. The system handles everything from secure user onboarding with granular permissions to complete product lifecycles, real-time cart computations, secure checkouts, and system-wide security configurations. 

---

## 🛠️ Tech Stack & Core Tools Used

* **Core Framework:** Django 5.x & Django REST Framework (DRF)
* **Authentication:** SimpleJWT (JSON Web Tokens) & Bearer Token Mechanics
* **Database & ORM:** Relational Database (SQLite/PostgreSQL) with optimized Model Relationships
* **Filtering & Search:** Django-Filter Engine
* **Payment Gateway:** SSLCommerz Sandbox/Production SDK
* **API Testing & Validation:** Postman

---

## 🚀 Key Features Implemented

### 1. Authentication & Granular Access Control
* **JWT Authentication:** Implemented secure stateless session management via `rest_framework_simplejwt` using Bearer tokens.
* **Role-Based Access Control (RBAC):** Distinct workflows and granular permissions tailored specifically for different user types (Buyers & Sellers).

### 2. Secure Product Management (CRUD)
* **Unified Endpoints:** Standardized URL structure mapping both product listing and creation to a single clean root path (`/api/products/`).
* **Strict Object Ownership:** Custom `IsProductOwner` along with `IsSeller` permissions to ensure products can **only** be modified or deleted by the exact seller who created them.

### 3. Cart & Order Management Systems
* **Dynamic Cart Handling:** Scalable cart structure that tracks user selections, live availability, and price state consistency.
* **Order Lifecycle Handling:** End-to-end order processing from initiation to checkout validation.

### 4. Advanced API Search, Filtering, & Pagination
* **Partial Text Search:** Instantly query items across titles or descriptions using `SearchFilter` (`?search=Keyboard`).
* **Exact Matching & Sorting:** Filter items instantly based on stock attributes (`DjangoFilterBackend`) and sort dynamically by price or creation dates (`OrderingFilter`).
* **PageNumberPagination:** Structured responses with metadata records like total page counts, next, and previous links.

### 5. Enterprise Security & Rate Limiting
* **Global API Throttling:** Configured `AnonRateThrottle` and `UserRateThrottle` to mitigate brute-force and DDoS/Bot attacks by enforcing automated `429 Too Many Requests` limits.

### 6. Payment Integration
* **SSLCommerz Integration:** Integrated Bangladesh's leading payment gateway to securely manage checkouts, digital payments, and verification transactions.

---

## 📐 Architecture & Database Design

* **Relational Database Consistency:** Designed clean, normalized tables with carefully structured foreign keys and relationships to avoid data redundancy and maintain absolute consistency.
* **REST Best Practices:** Followed industry-standard modular structures for URLs, Views, and Serializers to ensure the codebase remains maintainable for large teams.

---

## 🛣️ Core API Roadmap

| Module | Endpoint | Method | Access Control | Description |
| :--- | :--- | :---: | :--- | :--- |
| **Auth** | `/api/auth/register/` | POST | Public | Registers a new Buyer or Seller |
| | `/api/auth/login/` | POST | Public | Obtains JWT Access & Refresh Tokens |
| **Products** | `/api/products/` | GET | Public | Lists all products *(Supports pagination, search, filters)* |
| | `/api/products/` | POST | Seller Only | Creates a new product into the marketplace |
| | `/api/products/update/<id>/` | PUT/PATCH | Seller + Owner | Updates details of a specific product |
| | `/api/products/delete/<id>/` | DELETE | Seller + Owner | Permanently removes a product from the database |
| **Payment** | `/api/payment/checkout/` | POST | Authenticated | Initializes SSLCommerz payment session |

---

## 💻 Local Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/Multi-Vendor-Marketplace-API.git](https://github.com/your-username/Multi-Vendor-Marketplace-API.git)
   cd Multi-Vendor-Marketplace-API
