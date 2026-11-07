@echo off
setlocal
cd /d "%~dp0"
if not exist ".tools\backend-env\Scripts\python.exe" (
  echo Please follow account-service\README.md to install the account service first.
  pause
  exit /b 1
)
set "LENS_INSECURE_LOCAL=1"
set "LENS_ORIGIN=http://localhost:5173"
set "LENS_RP_ID=localhost"
set "LENS_DB=%~dp0.tools\paymentlens-local.sqlite3"
cd account-service
echo Development only. Open the website at http://localhost:5173
"..\.tools\backend-env\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000
pause
