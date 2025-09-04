# K-MAP Project Git Convention Guide

이 문서는 K-MAP 프로젝트의 Git 워크플로우 효율성과 코드 변경 이력의 가독성을 높이기 위한 브랜치 생성 및 커밋 메시지 규칙을 정의합니다.

## 1\. Branch Naming Convention

모든 브랜치는 `main` 브랜치에서 시작하며, 작업의 목적을 명확하게 표현하기 위해 다음 구조를 따릅니다.

> **구조: `type/scope/description`**

---

### Branch Type

| Type           | 설명                           |
| :------------- | :----------------------------- |
| **`feat`**     | 새로운 기능 개발 (Feature)     |
| **`fix`**      | 버그 수정 (Bug Fix)            |
| **`refactor`** | 기능 변경 없는 코드 구조 개선  |
| **`chore`**    | 빌드, 설정 등 개발 외적인 작업 |
| **`docs`**     | 문서 작성 및 수정              |

### Branch Scope (Optional)

| Scope        | 설명                                 |
| :----------- | :----------------------------------- |
| **`fe`**     | Frontend (React)                     |
| **`be`**     | Backend (FastAPI)                    |
| **`ci`**     | CI/CD 관련 작업                      |
| **`common`** | 공통 모듈 또는 여러 영역에 걸친 작업 |

### Branch Description

- 작업 내용을 간결하게 설명합니다.
- 소문자와 하이픈(`-`)을 사용하여 작성합니다. (e.g., `create-header-component`)

---

### ✅ Branch Name Examples

```bash
# Backend: 데이터셋 목록 조회 API 기능 개발
git switch -c feat/be/implement-dataset-list-api

# Frontend: 공통 헤더 컴포넌트 구현
git switch -c feat/fe/create-header-component

# Frontend: 데이터 테이블 UI 깨짐 현상 수정
git switch -c fix/fe/dataset-table-ui-bug

# CI: Ruff 코드 스타일 검사 파이프라인 추가
git switch -c chore/ci/add-ruff-check-pipeline
```

## 2\. Commit Message Convention

프로젝트의 변경 이력을 명확하고 일관성 있게 기록하기 위해 **Conventional Commits** 명세를 따릅니다.

> **구조:**
>
> ```
> <type>(<scope>): <subject>
> <BLANK LINE>
> <body>
> <BLANK LINE>
> <footer>
> ```

---

### Header: `<type>(<scope>): <subject>`

- **`type`**: 브랜치 `type`과 동일한 키워드를 사용합니다.
- **`scope`**: 변경이 발생한 영역을 명시합니다. (`fe`, `be`, `docs` 등)
- **`subject`**:
  - 현재 시제의 동사 원형으로 시작합니다. (e.g., `Add`, `Fix`, `Change`)
  - 첫 글자는 대문자로 작성합니다.
  - 50자 이내로 간결하게 작성하며, 마침표를 찍지 않습니다.

### Body (Optional)

- 커밋의 상세한 내용을 작성합니다.
- "무엇을" 그리고 "왜" 변경했는지 설명합니다.
- 한 줄에 72자 이내로 작성하여 가독성을 높입니다.

### Footer (Optional)

- 관련된 이슈 번호를 참조할 때 사용합니다. (e.g., `Closes #123`)

---

### ✅ Commit Message Examples

- **간단한 커밋 (제목만 사용)**

  ```
  feat(be): Add basic structure for dataset list API
  ```

  ```
  docs(readme): Update project setup instructions
  ```

- **상세 커밋 (본문 포함)**

  ```
  fix(fe): Correct date format in dataset table

  The publication date in the table was not formatted correctly.
  This commit uses the 'date-fns' library to format the date string
  to 'YYYY-MM-DD' for consistency.
  ```

- **기능 구현 커밋 (백엔드)**

  ```
  feat(be): Implement GET /datasets endpoint with mock data

  - Create a Pydantic model for the dataset response.
  - Implement the basic API endpoint for fetching the dataset list.
  - Returns a static mock data array for initial frontend integration,
    as specified in the 1st-week milestone.
  ```
