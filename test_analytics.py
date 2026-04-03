"""
Tests for analytics endpoints – summary, category breakdown, monthly totals.
"""

from tests.conftest import auth_header

INCOME = {
    "amount": 5000.00,
    "type": "income",
    "category": "Salary",
    "date": "2026-03-01",
    "description": "March salary",
}
EXPENSE = {
    "amount": 1200.00,
    "type": "expense",
    "category": "Rent",
    "date": "2026-03-05",
    "description": "Monthly rent",
}


def _seed(client, token):
    """Insert two transactions as admin."""
    client.post("/api/transactions", json=INCOME, headers=auth_header(token))
    client.post("/api/transactions", json=EXPENSE, headers=auth_header(token))


class TestSummary:
    def test_summary_values(self, client, admin_user):
        _, token = admin_user
        _seed(client, token)

        resp = client.get("/api/analytics/summary", headers=auth_header(token))
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_income"] == 5000.00
        assert data["total_expenses"] == 1200.00
        assert data["balance"] == 3800.00
        assert data["transaction_count"] == 2

    def test_viewer_can_see_summary(self, client, admin_user, viewer_user):
        _, admin_token = admin_user
        _, viewer_token = viewer_user
        _seed(client, admin_token)

        resp = client.get(
            "/api/analytics/summary", headers=auth_header(viewer_token)
        )
        assert resp.status_code == 200


class TestCategoryBreakdown:
    def test_breakdown(self, client, admin_user):
        _, token = admin_user
        _seed(client, token)

        resp = client.get(
            "/api/analytics/category-breakdown", headers=auth_header(token)
        )
        assert resp.status_code == 200
        categories = {c["category"]: c["total"] for c in resp.json()}
        assert categories["Salary"] == 5000.00
        assert categories["Rent"] == 1200.00

    def test_viewer_cannot_access(self, client, viewer_user):
        _, token = viewer_user
        resp = client.get(
            "/api/analytics/category-breakdown", headers=auth_header(token)
        )
        assert resp.status_code == 403


class TestMonthlyTotals:
    def test_monthly(self, client, admin_user):
        _, token = admin_user
        _seed(client, token)

        resp = client.get(
            "/api/analytics/monthly", headers=auth_header(token)
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        march = data[0]
        assert march["month"] == "2026-03"
        assert march["income"] == 5000.00
        assert march["expenses"] == 1200.00
        assert march["net"] == 3800.00


class TestRecentActivity:
    def test_recent(self, client, admin_user):
        _, token = admin_user
        _seed(client, token)

        resp = client.get(
            "/api/analytics/recent?limit=5", headers=auth_header(token)
        )
        assert resp.status_code == 200
        assert len(resp.json()) == 2
