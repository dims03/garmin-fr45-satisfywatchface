@echo off
setlocal
title SATISFY FR45 - Simulator Garmin
set "taskRoot=%~dp0"
set "sdkBin=%taskRoot%.tools\sdk\bin"
set "watchFile=%taskRoot%output\SATISFY-FR45.prg"
set "javaExe=C:\Program Files\Android\Android Studio\jbr\bin\java.exe"

if not exist "%javaExe%" (
    echo Java tidak ditemukan di lokasi Android Studio.
    echo Sesuaikan javaExe pada file peluncur ini ke lokasi java.exe Anda.
    pause
    exit /b 1
)
if not exist "%sdkBin%\simulator.exe" (
    echo SDK Garmin tidak ditemukan di folder proyek .tools\sdk.
    pause
    exit /b 1
)
if not exist "%watchFile%" (
    echo File output\SATISFY-FR45.prg tidak ditemukan.
    pause
    exit /b 1
)

tasklist /FI "IMAGENAME eq simulator.exe" /NH | findstr /I /C:"simulator.exe" >nul
if errorlevel 1 (
    echo Membuka simulator Garmin...
    start "" /D "%sdkBin%" "%sdkBin%\simulator.exe"
    timeout /t 3 /nobreak >nul
)

echo Menjalankan watch face SATISFY untuk Forerunner 45...
echo Biarkan jendela ini terbuka selama pengujian.
"%javaExe%" -classpath "%sdkBin%\monkeybrains.jar" com.garmin.monkeybrains.monkeydodeux.MonkeyDoDeux -f "%watchFile%" -d fr45 -s "%sdkBin%\shell.exe"
if errorlevel 1 (
    echo.
    echo Simulator belum siap atau koneksi gagal.
    echo Pastikan jendela simulator sudah terbuka, lalu coba jalankan lagi.
    pause
    exit /b 1
)
endlocal
