from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    dataset_id = Column(Integer, primary_key=True)
    public_dataset_id = Column(String(255), unique=True, index=True, nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.user_id"))
    group_name = Column(String(255))
    data_type = Column(String(100))
    organ = Column(String(100))
    status = Column(String(50))
    publication_date = Column(Date)
    description = Column(Text)
    citation = Column(String(255))
    file_storage_path = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    uploader = relationship("User", back_populates="datasets")

    def __repr__(self):
        return f"Dataset(dataset_id={self.dataset_id}, public_dataset_id={self.public_dataset_id})"