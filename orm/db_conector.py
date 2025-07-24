import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432") 
DB_NAME = os.getenv("POSTGRES_DB")
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Conectando --> {DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

try:
    engine = create_engine(DATABASE_URL, echo=False)
    print("Conexion OK")
except Exception as e:
    print(f"Error al conectar la bd --> {e}")
    raise

Base = declarative_base()
dbSession = sessionmaker(bind=engine)

def get_dbengine():
    return engine

def get_dbconnection():
    return engine.connect()

def get_dbsession():
    return dbSession()
