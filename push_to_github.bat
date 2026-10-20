@echo off
title Push CarePlus MediSuite to GitHub
cd /d "%~dp0"
echo ======================================================
echo   Pushing CarePlus MediSuite to GitHub
echo   Repository: https://github.com/bbhupinder5321-lang/BBAT104_TQM_2410301011
echo ======================================================
echo.
git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Successfully pushed all commits to GitHub!
) else (
    echo.
    echo [NOTE] If you haven't created the repository on GitHub yet:
    echo 1. Open https://github.com/new in your browser
    echo 2. Set Repository name to: BBAT104_TQM_2410301011
    echo 3. Leave "Initialize with README" UNCHECKED
    echo 4. Click "Create repository", then run this script again!
)
echo.
pause
