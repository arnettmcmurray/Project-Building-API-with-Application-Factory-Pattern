import pytest
from app import create_app, db
from config import TestingConfig

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    app.config.update({"TESTING": True})

    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
