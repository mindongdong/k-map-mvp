#!/usr/bin/env python3
"""
Database seeding script for K-map project
Seeds the database with initial admin user and datasets from CSV file
"""

import csv
import sys
import os
from datetime import datetime, date
from pathlib import Path

# Add the app directory to Python path
sys.path.append('/app')

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from passlib.context import CryptContext

from app.core.config import settings
from app.models.user import User
from app.models.dataset import Dataset

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_database():
    """Seed database with initial data"""
    
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("👤 Creating admin user...")
            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin_password"),
                role="admin"
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Admin user created with ID: {admin_user.user_id}")
        else:
            print(f"👤 Admin user already exists with ID: {admin_user.user_id}")
        
        # Check if datasets already exist
        existing_count = db.query(Dataset).count()
        if existing_count > 0:
            print(f"📊 {existing_count} datasets already exist in database")
            return
        
        # Read CSV file and seed datasets
        csv_file_path = "/app/datasets.csv"
        if not os.path.exists(csv_file_path):
            print(f"❌ CSV file not found: {csv_file_path}")
            return
        
        print(f"📁 Reading datasets from: {csv_file_path}")
        
        datasets_created = 0
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Skip empty rows
                if not row.get('public_dataset_id'):
                    continue
                
                # Parse publication date
                try:
                    pub_date = datetime.strptime(row['publication_date'], '%Y-%m-%d').date()
                except ValueError:
                    pub_date = date.today()
                
                # Create dataset
                dataset = Dataset(
                    public_dataset_id=row['public_dataset_id'],
                    uploader_id=admin_user.user_id,
                    group_name=row['group_name'],
                    data_type=row['data_type'],
                    organ=row['organ'],
                    status=row['status'],
                    publication_date=pub_date,
                    description=row['description'],
                    citation=row['citation'],
                    file_storage_path=row['file_storage_path']
                )
                
                db.add(dataset)
                datasets_created += 1
        
        # Commit all datasets
        db.commit()
        print(f"✅ Successfully created {datasets_created} datasets")
        
        # Verify data
        total_datasets = db.query(Dataset).count()
        total_users = db.query(User).count()
        
        print("🎯 Database seeding completed!")
        print(f"📊 Total datasets in database: {total_datasets}")
        print(f"👥 Total users in database: {total_users}")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()