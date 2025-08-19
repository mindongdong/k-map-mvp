# K-map: 생물학 데이터 포털

한국인 인체 생물학 데이터를 제공하는 혁신적인 데이터 포털 MVP 프로젝트입니다.

## 🎯 프로젝트 개요

- **프로젝트명**: K-map
- **목표**: 생물학 데이터의 접근성 향상 및 최적화된 시각화 경험 제공
- **기술 스택**: React.js + FastAPI + PostgreSQL + Docker
- **개발 기간**: 4주 (MVP)

## 🏗️ 아키텍처

```
k-map-mvp/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── api/            # API 라우터
│   │   ├── core/           # 설정 및 데이터베이스
│   │   ├── models/         # SQLAlchemy 모델
│   │   └── schemas/        # Pydantic 스키마
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── components/     # 재사용 컴포넌트
│   │   ├── pages/          # 페이지 컴포넌트
│   │   ├── services/       # API 통신
│   │   └── types/          # TypeScript 타입
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml      # 개발환경 오케스트레이션
```

## 🚀 빠른 시작

### 필수 요구사항

- Docker & Docker Compose
- Git

### 개발 환경 실행

1. **프로젝트 클론**
```bash
git clone <repository-url>
cd k-map-mvp
```

2. **환경변수 설정**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. **전체 스택 실행**
```bash
docker compose up
```

4. **개별 서비스 실행**
```bash
# 프론트엔드만 실행
docker compose up frontend

# 백엔드만 실행
docker compose up backend db

# 데이터베이스만 실행
docker compose up db
```

### 접속 URL

- **프론트엔드**: http://localhost:3000
- **백엔드 API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

## 📋 주요 기능

### 사용자 기능
- **데이터셋 페이지**: 목록 조회, 필터링, 검색, 다운로드
- **시각화 페이지**: UMAP, 히트맵, 박스플롯 등 인터랙티브 차트
- **반응형 웹디자인**: 모바일/데스크톱 최적화

### 관리자 기능
- **인증 시스템**: 관리자 로그인
- **데이터 관리**: 업로드, 수정, 삭제 (CRUD)
- **파일 업로드**: .csv, .json, .h5ad 형식 지원

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 Python 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 추상화
- **PostgreSQL**: 관계형 데이터베이스
- **Pydantic**: 데이터 검증 및 직렬화
- **Plotly**: 백엔드 시각화 데이터 생성

### Frontend
- **React 18**: 최신 React + Hooks
- **TypeScript**: 타입 안전성
- **React Router**: 클라이언트 사이드 라우팅
- **Plotly.js**: 인터랙티브 데이터 시각화
- **Axios**: HTTP 클라이언트

### Infrastructure
- **Docker**: 컨테이너화
- **Docker Compose**: 멀티 컨테이너 오케스트레이션

## 🎨 UI/UX 특징

- **직관적인 인터페이스**: 연구자 친화적 디자인
- **반응형 레이아웃**: 모든 디바이스 지원
- **인터랙티브 시각화**: 확대/축소, 패닝, 호버 기능
- **빠른 로딩**: 최적화된 성능

## 📝 개발 가이드

### 코딩 컨벤션

**Backend (Python)**
- PEP 8 준수
- 타입 힌트 필수 사용
- Ruff를 통한 포매팅 및 린팅

**Frontend (TypeScript/React)**
- 함수형 컴포넌트 + Hooks 사용
- PascalCase (컴포넌트), camelCase (변수/함수)
- ESLint + Prettier 적용

### API 설계

RESTful API 설계 원칙을 따르며, 다음과 같은 주요 엔드포인트를 제공합니다:

```
GET    /api/v1/datasets              # 데이터셋 목록
GET    /api/v1/datasets/{id}         # 데이터셋 상세
GET    /api/v1/visualizations/umap   # UMAP 시각화
POST   /api/v1/admin/login           # 관리자 로그인
POST   /api/v1/admin/datasets        # 데이터셋 생성
```

## 🔒 보안

- JWT 기반 관리자 인증
- CORS 설정으로 안전한 크로스 오리진 요청
- 환경변수를 통한 민감정보 관리
- SQL Injection 방지 (SQLAlchemy ORM)

## 📊 성능 최적화

- **Backend**: 비동기 처리 (FastAPI)
- **Frontend**: 코드 스플리팅, 레이지 로딩
- **Database**: 인덱싱 및 쿼리 최적화
- **Caching**: 시각화 데이터 캐싱

## 🧪 테스트

```bash
# 백엔드 테스트
cd backend
pytest

# 프론트엔드 테스트
cd frontend
npm test
```

## 📚 참고 문서



---

**Demo 계정 정보:**
- 관리자 계정: `admin` / `admin123`