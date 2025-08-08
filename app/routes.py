from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .dependencies import get_db
from .services import get_vendors_by_name, get_vendors_by_address, get_vendors_nearby
from sqlalchemy import func
import logging
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()

# Pydantic Response Models
class VendorApplicationResponse(BaseModel):
    id: int
    applicant_name: str
    facility_type: str
    status: str
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    approved: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

    class Config:
        from_attributes = True 


@router.get("/applications", response_model=List[VendorApplicationResponse])
def read_vendors(name: str, all_status: bool = False, db: Session = Depends(get_db)):
    """Get vendors by name."""
    logger.debug("read_vendors %s %s", name, all_status)
    return get_vendors_by_name(name, db, all_status)

@router.get("/applications/address", response_model=List[VendorApplicationResponse])
def read_vendors_from_address(contains: str, db: Session = Depends(get_db)):
    """Get vendors by address containing the specified text."""
    logger.debug("read_facilities_from_address %s", contains)
    return get_vendors_by_address(contains, db)

@router.get("/applications/nearby", response_model=List[VendorApplicationResponse])
def read_vendors_nearby(lat: float, long: float, all_status: bool = False, db: Session = Depends(get_db)):
    """Get vendors near the specified coordinates."""
    logger.debug("read_vendors_nearby lat: %s long: %s, all_status: %s", lat, long, all_status)
    return get_vendors_nearby(lat, long, db, all_status)

