from app import create_app
from app.extensions import db
from app.dev import seed  # this is the correct import path

def reset_and_seed():
    app = create_app()
    with app.app_context():
        print("⏳ Dropping and recreating database...")
        db.drop_all()
        db.create_all()
        seed.main()  # call the function inside seed.py

if __name__ == "__main__":
    reset_and_seed()
