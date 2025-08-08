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
