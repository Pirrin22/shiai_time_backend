from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Esta es la "dirección" de tu base de datos.
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://shiai_admin:admin123@localhost/shiai_time_db'

# El motor quue se encarga de hablar con PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# La sesión que usaremos para enviar y pedir datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()