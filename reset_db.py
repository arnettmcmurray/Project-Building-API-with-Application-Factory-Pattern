from app import create_app, db
import seed

def reset_and_seed():
    app = create_app("production")
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed.run_seed()

if __name__ == "__main__":
    reset_and_seed()
