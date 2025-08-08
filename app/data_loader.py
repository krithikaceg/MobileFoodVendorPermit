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
        # Check if data already exists
        count = db.query(VendorApplication).count()
        if count > 0:
            logger.info(f"Database already has {count} records. Skipping data load.")
            return
        
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
                    applicant_name=str(row.get('applicant_name', '')),
                    facility_type=str(row.get('facility_type', '')),
                    status=str(row.get('status', '')),
                    address=str(row.get('address', '')),
                    latitude=float(row.get('latitude', 0)) if pd.notna(row.get('latitude')) else None,
                    longitude=float(row.get('longitude', 0)) if pd.notna(row.get('longitude')) else None,
                    approved=pd.to_datetime(row.get('approved'), errors='coerce') if pd.notna(row.get('approved')) else None,
                    expiration_date=pd.to_datetime(row.get('expiration_date'), errors='coerce') if pd.notna(row.get('expiration_date')) else None
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
