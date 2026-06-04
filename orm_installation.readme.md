THIS SHOULD BE DATABASE.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg://postgres:Chibueze2007@127.0.0.1:5432/local database'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

download pyscopg so that you can connect with the url to the database

THIS SHOULD BE MODELS.py

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts" 
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), 
        nullable=False,
        server_default=text('now()'))


THIS SHOULD BE MAIN.pyfrom . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(engine)

app = FastAPI()

pass this into the path parameters
db: Session = Depends(get_db)

alembic after installing run alembic init alembic 
then go to alembic iit and chage script location to alembic
then go to env.py and import base from orm models

then run alembic to see if your database is connected.
