from app import create_app

# Use ProductionConfig for Render deployment
app = create_app("config.ProductionConfig")





