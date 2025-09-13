from app import create_app
from app.extensions import db
from config import ProductionConfig
from seed import run_seed   # seeding logic is wrapped in run_seed()

app = create_app(ProductionConfig)

with app.app_context():
    # Drop and recreate tables
    db.drop_all()
    db.create_all()
    print("✅ Database reset (Production)")

    # Seed
    run_seed()
    print("🌱 Database reseeded with sample data (Production)")
