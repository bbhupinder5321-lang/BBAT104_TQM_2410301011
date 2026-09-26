@echo off
title Hospital Management System (HMS) - BBAT104
cd /d "%~dp0"
echo Starting High-Performance Hospital Management System...
python src\main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with an error.
    pause
)
