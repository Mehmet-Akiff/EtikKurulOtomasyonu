@echo off
setlocal
title Etik Kurul Otomasyonu

echo ======================================================================
echo    ETIK KURUL OTOMASYONU - MASAAUSTU UYGULAMASI
echo ======================================================================
echo.
echo Masaustu uygulamasi baslatiliyor, lutfen bekleyiniz...
echo.

set "APP_DIR=%~dp0"
set "UNPACKED_EXE=%APP_DIR%4-MasaustuUygulamasi\dist\win-unpacked\Etik Kurul Otomasyonu.exe"
set "PORTABLE_EXE=%APP_DIR%4-MasaustuUygulamasi\dist\EtikKurulOtomasyonu-Portable.exe"

if exist "%UNPACKED_EXE%" (
    echo [BILGI] Uygulama baslatiliyor: Etik Kurul Otomasyonu.exe
    start "" "%UNPACKED_EXE%"
    goto :started
)

if exist "%PORTABLE_EXE%" (
    echo [BILGI] Uygulama baslatiliyor: EtikKurulOtomasyonu-Portable.exe
    start "" "%PORTABLE_EXE%"
    goto :started
)

echo [HATA] Calistirilabilir uygulama dosyasi bulunamadi!
echo Lutfen 4-MasaustuUygulamasi klasorunu kontrol ediniz.
pause
exit /b 1

:started
echo [BILGI] Uygulama basariyla baslatildi.
exit /b 0
