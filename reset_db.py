from app import create_app
from app.extensions import db
import seed   # just import the file, it runs its own seeding code
from config import ProductionConfig

app = create_app(ProductionConfig)

with app.app_context():
    db.drop_all()
    db.create_all()
    print(" Database reset (Production)")

    # seed runs automatically on import
    print("🌱 Database reseeded with sample data (Production)")
