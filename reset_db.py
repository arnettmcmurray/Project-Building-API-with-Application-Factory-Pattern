from app import create_app, db
from config import ProductionConfig
import seed

def reset_and_seed():
    app = create_app(ProductionConfig)  # use class, not string
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed.run_seed()

if __name__ == "__main__":
    reset_and_seed()
