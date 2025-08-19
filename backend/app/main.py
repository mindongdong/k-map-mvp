from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="K-map API", description="생물학 데이터 포털 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "K-map API Server is running!"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/v1/datasets")
async def get_datasets():
    return {
        "datasets": [
            {
                "id": "DS001",
                "group": "Research Group A",
                "dataType": "RNA-seq",
                "organ": "Liver",
                "status": "Published",
                "publicationDate": "2024-08-01"
            }
        ]
    }