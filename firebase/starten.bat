@echo off
chcp 65001 >nul
title SPIKE Bridge Starter
color 0A

:check_path
echo.
echo ┌──────────────────────────────────────────┐
echo │   Prüfe Pfad...                          │
echo └──────────────────────────────────────────┘

set "BRIDGE_PATH=C:\Users\zinssejo\Documents\Unearthed_FLL\pybricks\Unearthed\firebase"
set "BRIDGE_FILE=%BRIDGE_PATH%\bridge_firebase.py"

echo.
echo SUCHEN IN:
echo %BRIDGE_PATH%
echo.

if not exist "%BRIDGE_PATH%" (
    echo ❌ PFAD EXISTIERT NICHT!
    echo.
    echo Der angegebene Pfad wurde nicht gefunden.
    echo Bitte überprüfe: %BRIDGE_PATH%
    echo.
    pause
    exit /b 1
)

echo ✓ Pfad existiert

if not exist "%BRIDGE_FILE%" (
    echo.
    echo ❌ BRIDGE-DATEI NICHT GEFUNDEN!
    echo Gesucht: bridge_firebase.py
    echo Inhalt von %BRIDGE_PATH%:
    dir /b "%BRIDGE_PATH%"
    echo.
    echo Bitte stelle sicher, dass bridge_firebase.py vorhanden ist.
    echo.
    pause
    exit /b 1
)

echo ✓ Bridge-Datei gefunden: bridge_firebase.py
echo.

cd /d "%BRIDGE_PATH%"
echo ARBEITSVERZEICHNIS:
echo %cd%
echo.

:menu
cls
echo.
echo ╔══════════════════════════════════════════╗
echo ║         SPIKE BRIDGE STARTER             ║
echo ╠══════════════════════════════════════════╣
echo ║  1. Bridge starten (bridge_firebase.py)  ║
echo ║  2. Bridge beenden (alle Python Prozesse)║
echo ║  3. Ordner öffnen                        ║
echo ║  4. Dateien anzeigen                     ║
echo ║  5. Python Version prüfen                ║
echo ║  6. Beenden                              ║
echo ╚══════════════════════════════════════════╝
echo.
echo Aktueller Pfad: %BRIDGE_PATH%
echo Bridge-Datei: bridge_firebase.py
echo.
set /p choice="Wähle (1-6): "

if "%choice%"=="1" goto start
if "%choice%"=="2" goto stop
if "%choice%"=="3" goto openfolder
if "%choice%"=="4" goto showfiles
if "%choice%"=="5" goto checkpython
if "%choice%"=="6" goto exit

goto menu

:start
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Starte Bridge...                       │
echo └──────────────────────────────────────────┘
echo.
echo PFAD: %BRIDGE_PATH%
echo DATEI: bridge_firebase.py
echo.
echo STRG+C zum Beenden der Bridge
echo.
echo -----------------------
python bridge_firebase.py
echo -----------------------
echo.
echo Bridge beendet.
pause
goto menu

:stop
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Stoppe Bridge...                       │
echo └──────────────────────────────────────────┘
echo.
echo Aktive Python-Prozesse:
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find "python.exe" >nul
if errorlevel 1 (
    echo Keine Python-Prozesse gefunden.
) else (
    tasklist /FI "IMAGENAME eq python.exe"
    echo.
    taskkill /F /IM python.exe 2>nul
    echo ✓ Alle Python-Prozesse wurden gestoppt.
)
echo.
pause
goto menu

:openfolder
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Öffne Ordner...                        │
echo └──────────────────────────────────────────┘
echo.
echo Öffne: %BRIDGE_PATH%
explorer "%BRIDGE_PATH%"
echo.
goto menu

:showfiles
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Dateien im Ordner:                     │
echo └──────────────────────────────────────────┘
echo.
echo PFAD: %BRIDGE_PATH%
echo.
echo Dateien:
dir /b "%BRIDGE_PATH%"
echo.
echo Bridge-Datei: 
if exist "%BRIDGE_FILE%" (
    echo ✓ bridge_firebase.py gefunden (%BRIDGE_FILE%)
) else (
    echo ❌ bridge_firebase.py NICHT gefunden!
)
echo.
pause
goto menu

:checkpython
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Python Version prüfen...               │
echo └──────────────────────────────────────────┘
echo.
python --version
echo.
echo Python Pfad: %PYTHONPATH%
echo.
echo Module prüfen:
python -c "import requests; print('✓ requests installiert')" 2>nul || echo "❌ requests nicht installiert"
python -c "import sys; print('✓ Python', sys.version)" 2>nul || echo "❌ Python nicht gefunden"
echo.
pause
goto menu

:exit
cls
echo.
echo ┌──────────────────────────────────────────┐
echo │   Auf Wiedersehen!                       │
echo └──────────────────────────────────────────┘
echo.
echo Bridge-Pfad: %BRIDGE_PATH%
echo Bridge-Datei: bridge_firebase.py
echo.
timeout /t 2 >nul
exit