# Single-Cell Test Frontend

k-map-mvp 단일세포 API 테스트용 프론트엔드입니다.
`KMAP/optimization_v2/frontend`에서 이식되었습니다.

## 설치

```bash
cd backend/sc_test_frontend
npm install
```

## 실행

```bash
# 1. 백엔드 먼저 실행
cd backend
uvicorn app.main:app --reload --port 8000

# 2. 프론트엔드 실행 (새 터미널)
cd backend/sc_test_frontend
npm run dev
```

## API 연결

- 백엔드: `http://localhost:8000`
- API 경로: `/api/v1/sc/*`
- Admin API: `/api/v1/sc/admin/*`

## 기능

- UMAP 시각화 (WebGL)
- 유전자 검색 및 발현 오버레이
- 클러스터 정보 표시
- 데이터셋 관리
- H5AD 파일 임포트

## 주의사항

이 프론트엔드는 **테스트/개발 용도**입니다.
실제 서비스에서는 `frontend/` 디렉토리의 메인 프론트엔드를 사용하세요.
