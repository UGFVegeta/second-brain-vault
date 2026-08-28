@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Mietverwaltung - Kontoauszug einlesen

where py >nul 2>nul
if %errorlevel%==0 (set PY=py -3) else (set PY=python)

if not exist "kontoauszuege" mkdir "kontoauszuege"

echo.
echo Es werden alle Dateien aus dem Ordner kontoauszuege gelesen.
echo.
%PY% skripte\umsaetze_importieren.py
echo.
echo Baue Dashboard neu ...
%PY% skripte\dashboard_bauen.py
echo.
pause
