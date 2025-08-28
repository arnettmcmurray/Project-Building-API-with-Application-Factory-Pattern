import unittest
from app import create_app
from app.extensions import db
from app.models import Inventory

class TestInventory(unittest.TestCase):
    def setUp(self):
        """Fresh app + db for inventory"""
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        with self.app.app_context():
            db.drop_all()
            db.create_all()

    # ---------- POST /inventory ----------
    def test_create_part_valid(self):
        payload = {"name": "Brake Pad", "price": 50}
        response = self.client.post("/inventory", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_create_part_missing_name(self):
        payload = {"price": 20}
        response = self.client.post("/inventory", json=payload)
        self.assertEqual(response.status_code, 400)

    def test_duplicate_part(self):
        payload = {"name": "Rotor", "price": 100}
        self.client.post("/inventory", json=payload)
        response = self.client.post("/inventory", json=payload)
        self.assertEqual(response.status_code, 409)

    # ---------- GET /inventory ----------
    def test_get_all_parts(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)

    # ---------- GET /inventory/<id> ----------
    def test_get_part_not_found(self):
        response = self.client.get("/inventory/999")
        self.assertEqual(response.status_code, 404)

    # ---------- PUT /inventory/<id> ----------
    def test_update_part_not_found(self):
        response = self.client.put("/inventory/999", json={"name": "Updated"})
        self.assertEqual(response.status_code, 404)

    # ---------- DELETE /inventory/<id> ----------
    def test_delete_part_not_found(self):
        response = self.client.delete("/inventory/999")
        self.assertEqual(response.status_code, 404)
