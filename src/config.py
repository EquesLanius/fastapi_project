from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

DB_HOST_TEST = os.environ.get("TEST_DB_HOST")
DB_PORT_TEST = os.environ.get("TEST_DB_PORT")
DB_NAME_TEST = os.environ.get("TEST_DB_NAME")
DB_USER_TEST = os.environ.get("TEST_DB_USER")
DB_PASS_TEST = os.environ.get("TEST_DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

SECRET_AUTH = os.environ.get("SECRET_AUTH")

KP_TOKEN = os.environ.get("KP_TOKEN")
KP_URL = os.environ.get("KP_URL")
MAL_URL = os.environ.get("MAL_URL")