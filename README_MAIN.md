# 💸 FinTrack API – Python Powered Finance System

> A smart, high-performance financial tracking backend. Built with Python and FastAPI, this API does the heavy lifting of managing user roles, securely storing transactions, and automatically crunching the numbers for real-time financial summaries.

Welcome to **FinTrack API**! 🚀 This project provides a clean, robust set of REST API endpoints designed to power budgeting apps, expense trackers, or personal finance dashboards. Rather than dealing with messy spreadsheets, FinTrack securely authenticates users, tracks income and expenses, and generates dynamic analytics—all governed by a strict role-based access hierarchy.

---

## 🏗️ Tech Stack

- **FastAPI**: Blazing fast web framework with auto-generated API documentation.
- **SQLAlchemy & SQLite**: Reliable database ORM mapped to a lightweight, file-based database.
- **python-jose**: Secure JWT (JSON Web Token) creation and validation.
- **Passlib + bcrypt**: Industry-standard password hashing.
- **Pydantic**: Strict data validation for all inputs and outputs.
- **Pytest**: Comprehensive automated test suite ensuring everything runs perfectly.

---

## 🚀 Quick Setup & Installation

Ready to get it running? You just need Python 3.10+ installed on your machine.

**1. Clone & Navigate to the project directory:**
```bash
git clone <your-repo-link>
cd "Python Powered FinTech"
```

**2. Create & Activate a virtual environment:**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

**3. Install dependencies & Seed the database:**
```bash
pip install -r requirements.txt
python seed_data.py
```
*(The seeder creates your database tables and populates them with sample users and transactions so you can start testing immediately!)*

**4. Start the server!**
```bash
uvicorn app.main:app --reload
```
🎉 Your API is now live at: **http://127.0.0.1:8000**

---

## 📖 Interactive API Documentation

FastAPI automatically generates a beautiful GUI for you to test your endpoints without needing a frontend app. Once your server is running, visit:

- **Swagger UI (Interactive API Explorer):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc (Alternative Docs):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Authentication & Seeded Accounts

The API is secured using **JWT Bearer tokens**. When testing in Swagger UI, click the "Authorize" button and log in. Every subsequent request will automatically use your access token!

If you ran `seed_data.py`, you can log in with any of these sample accounts:

| Username | Password | Role | What they can do |
|---|---|---|---|
| `admin` | `Admin@123` | **Admin** | Can do everything, including creating/deleting any transactions and managing users. |
| `analyst` | `Analyst@123` | **Analyst** | Has full read-access to all financial data and advanced analytics, but cannot edit. |
| `viewer` | `Viewer@123` | **Viewer** | Most restricted. Can only view their *own* personal transactions and basic summaries. |

---

## 📡 Core Features & Endpoints

### 👤 User Management (`/api/auth` & `/api/users`)
Handle user registration, secure login, profile data, and role promotions (Admin only).

### 💳 Transactions (`/api/transactions`)
The heart of the app. Add incomes and expenses, delete mistakes, or retrieve historical data using powerful filters (by category, date range, or transaction type). 
*(Bonus: Admins and Analysts can export reports to CSV or JSON!)*

### 📊 Financial Analytics (`/api/analytics`)
Skip the manual math! Hit these endpoints to instantly get:
- Your total balance, total income, and total expenses.
- A breakdown of where your money went by category (e.g., Rent vs. Groceries).
- Monthly spending trends.

---

## 🧪 Testing

We believe in reliable code. This project includes a 100% passing test suite covering authentication, role validation, accurate analytics math, and database CRUD operations. 

To run the tests yourself:
```bash
pytest tests/ -v
```

---

## 📜 License
This project is built for educational and portfolio purposes. Feel free to fork it, learn from it, and build your own awesome front-end on top of it!
```
