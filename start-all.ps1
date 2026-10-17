# start-all.ps1 - Tüm Modülleri Başlatma Betiği (Windows PowerShell)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "🏛️  ETİK KURUL OTOMASYONU - TÜM MODÜLLERİ BAŞLATICI" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Cyan

$baseDir = $PSScriptRoot

# PATH yenileme
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$phpBin = "C:\Users\PC\AppData\Local\Microsoft\WinGet\Packages\PHP.PHP.8.3_Microsoft.Winget.Source_8wekyb3d8bbwe\php.exe"
if (-not (Test-Path $phpBin)) {
    $phpCmd = Get-Command php -ErrorAction SilentlyContinue
    if ($phpCmd) { $phpBin = $phpCmd.Source }
}

Write-Host "`n[1/3] Modül 1 Başlatılıyor: ASP.NET Core (.NET 9) + MSSQL..." -ForegroundColor Green
$dotNetProc = Start-Process -FilePath "dotnet" -ArgumentList "run --urls http://localhost:5001" -WorkingDirectory "$baseDir\1-BasvuruModulu_DotNet" -PassThru

Write-Host "[2/3] Modül 2 Başlatılıyor: PHP + MySQL/SQLite..." -ForegroundColor Green
$phpProc = Start-Process -FilePath $phpBin -ArgumentList "-S localhost:5002 index.php" -WorkingDirectory "$baseDir\2-DegerlendirmeModulu_PHP" -PassThru

Write-Host "[3/3] Modül 3 Başlatılıyor: Node.js (Express) + MongoDB..." -ForegroundColor Green
$nodeProc = Start-Process -FilePath "node" -ArgumentList "src/server.js" -WorkingDirectory "$baseDir\3-KararVeBelgeModulu_Node" -PassThru -Environment @{ PORT = "5003" }

Start-Sleep -Seconds 3

Write-Host "`n✅ Tüm Modüller Başarıyla Başlatıldı!" -ForegroundColor Cyan
Write-Host "----------------------------------------------------------"
Write-Host "📌 Modül 1 (Başvuru & Evrak - ASP.NET Core):  http://localhost:5001/api/applications" -ForegroundColor White
Write-Host "📌 Modül 2 (Değerlendirme Portalı - PHP):     http://localhost:5002" -ForegroundColor White
Write-Host "📌 Modül 3 (Karar & Belge Portalı - Node.js): http://localhost:5003" -ForegroundColor White
Write-Host "----------------------------------------------------------"
Write-Host "Uçtan uca otomatik testi çalıştırmak için: .\test-workflow.ps1" -ForegroundColor Yellow
Write-Host "Servisleri durdurmak için bu pencereyi kapatabilir veya stop komutu verebilirsiniz.`n"
