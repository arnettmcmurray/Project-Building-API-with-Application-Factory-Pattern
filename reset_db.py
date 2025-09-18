# reset_db.py
# This resets and seeds the database in the same way Render does at deploy
# No .env, no local secret lookups. GitHub provides DATABASE_URL to Render.

from app import create_app, db
import seed

def reset_and_seed():
    # Force ProductionConfig so DATABASE_URL comes from GitHub/Render secrets
    app = create_app("production")
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed.run_seed()

if __name__ == "__main__":
    reset_and_seed()
