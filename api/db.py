import dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

USER = os.getenv('MYSQL_USER')
PASS = os.getenv('MYSQL_PASSWORD')
HOST = os.getenv('MYSQL_HOST')
PORT = os.getenv('MYSQL_PORT')
DB = os.getenv('MYSQL_DATABASE')

DATABASE_URL = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@db:3306/{MYSQL_DB}"engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()