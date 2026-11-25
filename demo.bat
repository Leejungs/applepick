@echo off
chcp 65001 >nul
REM 시연용 실행 스크립트 (Docker / Elasticsearch / MariaDB 없이 동작)
REM  - 백엔드: http://localhost:50000  (SQLite + 데모 검색 저장소, 샘플 매물 자동 생성)
REM  - 프론트: http://localhost:3000
REM  - AI 어시스턴트: .env 의 OPENAI_API_KEY 만 넣으면 동작
cd /d %~dp0

if not exist .env (
  copy .env.example .env >nul
  echo [안내] .env 파일을 만들었습니다. AI 기능을 쓰려면 OPENAI_API_KEY 를 입력하세요.
)

if not exist backend\.venv (
  echo [1/2] 파이썬 가상환경 생성...
  python -m venv backend\.venv || goto :error
)
echo [1/2] 백엔드 패키지 확인/설치...
backend\.venv\Scripts\python -m pip install -q --disable-pip-version-check -r backend\requirements.txt || goto :error

if not exist frontend\node_modules\.package-lock.json (
  echo [2/2] 프론트엔드 패키지 설치...
  pushd frontend & call npm install --no-audit --no-fund & popd
)

start "ApplePick - backend" cmd /k "cd /d %~dp0backend && .venv\Scripts\python run.py"
start "ApplePick - frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 6 >nul
start http://localhost:3000
echo.
echo 실제 번개장터 매물을 추가로 수집하려면:
echo   backend\.venv\Scripts\python backend\crawler\main.py --sources bunjang --no-notify
exit /b 0

:error
echo 설치 중 오류가 발생했습니다. Python 3.12 이상, Node 20 이상이 필요합니다.
pause
exit /b 1
