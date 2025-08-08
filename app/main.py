from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
from app.db import engine, Base
from app.models import VendorApplication
from app.data_loader import load_csv_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="My FastAPI App")

# Create database tables on startup
try:
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Load initial data from CSV
    logger.info("Loading initial data...")
    load_csv_data()
    logger.info("Data loading completed")
    
except Exception as e:
    logger.error(f"Error during startup: {e}")
    raise

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Add a simple health check directly to the app
@app.get("/health")
async def health_check():
    """Simple health check"""
    try:
        from app.db import SessionLocal
        from app.models import VendorApplication
        
        db = SessionLocal()
        count = db.query(VendorApplication).count()
        db.close()
        
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

@app.get("/debug/sample-data")
async def get_sample_data():
    """Get sample data to debug what's in the database"""
    try:
        from app.db import SessionLocal
        from app.models import VendorApplication
        
        db = SessionLocal()
        
        # Get first 5 records
        samples = db.query(VendorApplication).limit(5).all()
        
        # Get facility types
        facility_types = db.query(VendorApplication.facility_type).distinct().all()
        
        db.close()
        
        return {
            "sample_records": [
                {
                    "id": record.id,
                    "applicant_name": record.applicant_name,
                    "facility_type": record.facility_type,
                    "address": record.address
                } for record in samples
            ],
            "facility_types": [ft[0] for ft in facility_types if ft[0]]
        }
    except Exception as e:
        logger.error(f"Debug endpoint failed: {e}")
        return {"error": str(e)}

@app.get("/debug/db-info")
async def get_db_info():
    """Get database connection info"""
    import os
    from app.db import DATABASE_URL
    
    return {
        "database_url_env": os.getenv("DATABASE_URL"),
        "database_url_used": DATABASE_URL,
        "working_directory": os.getcwd(),
        "files_in_dir": os.listdir(".")[:10]  # First 10 files
    }
