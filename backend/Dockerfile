# Backend Docker 설정
# 
# 이 파일에서 구현할 내용:
# 1. Python 베이스 이미지 설정
# 2. 작업 디렉토리 설정
# 3. 의존성 설치 (requirements.txt)
# 4. 애플리케이션 코드 복사
# 5. 개발 서버 실행 설정
#
# 예시 구조:
# FROM python:3.11-slim
#
# WORKDIR /app
#
# # 시스템 의존성 설치
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*
#
# # Python 의존성 설치
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
#
# # 애플리케이션 코드 복사
# COPY . .
#
# # 개발 모드에서 실행
# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# TODO: 위 구조를 참고하여 Backend Dockerfile을 작성하세요