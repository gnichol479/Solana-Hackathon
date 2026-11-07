@echo off
setlocal
cd /d "%~dp0"
set "PYTHON=%~dp0backend\.venv\Scripts\python.exe"
if not exist "%PYTHON%" (
  echo Please follow backend\README.md to install the shared backend first.
  pause
  exit /b 1
)
set "APP_ENV=development"
set "SOLANA_NETWORK=devnet"
set "ALLOWED_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173"
cd backend
echo Development only. Backend listening on http://127.0.0.1:8001
"%PYTHON%" -m uvicorn app.main:app --host 127.0.0.1 --port 8001
pause
