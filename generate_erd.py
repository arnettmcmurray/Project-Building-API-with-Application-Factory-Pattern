from sqlalchemy_schemadisplay import create_schema_graph
from app.extensions import db
from app import create_app

# Create app + push context in order
app = create_app()
with app.app_context():
    engine = db.get_engine()
    metadata = db.Model.metadata

    graph = create_schema_graph(
        metadata=metadata,
        engine=engine,
        show_datatypes=True,
        show_indexes=True,
        rankdir="LR",
        concentrate=False
    )

    graph.write_png("erd.png")
    print("✅ ERD generated as erd.png")
