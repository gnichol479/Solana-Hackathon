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
call npm run dev
pause
