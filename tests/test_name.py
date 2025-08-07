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

def test_get_vendors_by_name(db):
    # Arrange
    db.add_all([
        VendorApplication(applicant_name = "Authentic India", status="APPROVED"),
        VendorApplication(applicant_name = "El Tonayense #60", status="PENDING"),
        VendorApplication(applicant_name = "El Tonayense #60", status="APPROVED"),
        VendorApplication(applicant_name = "Truly Food & More", status="EXPIRED")
    ])
    db.commit()

    # Assert
    assert len(get_vendors_by_name('ANBC', False, db)) == 0
    assert len(get_vendors_by_name('Authentic India', False, db)) == 1
    assert len(get_vendors_by_name('Authentic India', True, db)) == 1
    assert len(get_vendors_by_name('authentic INDIA', True, db)) == 1
    assert len(get_vendors_by_name('El Tonayense #60', False, db)) == 1
    assert len(get_vendors_by_name('El Tonayense #60', True, db)) == 2
    assert len(get_vendors_by_name('Truly Food & More', True, db)) == 1
    assert len(get_vendors_by_name('Truly Food & More', False, db)) == 0
    assert len(get_vendors_by_name('delete from vendor_application', True, db)) == 0
