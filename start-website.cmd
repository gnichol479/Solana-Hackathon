@echo off
setlocal
cd /d "%~dp0"
if exist ".tools\node-v22.14.0-win-x64\node.exe" set "PATH=%~dp0.tools\node-v22.14.0-win-x64;%PATH%"
where node >nul 2>nul
if errorlevel 1 (
  echo Please install Node.js 22 or later, then run this file again.
  pause
  exit /b 1
)
cd frontend
if not exist node_modules (
  call npm install
  if errorlevel 1 (
    pause
    exit /b 1
  )
)
if not defined VITE_API_BASE_URL set "VITE_API_BASE_URL=http://127.0.0.1:8001"
if not defined VITE_ACCOUNT_API_BASE_URL set "VITE_ACCOUNT_API_BASE_URL=http://localhost:8002"
if not defined VITE_ENABLE_DOCUMENT_UPLOAD set "VITE_ENABLE_DOCUMENT_UPLOAD=true"
call npm run dev
pause
