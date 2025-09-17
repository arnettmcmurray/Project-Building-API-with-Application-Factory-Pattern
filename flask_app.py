from app import create_app
from config import ProductionConfig

app = create_app("config.ProductionConfig")

if __name__ == "__main__":
    app.run(debug=True)

