import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base  # import your Base and models
import datetime
from app.models import VendorApplication
from app.services import get_vendors_by_address

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_get_applicants_by_address(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = 'A1', address = '123 Sansome st', facility_type="Truck", status="APPROVED"),
        VendorApplication(applicant_name = 'A1', address = '123 Sansome st', facility_type="Truck", status="PENDING"),
        VendorApplication(applicant_name = 'A2', address = '4 Market st', facility_type="Cart", status="APPROVED"),
        VendorApplication(applicant_name = 'A3', address = '4 Main st', facility_type="Truck", status="APPROVED"),
    ])
    db.commit()
    # Assert
    assert len(get_vendors_by_address('california',  db)) == 0
    assert len(get_vendors_by_address('San',  db)) == 2
    assert len(get_vendors_by_address('Mai',  db)) == 1
    assert len(get_vendors_by_address(' Mai ',  db)) == 1
    assert len(get_vendors_by_address('market',  db)) == 0
    

