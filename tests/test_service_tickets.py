import unittest
from app import create_app
from app.extensions import db
from app.models import ServiceTicket, Customer
from app.utils.auth import encode_token

class TestServiceTickets(unittest.TestCase):
    def setUp(self):
        """Fresh app + db + starter customer for token"""
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            cust = Customer(name="Jane", email="jane@ex.com", phone="111", car="Toyota")
            db.session.add(cust)
            db.session.commit()
            self.token = encode_token(cust.id, "user")

    # ---------- POST /service_tickets ----------
    def test_create_ticket_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"description": "Oil Change", "customer_id": 1}
        response = self.client.post("/service_tickets", json=payload, headers=headers)
        self.assertEqual(response.status_code, 201)

    def test_create_ticket_no_token(self):
        payload = {"description": "Brake Check", "customer_id": 1}
        response = self.client.post("/service_tickets", json=payload)
        self.assertEqual(response.status_code, 401)

    # ---------- GET /service_tickets ----------
    def test_get_tickets_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/service_tickets", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_tickets_no_token(self):
        response = self.client.get("/service_tickets")
        self.assertEqual(response.status_code, 401)

    # ---------- PUT /service_tickets/<id> ----------
    def test_update_ticket_no_token(self):
        response = self.client.put("/service_tickets/1", json={"description": "Update"})
        self.assertEqual(response.status_code, 401)

    # ---------- DELETE /service_tickets/<id> ----------
    def test_delete_ticket_no_token(self):
        response = self.client.delete("/service_tickets/1")
        self.assertEqual(response.status_code, 401)
