# Single-Cell Visualization API

K-map MVP 백엔드의 단일세포 시각화 API 문서입니다.

## 개요

이 모듈은 `KMAP/optimization_v2` 프로젝트의 단일세포 시각화 기능을 통합하여 RESTful API로 제공합니다.

### 주요 기능
- UMAP 좌표 시각화
- 마커 유전자 조회
- 유전자 발현 오버레이
- 클러스터 통계
- H5AD 파일 임포트

---

## 데이터베이스 스키마

### 새 테이블

| 테이블 | 설명 |
|--------|------|
| `sc_datasets` | 단일세포 데이터셋 메타데이터 |
| `cells` | 세포 정보 및 UMAP 좌표 |
| `genes` | 유전자 정보 |
| `marker_genes` | 클러스터별 마커 유전자 |
| `gene_expression` | 유전자 발현 데이터 (sparse) |
| `cluster_stats` | 클러스터 통계 |
| `umap_view` | UMAP 조회용 Materialized View |

### 마이그레이션 실행

```bash
cd backend
alembic upgrade head
```

---

## API 엔드포인트

### 시각화 API (`/api/v1/sc/`)

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/datasets` | GET | 데이터셋 목록 조회 |
| `/datasets/{name}` | GET | 데이터셋 상세 정보 |
| `/umap/{name}` | GET | UMAP 좌표 조회 |
| `/umap/{name}/region` | GET | UMAP 영역 선택 |
| `/markers/{name}` | GET | 마커 유전자 조회 |
| `/clusters/{name}` | GET | 클러스터 통계 |
| `/clusters/{name}/{cluster_id}/genes` | GET | 클러스터별 유전자 |
| `/expression/{name}/{gene}` | GET | 유전자 발현 오버레이 |
| `/genes/{name}/search` | GET | 유전자 검색 |

### 관리자 API (`/api/v1/sc/admin/`)

| 엔드포인트 | 메서드 | 설명 | 인증 |
|-----------|--------|------|------|
| `/import` | POST | H5AD 파일 임포트 | 필수 |
| `/import/overwrite` | POST | 덮어쓰기 임포트 | 필수 |
| `/datasets/{name}` | DELETE | 데이터셋 삭제 | 필수 |
| `/datasets/{name}/status` | GET | 임포트 상태 조회 | 필수 |
| `/refresh-view` | POST | Materialized View 갱신 | 필수 |

---

## 사용 예시

### UMAP 데이터 조회

```bash
# 전체 데이터
GET /api/v1/sc/umap/my_dataset

# 특정 클러스터만
GET /api/v1/sc/umap/my_dataset?cluster_ids=0,1,2

# 샘플링 (대용량 데이터셋용)
GET /api/v1/sc/umap/my_dataset?sample_rate=0.5
```

### 마커 유전자 조회

```bash
# 전체 클러스터 상위 25개
GET /api/v1/sc/markers/my_dataset

# 특정 클러스터 상위 50개
GET /api/v1/sc/markers/my_dataset?cluster_id=0&top_n=50
```

### 유전자 발현 오버레이

```bash
GET /api/v1/sc/expression/my_dataset/CD3D
```

### 유전자 검색

```bash
GET /api/v1/sc/genes/my_dataset/search?q=CD&limit=20
```

### H5AD 파일 임포트 (관리자)

```bash
POST /api/v1/sc/admin/import
Content-Type: application/json
Authorization: Bearer <token>

{
  "file_path": "/data/sample.h5ad",
  "name": "my_dataset",
  "import_expression": false,
  "n_top_genes": 100
}
```

---

## 파일 구조

```
backend/
├── alembic/versions/
│   ├── a1b2c3d4e5f6_add_single_cell_tables.py
│   └── b2c3d4e5f6a7_add_umap_materialized_view.py
├── app/
│   ├── api/
│   │   ├── sc_visualizations.py    # 시각화 API
│   │   └── sc_admin.py             # 관리자 API
│   ├── models/
│   │   └── single_cell.py          # SQLAlchemy 모델
│   ├── schemas/
│   │   └── single_cell.py          # Pydantic 스키마
│   └── services/
│       ├── visualization_service.py # 시각화 쿼리 서비스
│       └── import_service.py        # H5AD 임포트 서비스
└── tests/
    └── test_sc_api.py              # API 테스트
```

---

## 의존성

`requirements.txt`에 추가된 패키지:

```
scanpy>=1.9.0
anndata>=0.9.0
scipy>=1.10.0
tqdm>=4.65.0
```

---

## 성능 최적화

- **Materialized View**: `umap_view`를 사용하여 UMAP 조회 성능 향상
- **배치 처리**: 대용량 데이터 임포트 시 2000개 단위 배치 처리
- **샘플링**: `sample_rate` 파라미터로 대용량 데이터셋 샘플링 지원

### Materialized View 갱신

데이터 임포트 후 자동으로 갱신됩니다. 수동 갱신이 필요한 경우:

```bash
POST /api/v1/sc/admin/refresh-view
```

---

## 데이터 마이그레이션

기존 `optimization_v2` PostgreSQL에서 데이터를 마이그레이션하는 방법입니다.

### 사전 조건

1. k-map-mvp Docker 컨테이너 실행 중
2. optimization_v2 Docker 컨테이너 실행 중 (또는 DB 접근 가능)

### 마이그레이션 실행

```bash
# 1. 테이블 생성 (최초 1회)
cd backend
alembic upgrade head

# 2. 환경변수 설정
export SOURCE_DB_PASSWORD=<optimization_v2_db_password>

# 3. 마이그레이션 스크립트 실행
python scripts/migrate_sc_data.py
```

### 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SOURCE_DB_HOST` | localhost | 소스 DB 호스트 |
| `SOURCE_DB_PORT` | 5432 | 소스 DB 포트 |
| `SOURCE_DB_NAME` | kmap_visualization | 소스 DB 이름 |
| `SOURCE_DB_USER` | kmap | 소스 DB 사용자 |
| `SOURCE_DB_PASSWORD` | (필수) | 소스 DB 비밀번호 |

### 마이그레이션 내용

스크립트가 자동으로 처리하는 항목:
- `datasets` → `sc_datasets` 테이블명 변환
- `cells`, `genes`, `marker_genes`, `cluster_stats` 데이터 복사
- `gene_expression` 데이터 복사 (있는 경우)
- ID 매핑 처리 (외래 키 관계 유지)
- Materialized View 자동 갱신

---

## SQL 덤프 파일 복원

이미 덤프 파일이 있는 경우 직접 복원할 수 있습니다.

### 생성된 파일

| 파일 | 설명 |
|------|------|
| `scripts/sc_data_dump.sql` | optimization_v2 원본 덤프 |
| `scripts/sc_data_converted.sql` | 테이블명 변환된 덤프 (sc_datasets) |
| `scripts/restore_sc_data.py` | 복원 스크립트 |

### 복원 방법

#### 방법 1: Python 스크립트 사용

```bash
# 1. k-map-mvp 테이블 생성
cd backend
alembic upgrade head

# 2. 환경변수 설정
export TARGET_DB_PASSWORD=<password>

# 3. 복원 실행
python scripts/restore_sc_data.py \
  --target-host localhost \
  --target-port 5432 \
  --target-db kmap \
  --target-user kmap
```

#### 방법 2: Docker 컨테이너로 직접 복원

```bash
# 1. k-map-mvp Docker 시작
cd c:/Projects/k-map-mvp
docker-compose up -d postgres

# 2. 마이그레이션 실행
cd backend
alembic upgrade head

# 3. 덤프 파일 복사 및 복원
docker cp scripts/sc_data_converted.sql kmap-postgres:/tmp/
docker exec -it kmap-postgres psql -U kmap -d kmap -f /tmp/sc_data_converted.sql

# 4. Materialized View 갱신
docker exec -it kmap-postgres psql -U kmap -d kmap -c \
  "REFRESH MATERIALIZED VIEW umap_view;"
```

### 복원 스크립트 옵션

```bash
python scripts/restore_sc_data.py --help

# 옵션:
#   --input          입력 덤프 파일 (기본: sc_data_dump.sql)
#   --convert-only   변환만 실행, 복원 안함
#   --target-host    타겟 PostgreSQL 호스트 (기본: localhost)
#   --target-port    타겟 PostgreSQL 포트 (기본: 5432)
#   --target-db      타겟 데이터베이스 이름 (기본: kmap)
#   --target-user    타겟 데이터베이스 사용자 (기본: kmap)
```

### 데이터 용량

현재 덤프 파일 통계:
- 파일 크기: 약 54만 줄
- 포함 데이터셋: 10개 (pbmc3k, CRCtotal, breast_20_c 등)
- 총 세포 수: 약 50만 개
