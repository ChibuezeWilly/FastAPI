import pytest

from fastapi.testclient import TestClient
from app.main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

SQLALCHEMY_DATABASE_URL_TEST = 'postgresql+psycopg://postgres:Chibueze2007@127.0.0.1:5432/fastapi_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False)

@pytest.fixture()
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture()
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overide_get_db
    yield TestClient(app)
    
    
@pytest.fixture()
def test_user(client):
    user_data = {
        "email": "pricelesswilliams1234@gmail.com", "password":"Chibueze2007"
    } 
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
    