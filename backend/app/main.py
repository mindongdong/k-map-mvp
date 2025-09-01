import logging
import csv
import os
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import datasets, admin, visualizations
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.dataset import Dataset

# --- Database Initialization Logic ---

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'datasets.csv')

def init_db(db: Session) -> None:
    """
    Initializes the database and creates initial data if it doesn't exist.
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        logger.info("Tables checked/created.")

        # Create admin user if it doesn't exist
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            logger.info("Admin user not found, creating one...")
            admin_user = User(username="admin", hashed_password="fake_hashed_password", role="admin")
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info("Admin user created.")

        # Create datasets if they don't exist
        if db.query(Dataset).count() == 0:
            logger.info(f"No datasets found. Reading from {DATA_FILE_PATH}...")
            if not os.path.exists(DATA_FILE_PATH):
                logger.error(f"Data file not found: {DATA_FILE_PATH}")
                return

            with open(DATA_FILE_PATH, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                datasets_to_create = [
                    Dataset(
                        public_dataset_id=row['public_dataset_id'],
                        uploader_id=admin_user.user_id,
                        group_name=row['group_name'],
                        data_type=row['data_type'],
                        organ=row['organ'],
                        status=row['status'],
                        publication_date=datetime.strptime(row['publication_date'], '%Y-%m-%d').date(),
                        description=row['description'],
                        citation=row['citation'],
                        file_storage_path=row['file_storage_path']
                    ) for row in reader
                ]
            db.add_all(datasets_to_create)
            db.commit()
            logger.info(f"{len(datasets_to_create)} sample datasets created from CSV.")
        else:
            logger.info("Datasets already exist. Skipping data creation.")

    except Exception as e:
        logger.error(f"An error occurred during DB initialization: {e}")
        db.rollback()

# --- FastAPI App Definition ---

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="생물학 데이터 포털 API",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_init():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("--- Running DB Initialization on Startup ---")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("--- DB Initialization Complete ---")


# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(datasets.router, prefix=f"{settings.API_V1_STR}/datasets", tags=["Datasets"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(visualizations.router, prefix=f"{settings.API_V1_STR}/visualizations", tags=["Visualizations"])

@app.get("/")
async def root():
    return {"message": "K-map API Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
