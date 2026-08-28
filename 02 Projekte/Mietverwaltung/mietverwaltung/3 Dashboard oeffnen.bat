@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Mietverwaltung - Dashboard

where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)

%PY% skripte\dashboard_bauen.py
if errorlevel 1 (
  echo.
  echo Das Dashboard konnte nicht gebaut werden. Bitte Claude die Meldung zeigen.
  echo.
  pause
  exit /b 1
)

start "" "Dashboard.html"
