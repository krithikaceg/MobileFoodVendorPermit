from fastapi import Depends
from app.utils import get_bounding_box, haversine_distance
from app.models import VendorApplication
from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from app.dependencies import get_db
from sqlalchemy import func
import logging
import os

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)
NEARBY_VENDORS_COUNT = int(os.getenv("NEARBY_VENDORS_COUNT"))

# db = Session(Depends(get_db))

def get_vendors_by_name(name: str, all_status: bool = False, db: Session = Depends(get_db)):
    name = name.strip().lower()
    if (len(name) == 0 or len(name) > 200):
        return {"message" : "Name is either empty or too long"}
    applicants = db.query(VendorApplication).filter(func.lower(VendorApplication.applicant_name) == name)
    
    if not all_status:
        applicants = applicants.filter(VendorApplication.status == "APPROVED") # type: ignore
    return applicants.all()

def get_vendors_by_address(contains: str, db):
    contains = contains.strip().lower()
    if (len(contains) == 0):
        return {"message" : "contains is empty"}
    elif(len(contains) > 200):
       return {"message" : "contains is too long"}
    stmt = select(VendorApplication).where(VendorApplication.facility_type == 'Truck', 
                                           VendorApplication.address.ilike(f"%{contains}%"))
    result = db.execute(stmt)
    return result.scalars().all()

def get_vendors_nearby(lat: float, long: float, all_status: bool = False, db: Session = Depends(get_db)):
    bounding_lat_long = get_bounding_box(lat, long)
    logger.debug(bounding_lat_long)
    applicants = get_applicants_within_radius(bounding_lat_long, all_status, db)
    
    logger.debug(len(applicants))
    vendor_distances = {}
    for applicant in applicants:
        distance_from_given_point = haversine_distance(lat, long, applicant.latitude, applicant.longitude)
        vendor_distances[applicant.id] = (distance_from_given_point, applicant)

    logger.debug(vendor_distances)
    vendors = [v[1] for k, v in sorted(vendor_distances.items(), key = lambda item:item[1][0])[:NEARBY_VENDORS_COUNT]]
    
    return vendors

def get_applicants_within_radius(bounding_lat_long: tuple, all_status: bool = False, db: Session = Depends(get_db)):
    
    subquery_base = db.query(
        VendorApplication.latitude,
        VendorApplication.longitude,
        VendorApplication.applicant_name,
        func.max(VendorApplication.id).label("latest_id")
    ).filter(
        VendorApplication.latitude.between(bounding_lat_long[0], bounding_lat_long[1]),
        VendorApplication.longitude.between(bounding_lat_long[2], bounding_lat_long[3])
    )

    if not all_status:
        # logger.debug("Getting only Approved")
        subquery_base = subquery_base.filter(VendorApplication.status == "APPROVED")

    subquery = subquery_base.group_by(
        VendorApplication.latitude,
        VendorApplication.longitude,
        VendorApplication.applicant_name
    ).subquery()

    query = (
        db.query(VendorApplication)
        .join(
            subquery,
            VendorApplication.id == subquery.c.latest_id
        )
    )

    # limit(NEARBY_VENDORS_COUNT*3)
    result = query.all()
    for r in result:
        print(r.id)
    return result