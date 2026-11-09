@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Curriculum Vitae Studio

REM 1. Tester runtime local embarque
if exist "%~dp0runtime\pythonw.exe" (
    start "" "%~dp0runtime\pythonw.exe" "%~dp0cv_editor_ui.py"
    exit /b 0
)
if exist "%~dp0runtime\python.exe" (
    start "" "%~dp0runtime\python.exe" "%~dp0cv_editor_ui.py"
    exit /b 0
)

REM 2. Lancer via le lanceur intelligent vbs
if exist "%~dp0run_silent.vbs" (
    wscript.exe //B //nologo "%~dp0run_silent.vbs"
    exit /b 0
)

REM 3. Tester python standard dans le PATH
where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw "%~dp0cv_editor_ui.py"
    exit /b 0
)
where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python "%~dp0cv_editor_ui.py"
    exit /b 0
)

REM 4. Secours automatique sur la version Web
if exist "%~dp0web_version\index.html" (
    start "" "%~dp0web_version\index.html"
    exit /b 0
)

echo ========================================================
echo  [ERREUR] Aucun interpreteur Python valide n a ete trouve.
echo ========================================================
echo.
pause
exit /b 1
