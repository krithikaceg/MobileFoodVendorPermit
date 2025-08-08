import pandas as pd
import os
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import VendorApplication
import logging

logger = logging.getLogger(__name__)

def load_csv_data():
    """Load data from CSV file into the database if the table is empty"""
    
    db = SessionLocal()
    try:
        # Check if data already exists and is valid
        count = db.query(VendorApplication).count()
        if count > 0:
            # Check if existing data is valid (has non-empty names)
            valid_count = db.query(VendorApplication).filter(VendorApplication.applicant_name != '').count()
            if valid_count > 0:
                logger.info(f"Database already has {valid_count} valid records. Skipping data load.")
                return
            else:
                logger.info(f"Found {count} empty records. Clearing and reloading data.")
                db.query(VendorApplication).delete()
                db.commit()
        
        logger.info("Loading data from CSV file...")
        
        # Read CSV file
        csv_file = "Mobile_Food_Facility_Permit_2.csv"
        if not os.path.exists(csv_file):
            logger.warning(f"CSV file {csv_file} not found. Skipping data load.")
            return
            
        df = pd.read_csv(csv_file)
        logger.info(f"Found {len(df)} records in CSV file")
        
        # Insert data into database
        records_inserted = 0
        for _, row in df.iterrows():
            try:
                vendor = VendorApplication(
                    applicant_name=str(row.get('Name', '')),
                    facility_type=str(row.get('FacilityType', '')),
                    status=str(row.get('Status', '')),
                    address=str(row.get('Address', '')),
                    latitude=float(row.get('Latitude', 0)) if pd.notna(row.get('Latitude')) else None,
                    longitude=float(row.get('Longitude', 0)) if pd.notna(row.get('Longitude')) else None,
                    approved=pd.to_datetime(row.get('Approved'), errors='coerce') if pd.notna(row.get('Approved')) else None,
                    expiration_date=pd.to_datetime(row.get('ExpirationDate'), errors='coerce') if pd.notna(row.get('ExpirationDate')) else None
                )
                db.add(vendor)
                records_inserted += 1
            except Exception as e:
                logger.warning(f"Error inserting record: {e}")
                continue
        
        db.commit()
        logger.info(f"Successfully loaded {records_inserted} records into the database")
        
    except Exception as e:
        logger.error(f"Error loading CSV data: {e}")
        db.rollback()
    finally:
        db.close()
