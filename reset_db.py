from app import create_app
from app.extensions import db

# Create app context
app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    print(" Database reset: all tables dropped and recreated")
