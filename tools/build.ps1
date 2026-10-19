param(
    [string]$SdkPath = '',
    [string]$JavaPath = '',
    [switch]$DebugBuild,
    [switch]$UnitTests
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

if (-not $SdkPath) {
    $localSdk = Join-Path $projectRoot '.tools\sdk'
    $currentSdk = Join-Path $env:APPDATA 'Garmin\ConnectIQ\current-sdk.cfg'
    if (Test-Path -LiteralPath $currentSdk) {
        $SdkPath = (Get-Content -LiteralPath $currentSdk -Raw).Trim()
    } elseif (Test-Path -LiteralPath $localSdk) {
        $SdkPath = $localSdk
    } else {
        throw 'Install Garmin Connect IQ SDK through SDK Manager first, or supply -SdkPath.'
    }
}
if (-not $JavaPath) {
    $javaCommand = Get-Command java -ErrorAction SilentlyContinue
    $androidJava = 'C:\Program Files\Android\Android Studio\jbr\bin\java.exe'
    if ($javaCommand) { $JavaPath = $javaCommand.Source }
    elseif (Test-Path -LiteralPath $androidJava) { $JavaPath = $androidJava }
    else { throw 'Java is required. Supply -JavaPath to java.exe.' }
}

$deviceFile = Join-Path $env:APPDATA 'Garmin\ConnectIQ\Devices\fr45\compiler.json'
if (-not (Test-Path -LiteralPath $deviceFile)) {
    throw 'FR45 profile is missing. Sign into Garmin SDK Manager, open Devices, download Forerunner 45, then rerun this script.'
}
$privateDir = Join-Path $projectRoot '.private'
New-Item -ItemType Directory -Path $privateDir -Force | Out-Null
$keyPath = Join-Path $privateDir 'developer_key.der'
if (-not (Test-Path -LiteralPath $keyPath)) {
    $rsa = [System.Security.Cryptography.RSA]::Create(4096)
    try { [IO.File]::WriteAllBytes($keyPath, $rsa.ExportPkcs8PrivateKey()) }
    finally { $rsa.Dispose() }
}
New-Item -ItemType Directory -Path 'output' -Force | Out-Null
$outputPath = 'output\SATISFY-FR45.prg'
if ($UnitTests) {
    New-Item -ItemType Directory -Path 'bin' -Force | Out-Null
    $outputPath = 'bin\SATISFY-FR45-tests.prg'
}
$jarPath = Join-Path $SdkPath 'bin\monkeybrains.jar'
$buildArgs = @('-jar', $jarPath, '-f', 'monkey.jungle', '-d', 'fr45', '-o', $outputPath, '-y', $keyPath, '-w', '-O', 'z')
if ($UnitTests) { $buildArgs += '-t' }
elseif (-not $DebugBuild) { $buildArgs += '-r' }
& $JavaPath @buildArgs
if ($LASTEXITCODE -ne 0) { throw ('Garmin compiler failed with exit code ' + $LASTEXITCODE) }
Get-FileHash -LiteralPath $outputPath -Algorithm SHA256
Write-Host ('Built ' + $outputPath + ' for Forerunner 45.')
