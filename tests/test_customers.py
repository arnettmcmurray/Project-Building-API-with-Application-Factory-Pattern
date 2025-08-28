import unittest
from app import create_app
from app.extensions import db
from app.models import Customer
from app.utils.auth import encode_token

class TestCustomers(unittest.TestCase):
    def setUp(self):
        """
        Fresh test app + db before each run.
        Creates a fake token (id=1) for endpoints requiring @token_required.
        """
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            # create a dummy token for customer role
            self.token = encode_token(1, "user")

    # ---------- POST /customers ----------
    def test_create_customer_valid(self):
        # Positive: create customer with all fields
        payload = {"name": "Jane Doe", "email": "jane@example.com", "phone": "123456", "car": "Toyota"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_customer_missing_email(self):
        # Negative: missing required email
        payload = {"name": "No Email", "phone": "111222", "car": "Honda"}
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_customer_duplicate_email(self):
        # Duplicate emails are blocked (IntegrityError -> 409)
        payload = {"name": "Jane", "email": "jane@dup.com", "phone": "123", "car": "Toyota"}
        self.client.post("/customers", json=payload)
        response = self.client.post("/customers", json=payload)
        self.assertEqual(response.status_code, 409)

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
        # First create
        self.client.post("/customers", json={"name": "Jane", "email": "jane@ex.com", "phone": "111", "car": "Toyota"})
        # Then update with token
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

    # ---------- GET /customers/search ----------
    def test_search_customer_found(self):
        # Create a customer first
        self.client.post("/customers", json={"name": "Sam", "email": "sam@example.com", "phone": "333", "car": "Ford"})
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/customers/search?email=sam@example.com", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_search_customer_not_found(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/customers/search?email=notfound@example.com", headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_search_customer_no_email_param(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/customers/search", headers=headers)
        self.assertEqual(response.status_code, 400)
