@echo off
setlocal
cd /d "%~dp0"
echo Starting Payment Lens backend services and frontend...
start "Payment Lens Backend" cmd /k call "%~dp0start-backend.cmd"
start "Payment Lens Accounts" cmd /k call "%~dp0start-account-service.cmd"
call "%~dp0start-website.cmd"
