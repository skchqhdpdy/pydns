import os
from dotenv import load_dotenv

load_dotenv()

APP_PORT = int(os.environ["APP_PORT"])

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]
DB_DSN = f"mysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

mmdb_id = os.environ["mmdb_id"]
mmdb_key = os.environ["mmdb_key"]