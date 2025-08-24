from sqlalchemy_schemadisplay import create_schema_graph
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    graph = create_schema_graph(
    engine=db.engine,
    metadata=db.Model.metadata,
    show_datatypes=True,    # column types
    show_indexes=True,      # keep indexes visible for clarity
    rankdir="TB",           # top-to-bottom layout 
    concentrate=True        # merge lines
)

    graph.write_png("erd.png")
    print("ERD generated as erd.png")
