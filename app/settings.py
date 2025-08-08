from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    project_name: str
    database_url: str
    search_radius_miles: float = 2.0
    nearby_vendors_count: int = 5
    approved: str = "APPROVED"
    food_truck: str = "Truck"

    class Config:
        env_file = ".env"  # optional, to load from a .env file

settings = Settings()