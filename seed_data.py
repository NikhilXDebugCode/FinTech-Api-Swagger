"""
Seed script – populates the database with sample users and transactions.

Usage:
    python seed_data.py
"""

import sys
from datetime import date

# Ensure imports work when running from project root
sys.path.insert(0, ".")

from app.database import Base, SessionLocal, engine
from app.models.transaction import Transaction, TransactionType
from app.models.user import User, UserRole
from app.services.auth_service import hash_password


def seed():
    """Drop existing data, recreate tables, and insert sample records."""

    print("🔄 Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # ── Users ────────────────────────────────────────────
        admin = User(
            username="admin",
            email="admin@fintrack.com",
            hashed_password=hash_password("Admin@123"),
            role=UserRole.ADMIN,
        )
        analyst = User(
            username="analyst",
            email="analyst@fintrack.com",
            hashed_password=hash_password("Analyst@123"),
            role=UserRole.ANALYST,
        )
        viewer = User(
            username="viewer",
            email="viewer@fintrack.com",
            hashed_password=hash_password("Viewer@123"),
            role=UserRole.VIEWER,
        )
        db.add_all([admin, analyst, viewer])
        db.flush()  # assigns IDs

        print(f"✅ Created users: admin (id={admin.id}), analyst (id={analyst.id}), viewer (id={viewer.id})")

        # ── Transactions ─────────────────────────────────────
        transactions = [
            # January 2026
            Transaction(amount=5000.00, type=TransactionType.INCOME, category="Salary", date=date(2026, 1, 1), description="January salary", user_id=admin.id),
            Transaction(amount=1200.00, type=TransactionType.EXPENSE, category="Rent", date=date(2026, 1, 3), description="Monthly rent", user_id=admin.id),
            Transaction(amount=300.00, type=TransactionType.EXPENSE, category="Groceries", date=date(2026, 1, 5), description="Weekly groceries", user_id=admin.id),
            Transaction(amount=150.00, type=TransactionType.EXPENSE, category="Utilities", date=date(2026, 1, 10), description="Electricity bill", user_id=admin.id),
            Transaction(amount=500.00, type=TransactionType.INCOME, category="Freelance", date=date(2026, 1, 15), description="Logo design project", user_id=admin.id),

            # February 2026
            Transaction(amount=5000.00, type=TransactionType.INCOME, category="Salary", date=date(2026, 2, 1), description="February salary", user_id=admin.id),
            Transaction(amount=1200.00, type=TransactionType.EXPENSE, category="Rent", date=date(2026, 2, 3), description="Monthly rent", user_id=admin.id),
            Transaction(amount=450.00, type=TransactionType.EXPENSE, category="Groceries", date=date(2026, 2, 7), description="Bi-weekly groceries", user_id=admin.id),
            Transaction(amount=200.00, type=TransactionType.EXPENSE, category="Transport", date=date(2026, 2, 12), description="Metro pass", user_id=admin.id),
            Transaction(amount=80.00, type=TransactionType.EXPENSE, category="Entertainment", date=date(2026, 2, 14), description="Movie night", user_id=admin.id),

            # March 2026
            Transaction(amount=5000.00, type=TransactionType.INCOME, category="Salary", date=date(2026, 3, 1), description="March salary", user_id=admin.id),
            Transaction(amount=1200.00, type=TransactionType.EXPENSE, category="Rent", date=date(2026, 3, 3), description="Monthly rent", user_id=admin.id),
            Transaction(amount=600.00, type=TransactionType.EXPENSE, category="Healthcare", date=date(2026, 3, 8), description="Dental checkup", user_id=admin.id),
            Transaction(amount=1000.00, type=TransactionType.INCOME, category="Freelance", date=date(2026, 3, 20), description="Web development gig", user_id=admin.id),
            Transaction(amount=250.00, type=TransactionType.EXPENSE, category="Groceries", date=date(2026, 3, 22), description="Weekly groceries", user_id=admin.id),
            Transaction(amount=100.00, type=TransactionType.EXPENSE, category="Subscriptions", date=date(2026, 3, 25), description="Streaming services", user_id=admin.id),
        ]

        db.add_all(transactions)
        db.commit()

        print(f"✅ Created {len(transactions)} sample transactions")
        print("\n📋 Seeded credentials:")
        print("   admin   / Admin@123   (role: admin)")
        print("   analyst / Analyst@123 (role: analyst)")
        print("   viewer  / Viewer@123  (role: viewer)")
        print("\n🚀 Run the server with: uvicorn app.main:app --reload")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
