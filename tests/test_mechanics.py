import unittest
from app import create_app
from app.extensions import db
from app.models import Mechanic
from app.utils.auth import encode_token


class TestMechanics(unittest.TestCase):
    def setUp(self):
        """
        Fresh app + db before each test.
        Creates one mechanic + token for protected routes.
        """
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            mech = Mechanic(name="Mike", email="mike@ex.com", specialty="Brakes")
            mech.set_password("123")
            db.session.add(mech)
            db.session.commit()
            self.token = encode_token(mech.id, "mechanic")

    # ---------- POST /mechanics ----------
    def test_create_mechanic_valid(self):
        payload = {"name": "John", "email": "john@ex.com", "password": "123", "specialty": "Engines"}
        response = self.client.post("/mechanics", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_mechanic_missing_email(self):
        payload = {"name": "Bad", "password": "123", "specialty": "Wheels"}
        response = self.client.post("/mechanics", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_mechanic_duplicate_email(self):
        payload = {"name": "Dup", "email": "mike@ex.com", "password": "123", "specialty": "Brakes"}
        response = self.client.post("/mechanics", json=payload)
        self.assertEqual(response.status_code, 409)

    # ---------- POST /mechanics/login ----------
    def test_login_valid(self):
        payload = {"email": "mike@ex.com", "password": "123"}
        response = self.client.post("/mechanics/login", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json)

    def test_login_invalid_password(self):
        payload = {"email": "mike@ex.com", "password": "wrong"}
        response = self.client.post("/mechanics/login", json=payload)
        self.assertEqual(response.status_code, 401)

    # ---------- GET /mechanics ----------
    def test_get_mechanics_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/mechanics", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_get_mechanics_no_token(self):
        response = self.client.get("/mechanics")
        self.assertEqual(response.status_code, 401)

    # ---------- PUT /mechanics/<id> ----------
    def test_update_mechanic_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.put("/mechanics/1", json={"specialty": "Suspension"}, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_mechanic_no_token(self):
        response = self.client.put("/mechanics/1", json={"specialty": "Suspension"})
        self.assertEqual(response.status_code, 401)

    # ---------- DELETE /mechanics/<id> ----------
    def test_delete_mechanic_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.delete("/mechanics/1", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_mechanic_no_token(self):
        response = self.client.delete("/mechanics/1")
        self.assertEqual(response.status_code, 401)

    # ---------- GET /mechanics/my-tickets ----------
    def test_my_tickets_authorized(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/mechanics/my-tickets", headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_my_tickets_no_token(self):
        response = self.client.get("/mechanics/my-tickets")
        self.assertEqual(response.status_code, 401)

    # ---------- GET /mechanics/top ----------
    def test_top_mechanic_no_token(self):
        response = self.client.get("/mechanics/top")
        self.assertEqual(response.status_code, 401)

    # ---------- GET /mechanics/ticket-count ----------
    def test_ticket_count_no_token(self):
        response = self.client.get("/mechanics/ticket-count")
        self.assertEqual(response.status_code, 401)
