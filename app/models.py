from sqlalchemy import Column, Integer, String, Float, DateTime
from .db import Base

class VendorApplication(Base):
    __tablename__ = "food_vendor_application"

    id = Column(Integer, primary_key=True, index=True)
    applicant_name = Column(String, index=True)
    facility_type = Column(String)
    status = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    approved = Column(DateTime, nullable=True)
    expiration_date = Column(DateTime, nullable=True)
