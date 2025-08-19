# 데이터베이스 연결 및 세션 관리
#
# 이 파일에서 구현할 내용:
# 1. SQLAlchemy 엔진 설정
# 2. 데이터베이스 세션 팩토리
# 3. Base 모델 클래스
# 4. 의존성 주입용 get_db 함수
#
# 예시 구조:
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings
#
# engine = create_engine(settings.DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# def get_db():
#     """데이터베이스 세션 의존성"""
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# TODO: 위 구조를 참고하여 데이터베이스 연결을 설정하세요