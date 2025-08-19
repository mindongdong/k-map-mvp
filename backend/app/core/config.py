# 애플리케이션 설정 파일

# 이 파일에서 구현할 내용:
# 1. Pydantic Settings를 사용한 환경변수 관리
# 2. 데이터베이스 연결 설정
# 3. CORS 설정
# 4. JWT 보안 설정
# 5. API 버전 및 프로젝트 정보

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API 설정
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "K-map"
    
    # CORS 설정
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # 데이터베이스 설정
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "kmap_user"
    POSTGRES_PASSWORD: str = "kmap_password"
    POSTGRES_DB: str = "kmap_db"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # JWT 설정
    SECRET_KEY: str = "your-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
