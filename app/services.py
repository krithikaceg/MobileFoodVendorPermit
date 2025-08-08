from fastapi import Depends, HTTPException
from app.utils import get_bounding_box, haversine_distance
from app.models import VendorApplication
from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from app.dependencies import get_db
from sqlalchemy import func
import logging
import os
from app.settings import settings

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

def get_vendors_by_name(name: str, db, all_status: bool = False):
    name = name.strip().lower()
    if (len(name) == 0 or len(name) > 200):
        raise HTTPException(400, "Name cannot be empty or longer than 200 characters")
    stmt = select(VendorApplication).where(func.lower(VendorApplication.applicant_name) == name)
    
    if not all_status:
        stmt = stmt.where(VendorApplication.status == settings.approved) 
    result = db.execute(stmt)
    return result.scalars().all()

def get_vendors_by_address(contains: str, db):
    contains = contains.strip().lower()
    if (len(contains) == 0 or len(contains) > 200):
        raise HTTPException(400, "address search string cannot be empty or longer than 200 characters")
    stmt = select(VendorApplication).where(VendorApplication.facility_type == settings.food_truck, 
                                           VendorApplication.address.ilike(f"%{contains}%"))
    result = db.execute(stmt)
    return result.scalars().all()

def get_vendors_nearby(lat: float, long: float, db, all_status: bool = False):
    if (lat > 90 or lat < -90) or (long > 180 or long < -180):
        raise HTTPException(400, 'Latitude Longitide out of bounds')
    
    nearby_vendors_count = settings.nearby_vendors_count
    bounding_lat_long = get_bounding_box(lat, long)
    logger.debug(f"Lat: {lat} Long: {long} bounding_lat_long: {bounding_lat_long}")
    # TODO log
    applicants = get_applicants_within_radius(bounding_lat_long, db, all_status)
    
    logger.debug(f"Found {len(applicants)} applicants within bounding box by executing sql query")
    # TODO log
    vendor_distances = {}
    for applicant in applicants:
        distance_from_given_point = haversine_distance(lat, long, applicant.latitude, applicant.longitude)
        vendor_distances[applicant.id] = (distance_from_given_point, applicant)

    # TODO log
    vendors = [v[1] for k, v in sorted(vendor_distances.items(), key = lambda item:item[1][0])[:nearby_vendors_count]]
    logger.debug(f"For {nearby_vendors_count} applicants, chose {len(vendors)} nearby given ({lat},{long}) using haversine distance")
    return vendors

def get_applicants_within_radius(bounding_lat_long: tuple, db, all_status: bool = False):
    
    subquery_base = select(
        VendorApplication.latitude,
        VendorApplication.longitude,
        VendorApplication.applicant_name,
        func.max(VendorApplication.id).label("latest_id")
    ).where(
        VendorApplication.latitude.between(bounding_lat_long[0], bounding_lat_long[1]),
        VendorApplication.longitude.between(bounding_lat_long[2], bounding_lat_long[3])
    )

    if not all_status:
        # TODO log
        subquery_base = subquery_base.where(VendorApplication.status == settings.approved)

    subquery = subquery_base.group_by(
        VendorApplication.latitude,
        VendorApplication.longitude,
        VendorApplication.applicant_name
    ).subquery()

    stmt = (
        select(VendorApplication)
        .join(
            subquery,
            VendorApplication.id == subquery.c.latest_id
        )
    )
    
    # limit(NEARBY_VENDORS_COUNT*3)
    result = db.execute(stmt)
    return result.scalars().all()