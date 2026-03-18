@echo off
echo ==========================================
echo   Orion-DDH_v1 Project Packager
echo ==========================================
echo.

cd /d "%~dp0"

echo Creating project ZIP for Colab upload...
echo.

:: Create zip using PowerShell (works on all Windows 10/11)
powershell -Command "Compress-Archive -Path 'main.py','buildozer.spec','screens','data','assets' -DestinationPath 'ORION-DDH-READY-FOR-BUILD.zip' -Force"

if exist "ORION-DDH-READY-FOR-BUILD.zip" (
    echo ==========================================
    echo   SUCCESS!
    echo ==========================================
    echo.
    echo Created: ORION-DDH-READY-FOR-BUILD.zip
    echo.
    echo Next steps:
    echo   1. Go to colab.research.google.com
    echo   2. Upload BUILD_APK_COLAB.ipynb
    echo   3. Run all cells
    echo   4. Upload ORION-DDH-READY-FOR-BUILD.zip when prompted
    echo   5. Wait 30-45 min for APK
    echo.
) else (
    echo ERROR: Failed to create ZIP file
)

pause
