# Project Structure

K-MAP 프로젝트의 아키텍처와 컨벤션을 정의합니다.

## Architecture

```
Frontend (React 18 + TypeScript)
         ↓ HTTP/REST
Backend (FastAPI + SQLAlchemy)
         ↓ SQL
Database (PostgreSQL)
```

- **Frontend**: React 18, TypeScript, React Router, Plotly.js
- **Backend**: FastAPI, SQLAlchemy ORM, Pydantic
- **Database**: PostgreSQL
- **Infrastructure**: Docker Compose

## Directory Structure

### Frontend (`frontend/src/`)

```
src/
├── components/          # 재사용 가능한 UI 컴포넌트
│   ├── Layout/          # 레이아웃 컴포넌트 (Header, Footer, Sidebar)
│   └── Visualization/   # 차트/시각화 컴포넌트
├── pages/               # 라우트별 페이지 컴포넌트
│   ├── HomePage.tsx
│   ├── DatasetsPage.jsx
│   ├── DatasetDetailPage.tsx
│   ├── VisualizationPage.tsx
│   └── AdminPage.tsx
├── services/            # API 통신 레이어
│   └── api.ts           # Axios 인스턴스 및 API 서비스
├── hooks/               # 커스텀 React 훅
│   └── useApi.ts
├── utils/               # 유틸리티 함수
│   └── formatters.ts    # 포맷팅 함수 (날짜, 숫자 등)
├── types/               # TypeScript 타입 정의
│   └── api.ts
├── styles/              # CSS 스타일
│   ├── globals.css
│   ├── layout.css
│   ├── components.css
│   └── pages.css
└── App.tsx              # 라우팅 설정
```

### Backend (`backend/app/`)

```
app/
├── api/                 # API 라우터 (도메인별 분리)
│   ├── datasets.py      # 데이터셋 CRUD
│   ├── admin.py         # 관리자 인증/관리
│   └── visualizations.py # 시각화 데이터
├── models/              # SQLAlchemy ORM 모델
│   ├── dataset.py
│   └── user.py
├── schemas/             # Pydantic 요청/응답 스키마
│   └── dataset.py
├── services/            # 비즈니스 로직
│   └── dataset_service.py
├── core/                # 핵심 설정
│   ├── config.py        # 환경설정
│   ├── database.py      # DB 연결
│   ├── security.py      # 인증/보안
│   └── dependencies.py  # 의존성 주입
└── main.py              # FastAPI 앱 진입점
```

## Routes

### Frontend Routes

| Path | Component | Description |
|------|-----------|-------------|
| `/` | HomePage | 메인 페이지 |
| `/datasets` | DatasetsPage | 데이터셋 목록 |
| `/datasets/:id` | DatasetDetailPage | 데이터셋 상세 |
| `/visualization` | VisualizationPage | 시각화 페이지 |
| `/admin` | AdminPage | 관리자 페이지 |

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/datasets` | 데이터셋 목록 조회 |
| GET | `/api/v1/datasets/{id}` | 데이터셋 상세 조회 |
| GET | `/api/v1/visualizations/umap` | UMAP 시각화 데이터 |
| POST | `/api/v1/admin/login` | 관리자 로그인 |
| POST | `/api/v1/admin/datasets` | 데이터셋 생성 |
| PUT | `/api/v1/admin/datasets/{id}` | 데이터셋 수정 |
| DELETE | `/api/v1/admin/datasets/{id}` | 데이터셋 삭제 |

## Conventions

### Frontend

#### Naming
- **컴포넌트 파일**: PascalCase (`DatasetTable.tsx`)
- **함수/변수**: camelCase (`formatDate`, `datasetList`)
- **상수**: UPPER_SNAKE_CASE (`API_BASE_URL`)
- **타입/인터페이스**: PascalCase (`Dataset`, `ApiResponse`)

#### Patterns
- 함수형 컴포넌트 + React Hooks 사용
- API 호출은 `services/api.ts` 또는 커스텀 훅 사용
- 공통 타입은 `types/` 디렉토리에 정의
- 포맷팅 함수는 `utils/formatters.ts`에 집중
- 컴포넌트별 스타일은 같은 디렉토리에 `.css` 파일로 관리

#### Imports 순서
1. React/외부 라이브러리
2. 내부 컴포넌트
3. 서비스/훅
4. 타입
5. 스타일

### Backend

#### Naming
- **파일/모듈**: snake_case (`dataset_service.py`)
- **클래스**: PascalCase (`Dataset`, `DatasetCreate`)
- **함수/변수**: snake_case (`get_datasets`, `dataset_id`)
- **상수**: UPPER_SNAKE_CASE (`API_V1_STR`)

#### Patterns
- API 함수는 `async` 사용 (FastAPI 비동기)
- 타입 힌트 필수
- Pydantic 모델로 요청/응답 스키마 정의
- SQLAlchemy ORM 사용 (raw SQL 지양)
- 비즈니스 로직은 `services/`에 분리
- 의존성 주입은 `core/dependencies.py` 사용

#### API 응답 형식
```python
# 성공
{"data": [...], "total": 10}

# 에러
{"detail": "에러 메시지"}
```

## Data Flow

### 데이터셋 조회 흐름
```
[Frontend]                    [Backend]
DatasetsPage.jsx
    ↓ useEffect
api.ts (datasetService.getDatasets)
    ↓ GET /api/v1/datasets
                              datasets.py (router)
                                  ↓
                              dataset_service.py
                                  ↓
                              models/dataset.py (ORM)
                                  ↓
                              PostgreSQL
```

### 시각화 데이터 흐름
```
[Frontend]                    [Backend]
VisualizationPage.tsx
    ↓
Visualization.jsx (Plotly.js)
    ↓ GET /api/v1/visualizations/umap
                              visualizations.py
                                  ↓
                              Plotly JSON 생성
```

## Security

- JWT 기반 관리자 인증 (`core/security.py`)
- CORS 설정 (`main.py`)
- 환경변수로 민감정보 관리 (`.env`)
- SQLAlchemy ORM으로 SQL Injection 방지
