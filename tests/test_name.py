import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base  # import your Base and models
import datetime
from app.models import VendorApplication
from app.services import get_vendors_by_name

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

def test_get_vendors_by_name_non_existent(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()

    result =  get_vendors_by_name('ANBC', db, False)
    assert len(result) == 0
    

def test_get_vendors_by_name_approved(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('Authentic India', db, False)
    assert len(result) == 1

def test_get_vendors_by_name_all_status(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('Authentic India', db, True)
    assert len(result) == 1

def test_get_vendors_by_name_approved_case_insentive(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('authentic INDIA', db, True)
    assert len(result) == 1

def test_get_vendors_by_name_only_approved(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('El Tonayense #60', db, False)
    assert len(result) == 1

def test_get_vendors_by_name_all_status(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('El Tonayense #60', db, True)
    assert len(result) == 2

def test_get_vendors_by_name_status_expired_all_status(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('Truly Food & More', db, True)
    assert len(result) == 1

def test_get_vendors_by_name_status_expired_approved_only(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('Truly Food & More', db, False)
    assert len(result) == 0

def test_get_vendors_by_name_sql_injection(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()
    result =  get_vendors_by_name('delete from food_vendor_application;', db, True)
    assert len(result) == 0
