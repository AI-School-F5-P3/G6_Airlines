import dotenv
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

USER = os.getenv('DEV_USER')
PASS = os.getenv('DEV_PASSWORD')
HOST = os.getenv('DEV_HOST')
PORT = os.getenv('DEV_PORT')
DB = os.getenv('DEV_DATABASE')

database_url = f"mysql+mysqlconnector://{USER}:{PASS}@{HOST}:{PORT}/{DB}"

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()