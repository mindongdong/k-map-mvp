from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='user')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    datasets = relationship("Dataset", back_populates="uploader")

class Dataset(Base):
    __tablename__ = "datasets"
    
    dataset_id = Column(Integer, primary_key=True, index=True)
    public_dataset_id = Column(String(255), unique=True, index=True, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    group_name = Column(String(255), nullable=False)
    data_type = Column(String(100), nullable=False)
    organ = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="private")
    publication_date = Column(Date)
    description = Column(Text)
    citation = Column(String(255))
    file_storage_path = Column(String(255), nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    uploader = relationship("User", back_populates="datasets")
