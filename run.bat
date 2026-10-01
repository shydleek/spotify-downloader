@echo off
REM Единая точка входа для Windows
REM Просто запусти этот файл или: run.bat "ссылка_на_плейлист"

cd /d "%~dp0"

REM Ищем Python
where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo Python не найден. Установи его:
    echo   winget install Python.Python.3.12
    echo.
    pause
    exit /b 1
)

python run.py %*
if errorlevel 1 pause
