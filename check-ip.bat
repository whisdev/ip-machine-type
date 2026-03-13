@echo off
REM Check your public/online IP address - Windows native
REM Double-click to run like .exe

set "IP="

REM Try curl first (Windows 10+ has it built-in)
where curl >nul 2>&1
if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('curl -s -m 10 https://api.ipify.org 2^>nul') do set "IP=%%i"
)
if defined IP goto :found

if %errorlevel% equ 0 (
    for /f "delims=" %%i in ('curl -s -m 10 https://icanhazip.com 2^>nul') do set "IP=%%i"
)
if defined IP goto :found

REM Fallback: PowerShell (always available on Windows)
for /f "delims=" %%i in ('powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri 'https://api.ipify.org' -UseBasicParsing -TimeoutSec 10).Content.Trim() } catch {}" 2^>nul') do set "IP=%%i"
if defined IP goto :found

for /f "delims=" %%i in ('powershell -NoProfile -Command "try { (Invoke-WebRequest -Uri 'https://icanhazip.com' -UseBasicParsing -TimeoutSec 10).Content.Trim() } catch {}" 2^>nul') do set "IP=%%i"

:found
if defined IP (
    echo Your public IP: %IP%
) else (
    echo Error: Could not fetch public IP. Check your internet connection.
    exit /b 1
)

REM Pause so window stays open when double-clicked
pause
