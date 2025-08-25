
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default='admin')
    created_at = Column(TIMESTAMP, server_default=func.now())

    datasets = relationship("Dataset", back_populates="uploader")

    def __repr__(self):
        return f"User(user_id={self.user_id}, username={self.username}, role={self.role})"
