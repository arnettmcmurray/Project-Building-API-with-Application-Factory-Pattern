import unittest
from app import create_app
from app.extensions import db
from app.models import Customer
from app.utils.auth import encode_token

class TestCustomers(unittest.TestCase):
    def setUp(self):
        """Spin up fresh test app + db before each test"""
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # no default customer — created inside tests
            self.token = encode_token(1, "user")  # fake user id, role user

    # ---------- POST /customers ----------
    def test_create_customer_valid(self):
        """Positive: create a customer with valid data"""
        payload = {"name": "Jane Doe", "email": "jane@example.com", "phone": "123456", "car": "Toyota"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_customer_missing_email(self):
        """Negative: missing required field"""
        payload = {"name": "No Email", "phone": "111222", "car": "Honda"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 400)

    # ---------- GET /customers ----------
    def test_get_customers_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/customers", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_customers_no_token(self):
        response = self.client.get("/customers")
        self.assertEqual(response.status_code, 401)

    # ---------- PUT /customers/<id> ----------
    def test_update_customer_authorized(self):
        self.client.post("/customers", json={"name": "Jane", "email": "jane@ex.com", "phone": "111", "car": "Toyota"})
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.put("/customers/1", json={"name": "Jane Updated"}, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_customer_no_token(self):
        self.client.post("/customers", json={"name": "Jane", "email": "jane@ex.com", "phone": "111", "car": "Toyota"})
        response = self.client.put("/customers/1", json={"name": "Jane Updated"})
        self.assertEqual(response.status_code, 401)

    # ---------- DELETE /customers/<id> ----------
    def test_delete_customer_authorized(self):
        self.client.post("/customers", json={"name": "Jane", "email": "jane@ex.com", "phone": "111", "car": "Toyota"})
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete("/customers/1", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_customer_no_token(self):
        self.client.post("/customers", json={"name": "Jane", "email": "jane@ex.com", "phone": "111", "car": "Toyota"})
        response = self.client.delete("/customers/1")
        self.assertEqual(response.status_code, 401)
