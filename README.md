## R 자동화 - prediction

venv/docker로 실행 
(venv - R은 로컬에 설치된 R-4.1.2사용)

api 요청(로컬): http://127.0.0.1:5000/prediction
- Body: form-data
- research_id | text
- file | zip 파일

## Prediction API 동작 과정

### 1. API 요청 수신
- 클라이언트로부터 `prediction.zip` 파일을 받음

### 2. 압축 해제
- `/uploads` 폴더에 압축 해제
- 압축 해제된 폴더명은 `research_id`로 지정

### 3. 환경 준비
- 압축 해제 경로에 `postgresql-42.6.0.jar` 파일 복사
- 기존 `renv` 폴더 삭제
- `.Rprofile` 내용만 삭제
- `renv.lock` 파일 삭제

### 4. R 스크립트 생성 및 실행
- `prediction_script.R` 파일 생성
- `extracted_main_dir`에서 `.Rproj` 파일명(패키지 이름) 추출
- 생성된 `prediction_script.R` 실행

> ⚠️ (2025-09-26 현재까지 구현 단계)

### 5. 결과 처리
- 생성된 결과 파일을 서버에 업로드
- URL을 백엔드에 반환
- 백엔드 API 요청 성공 시 `./uploads/research_id` 폴더 삭제
