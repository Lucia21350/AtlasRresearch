# Python 베이스 이미지 사용
FROM python:3.11-slim

# R 설치
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends r-base && \
#    apt-get clean && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성
WORKDIR /app

# requirements.txt 복사 & 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

# 업로드 폴더 생성
RUN mkdir -p /app/uploads

# Flask 실행 (컨테이너는 5000번 포트 사용)
EXPOSE 5000
CMD ["python", "app.py"]
