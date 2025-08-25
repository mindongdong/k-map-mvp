# 애플리케이션 설정 파일

# 이 파일에서 구현할 내용:
# 1. Pydantic Settings를 사용한 환경변수 관리
# 2. 데이터베이스 연결 설정
# 3. CORS 설정
# 4. JWT 보안 설정
# 5. API 버전 및 프로젝트 정보

from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "K-map"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # CORS 설정
    # 문자열로 받은 후, 파싱하여 리스트로 사용
    CORS_ORIGINS: str

    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # 데이터베이스 설정
    POSTGRES_SERVER: str = "db"
    POSTGRES_USER: str = "kmap_user"
    POSTGRES_PASSWORD: str = "kmap_password"
    POSTGRES_DB: str = "kmap_db"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # JWT 설정
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 관리자 계정
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin123"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
