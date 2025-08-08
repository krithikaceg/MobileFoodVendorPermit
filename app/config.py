from pydantic_settings import BaseSettings
import os
from pathlib import Path

# Get the project root directory (parent of src)
ROOT_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    project_name: str
    database_url: str
    search_radius_miles: float = 2.0
    nearby_vendors_count: int = 5

    class Config:
        env_file = ROOT_DIR / ".env"  # Look for .env in project root
        case_sensitive = False

settings = Settings()