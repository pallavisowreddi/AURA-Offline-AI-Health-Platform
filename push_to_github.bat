@echo off
echo ======================================================================
echo  Pushing AURA to GitHub (https://github.com/pallavisowreddi/AURA-Offline-AI-Health-Platform)
echo ======================================================================
echo.

git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo  SUCCESS! Repository published to GitHub:
    echo  https://github.com/pallavisowreddi/AURA-Offline-AI-Health-Platform
    echo ======================================================================
) else (
    echo.
    echo ======================================================================
    echo  [ACTION NEEDED]: The repository is not yet created on GitHub.com!
    echo.
    echo  1. Open this pre-filled link in your browser:
    echo     https://github.com/new?name=AURA-Offline-AI-Health-Platform
    echo.
    echo  2. Click the green "Create repository" button.
    echo     (Leave "Add a README" UNCHECKED since code is already committed)
    echo.
    echo  3. Run this script (push_to_github.bat) again to push!
    echo ======================================================================
)

echo.
pause
