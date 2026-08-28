@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Mietverwaltung - Selbsttest

where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)

%PY% --version >nul 2>nul
if errorlevel 1 (
  echo.
  echo Python ist auf diesem Rechner nicht installiert.
  echo.
  echo Bitte einmalig installieren:  https://www.python.org/downloads/
  echo Beim Setup unbedingt "Add Python to PATH" ankreuzen.
  echo.
  pause
  exit /b 1
)

echo.
%PY% skripte\selbsttest.py
echo.
pause
