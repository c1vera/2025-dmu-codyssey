from sqlalchemy import create_engine, inspect
from database import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables found:", tables)

for table_name in ["question", "answer"]:
    if table_name in tables:
        columns = inspector.get_columns(table_name)
        print(f"\nColumns in '{table_name}' table:")
        for column in columns:
            print(f"- {column['name']} ({column['type']})")
    else:
        print(f"Table '{table_name}' not found.")
