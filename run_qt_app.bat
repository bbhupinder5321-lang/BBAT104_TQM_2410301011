@echo off
title CarePlus MediSuite - City Care Hospital (PySide6 UI) - BBAT104
cd /d "%~dp0"
echo Starting CarePlus MediSuite - Hospital & Queue Management System...
echo Student: Bhupinder Singh ^| Roll No: 2410301011 ^| CSE - A
echo Quality Goal: Q02 - Improve Performance
python qt_main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application exited with an error.
    pause
)
