@echo off
setlocal
set SCRIPT_DIR=%~dp0
python "%SCRIPT_DIR%export_directa_history_parametric.py" --config "%SCRIPT_DIR%directa_history_export_config.json" %*
if errorlevel 1 (
    echo.
    echo Errore durante l'esportazione.
    exit /b %errorlevel%
)
echo.
echo Esportazione completata.
endlocal
