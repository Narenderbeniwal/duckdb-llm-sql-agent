# csv_to_duckdb_loader.py

import os
import logging
import duckdb
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase

CSV_DIR = "data/"        # Folder containing your CSV files
DB_FILE = "mydb.duckdb"  # DuckDB database file
LOG_FILE = "csv_import.log"  # Log file for import process

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def init_db():
    con = duckdb.connect(database=DB_FILE)

    for fname in os.listdir(CSV_DIR):
        if fname.endswith(".csv"):
            table = os.path.splitext(fname)[0]  # Use filename (without extension) as table name
            fpath = os.path.join(CSV_DIR, fname)

            try:
                con.execute(f"""
                    CREATE OR REPLACE TABLE {table} AS 
                    SELECT * FROM read_csv_auto('{fpath}')
                """)
                msg = f"Loaded '{fname}' into table '{table}'"
                print(msg)
                logging.info(msg)

            except Exception as e:
                err_msg = f"Skipped '{fname}' due to error: {e}"
                print(err_msg)
                logging.error(err_msg)

    engine = create_engine(f"duckdb:///{DB_FILE}")
    db = SQLDatabase(engine)

    tables = db.get_usable_table_names()
    print("Tables available in the DB:", tables)
    logging.info(f"Available tables: {tables}")

    return db

# Only run this if executed directly
if __name__ == "__main__":
    init_db()

# When imported, you still get db ready
db = init_db()
