@echo off
cd /d "%~dp0"
py -3 -I -B -S verificar_integridad.py
set result=%errorlevel%
pause
exit /b %result%
