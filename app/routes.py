from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import VendorApplication
from app.services import get_vendors_by_name, get_vendors_by_address, get_vendors_nearby
from sqlalchemy import func
import logging
import sys


logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint that also verifies database connectivity"""
    try:
        # Try to count records in the table
        count = db.query(VendorApplication).count()
        return {
            "status": "healthy", 
            "database": "connected",
            "vendor_count": count
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

@router.get("/applicants")
async def read_vendors(name: str, all_status: bool = False, db: Session = Depends(get_db)):
    logger.debug("read_vendors %s %s", name, all_status)
    return get_vendors_by_name(name, all_status, db)

@router.get("/applicants/address")
async def read_vendors_from_address(contains: str, db: Session = Depends(get_db)):
    logger.debug("read_facilities_from_address %s", contains)
    return get_vendors_by_address(contains, db)

@router.get("/applicants/nearby")
async def read_vendors_nearby(lat: float, long: float, all_status: bool = False, db: Session = Depends(get_db)):
    applicants = get_vendors_nearby(lat, long, all_status, db)
    return applicants

