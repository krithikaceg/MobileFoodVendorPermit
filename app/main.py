from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
from app.db import engine, Base
from app.models import VendorApplication
from app.data_loader import load_csv_data

app = FastAPI(title="My FastAPI App")

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Load initial data from CSV
load_csv_data()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
