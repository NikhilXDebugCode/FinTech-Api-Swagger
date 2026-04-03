"""
Tests for transaction CRUD, filtering, validation, and role enforcement.
"""

from tests.conftest import auth_header

SAMPLE = {
    "amount": 1500.00,
    "type": "income",
    "category": "Salary",
    "date": "2026-03-01",
    "description": "March salary",
}


class TestCreateTransaction:
    def test_admin_can_create(self, client, admin_user):
        _, token = admin_user
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["amount"] == 1500.00
        assert data["category"] == "Salary"

    def test_viewer_cannot_create(self, client, viewer_user):
        _, token = viewer_user
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        assert resp.status_code == 403

    def test_analyst_cannot_create(self, client, analyst_user):
        _, token = analyst_user
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        assert resp.status_code == 403

    def test_invalid_amount(self, client, admin_user):
        _, token = admin_user
        bad = {**SAMPLE, "amount": -100}
        resp = client.post(
            "/api/transactions", json=bad, headers=auth_header(token)
        )
        assert resp.status_code == 422

    def test_missing_category(self, client, admin_user):
        _, token = admin_user
        bad = {**SAMPLE}
        del bad["category"]
        resp = client.post(
            "/api/transactions", json=bad, headers=auth_header(token)
        )
        assert resp.status_code == 422


class TestReadTransaction:
    def _create(self, client, token):
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        return resp.json()["id"]

    def test_get_by_id(self, client, admin_user):
        _, token = admin_user
        txn_id = self._create(client, token)
        resp = client.get(
            f"/api/transactions/{txn_id}", headers=auth_header(token)
        )
        assert resp.status_code == 200
        assert resp.json()["id"] == txn_id

    def test_not_found(self, client, admin_user):
        _, token = admin_user
        resp = client.get(
            "/api/transactions/9999", headers=auth_header(token)
        )
        assert resp.status_code == 404


class TestUpdateTransaction:
    def test_admin_can_update(self, client, admin_user):
        _, token = admin_user
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        txn_id = resp.json()["id"]

        resp = client.put(
            f"/api/transactions/{txn_id}",
            json={"amount": 2000, "category": "Bonus"},
            headers=auth_header(token),
        )
        assert resp.status_code == 200
        assert resp.json()["amount"] == 2000
        assert resp.json()["category"] == "Bonus"


class TestDeleteTransaction:
    def test_admin_can_delete(self, client, admin_user):
        _, token = admin_user
        resp = client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(token)
        )
        txn_id = resp.json()["id"]

        resp = client.delete(
            f"/api/transactions/{txn_id}", headers=auth_header(token)
        )
        assert resp.status_code == 204

        # Verify gone
        resp = client.get(
            f"/api/transactions/{txn_id}", headers=auth_header(token)
        )
        assert resp.status_code == 404


class TestListTransactions:
    def test_analyst_can_list(self, client, admin_user, analyst_user):
        _, admin_token = admin_user
        _, analyst_token = analyst_user

        # Create a few records
        for i in range(3):
            client.post(
                "/api/transactions", json=SAMPLE, headers=auth_header(admin_token)
            )

        resp = client.get(
            "/api/transactions", headers=auth_header(analyst_token)
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 3
        assert len(data["items"]) == 3

    def test_viewer_cannot_list(self, client, viewer_user):
        _, token = viewer_user
        resp = client.get(
            "/api/transactions", headers=auth_header(token)
        )
        assert resp.status_code == 403

    def test_filter_by_type(self, client, admin_user, analyst_user):
        _, admin_token = admin_user
        _, analyst_token = analyst_user

        client.post(
            "/api/transactions", json=SAMPLE, headers=auth_header(admin_token)
        )
        expense = {**SAMPLE, "type": "expense", "category": "Rent", "amount": 800}
        client.post(
            "/api/transactions", json=expense, headers=auth_header(admin_token)
        )

        resp = client.get(
            "/api/transactions?type=income", headers=auth_header(analyst_token)
        )
        assert resp.json()["total"] == 1
