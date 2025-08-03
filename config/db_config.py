import os
from dotenv import load_dotenv

load_dotenv()

SQL_DB_URI = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
)

DORIS_DB = {
    "host": os.getenv("DORIS_HOST"),
    "port": int(os.getenv("DORIS_PORT")),
    "user": os.getenv("DORIS_USER"),
    "password": os.getenv("DORIS_PASSWORD"),
    "database": os.getenv("DORIS_DATABASE"),
}
