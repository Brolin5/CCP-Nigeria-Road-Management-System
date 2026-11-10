import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nigeria Road Management System (NRMS)"
    PROJECT_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:ADA2019ry%40com@localhost:3306/nrms_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "nrms-super-secret-key-2026-production-grade")
    ALERTS_OVERDUE_DAYS: int = int(os.getenv("ALERTS_OVERDUE_DAYS", "30"))
    DUPLICATE_RADIUS_METERS: float = float(os.getenv("DUPLICATE_RADIUS_METERS", "100.0"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
