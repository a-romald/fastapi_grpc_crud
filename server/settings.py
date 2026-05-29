import os
from dotenv import load_dotenv

load_dotenv()

GRPC_PORT = os.getenv("GRPC_PORT")
API_KEY_NAME = os.getenv("API_KEY_NAME")
VALID_API_KEY = os.getenv("VALID_API_KEY")
GRPC_KEY_NAME = os.getenv("GRPC_KEY_NAME")
GRPC_KEY_VAL = os.getenv("GRPC_KEY_VAL")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
