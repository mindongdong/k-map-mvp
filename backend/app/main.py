from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import datasets, admin, visualizations

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="생물학 데이터 포털 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 포함
app.include_router(datasets.router, prefix=f"{settings.API_V1_STR}/datasets", tags=["Datasets"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(visualizations.router, prefix=f"{settings.API_V1_STR}/visualizations", tags=["Visualizations"])

@app.get("/")
async def root():
    return {"message": "K-map API Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
