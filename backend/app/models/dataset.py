# Dataset SQLAlchemy 모델
#
# 이 파일에서 구현할 내용:
# 1. Dataset 테이블 정의
# 2. 컬럼 정의 (id, dataset_id, group, data_type, organ, status, etc.)
# 3. 관계 설정 (필요한 경우)
# 4. 인덱스 설정
#
# 예시 구조:
# from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
# from sqlalchemy.sql import func
# from app.core.database import Base
#
# class Dataset(Base):
#     __tablename__ = "datasets"
#     
#     id = Column(Integer, primary_key=True, index=True)
#     dataset_id = Column(String(100), unique=True, index=True, nullable=False)
#     group = Column(String(100), nullable=False)
#     data_type = Column(String(50), nullable=False)
#     organ = Column(String(50), nullable=False)
#     status = Column(String(20), default="active")
#     description = Column(Text)
#     citation = Column(Text)
#     publication_date = Column(DateTime, nullable=False)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     
#     # JSON 형태의 메타데이터
#     technical_metadata = Column(JSON, default={})

# TODO: 위 구조를 참고하여 Dataset 모델을 정의하세요