from pathlib import Path
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

db_host = os.getenv("DB_HOST")

engine = create_engine(
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{db_host}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

print("DB_HOST =", db_host)
print("AIRFLOW_HOME =", os.getenv("AIRFLOW_HOME"))