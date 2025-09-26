import os

BASE_UPLOAD_DIR = "C:/Users/ljh86/Desktop/rServer/uploads" #"/app/uploads" # 변경: 실제 로컬/docker 경로로
os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)
