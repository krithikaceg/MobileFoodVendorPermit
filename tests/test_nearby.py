import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base  # import your Base and models
import datetime
from app.models import VendorApplication
from app.services import get_applicants_within_radius, get_vendors_nearby

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

def test_get_applicants_with_approved_status(db):
    bounding_box = (39.0, 42.0, -76.0, -73.0)  # min_lat, max_lat, min_long, max_long
    
    db.add_all([
        VendorApplication(id = 1,latitude=41.0, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=40.0, longitude=-74.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=40.0, longitude=-74.6, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A")
    ])
    db.commit()
    result =  get_applicants_within_radius(bounding_box, db, False)
    assert len(result) == 2
    for applicant in result:
        assert applicant.status == "APPROVED"
        assert(applicant.id in (1, 2))

def test_get_applicants_all_status_true(db):
    
    bounding_box = (40.0, 41.0, -75.0, -74.0)

    db.add_all([
        VendorApplication(id = 1,latitude=41.0, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=40.0, longitude=-74.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=40.0, longitude=-74.6, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A")
    ])
    db.commit()
    result =  get_applicants_within_radius(bounding_box, db, True)
    assert len(result) == 3

def test_get_applicants_within_radius_all_status_true(db):
    db.add_all([
        VendorApplication(id = 1,latitude=41.0, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=40.0, longitude=-74.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=40.0, longitude=-74.6, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A")
    ])
    db.commit()
    bounding_box = (0, 45, -76, -74.5)
    result =  get_applicants_within_radius(bounding_box, db, True)

    # returns vendors within boundary (max 15)
    assert len(result) == 2

def test_get_applicants_within_radius_result_greater_than_5(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=41.0002, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=41.0003, longitude=-75.0, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 4, latitude=41.0004, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 5, latitude=41.0005, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 6, latitude=41.0006, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
    ])
    db.commit()
    bounding_box = (41.0001, 41.0007, -75.01, -75.0)
    result =  get_applicants_within_radius(bounding_box, db, True)

    assert len(result) == 6

def test_get_applicants_within_radius(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=41.0002, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=41.0003, longitude=-75.0, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 4, latitude=41.0004, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 5, latitude=41.0005, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 6, latitude=41.0006, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
    ])
    db.commit()
    bounding_box = (41.0001, 41.0003, -75.01, -75.0)
    result =  get_applicants_within_radius(bounding_box, db, True)

    assert len(result) == 3

def test_get_vendors_nearby_return_top_5(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.000001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 2, latitude=41.000002, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 3, latitude=41.000003, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 4, latitude=41.000004, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 5, latitude=41.000005, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 6, latitude=41.000006, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC")
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.0, -75.0, db, False)

    assert len(result) == 5
    for r in result:
        assert r.id in range(6)

def test_get_vendors_nearby_all_status_true_max_5(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="A"),
        VendorApplication(id = 2, latitude=41.0002, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 7, 1), applicant_name="A"),
        VendorApplication(id = 3, latitude=41.0003, longitude=-75.0, status="PENDING",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 4, latitude=41.0004, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 5, latitude=41.0005, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
        VendorApplication(id = 6, latitude=41.0006, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 8, 1), applicant_name="A"),
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.003, -75.0, db, True)

    assert len(result) == 5 

def test_get_vendors_nearby_same_address_same_vendor_name(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 2, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC")
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.001, -75.0, db, True)

    assert len(result) == 1 

def test_get_vendors_nearby_same_address_different_vendor_name(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 2, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="XYZ")
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.001, -75.0, db, True)

    assert len(result) == 2

def test_get_vendors_nearby_same_address_same_vendor_name_only_approved(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 2, latitude=41.0001, longitude=-75.0, status="PENDING",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC")
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.001, -75.0, db, False)

    assert len(result) == 1 
    assert result[0].id == 1

def test_get_vendors_nearby_same_address_different_vendor_name_only_approved(db):

    db.add_all([
        VendorApplication(id = 1, latitude=41.0001, longitude=-75.0, status="APPROVED",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="ABC"),
        VendorApplication(id = 2, latitude=41.0001, longitude=-75.0, status="PENDING",
                          expiration_date=datetime.datetime(2025, 6, 1), applicant_name="XYZ")
    ])
    db.commit()
    
    result =  get_vendors_nearby(41.001, -75.0, db, True)

    assert len(result) == 2
    assert result[0].id == 1

