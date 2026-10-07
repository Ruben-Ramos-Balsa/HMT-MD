@echo off
cd /d "%~dp0"
py -3 06_VERIFICACION/verificar_integridad.py
set RESULT=%ERRORLEVEL%
pause
exit /b %RESULT%
