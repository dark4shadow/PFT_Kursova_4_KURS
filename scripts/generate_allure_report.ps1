param(
  [string]$ResultsDir = "allure-results",
  [string]$OutDir = "allure-report"
)

$ErrorActionPreference = "Stop"

function Get-LatestAllureVersion {
  $latest = Invoke-RestMethod "https://api.github.com/repos/allure-framework/allure2/releases/latest" -Headers @{ "User-Agent" = "pwsh" }
  return $latest.tag_name
}

function Ensure-AllureCli {
  param([string]$Version)

  $toolsRoot = Join-Path $PSScriptRoot "..\tools\allure"
  $toolsRoot = (Resolve-Path $toolsRoot).Path

  New-Item -ItemType Directory -Force $toolsRoot | Out-Null

  $zipPath = Join-Path $toolsRoot "allure-$Version.zip"
  $extractRoot = Join-Path $toolsRoot "allure-$Version"
  $allureBat = Join-Path $extractRoot "allure-$Version\bin\allure.bat"

  if (Test-Path $allureBat) {
    return (Resolve-Path $allureBat).Path
  }

  Write-Host "Downloading Allure CLI $Version..."

  $release = Invoke-RestMethod "https://api.github.com/repos/allure-framework/allure2/releases/tags/$Version" -Headers @{ "User-Agent" = "pwsh" }
  $asset = $release.assets | Where-Object { $_.name -eq "allure-$Version.zip" } | Select-Object -First 1
  if (-not $asset) {
    throw "Allure ZIP asset not found for version: $Version"
  }

  Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath

  if (Test-Path $extractRoot) {
    Remove-Item -Recurse -Force $extractRoot
  }

  Expand-Archive -Path $zipPath -DestinationPath $extractRoot

  if (-not (Test-Path $allureBat)) {
    throw "Allure CLI was downloaded but allure.bat not found at: $allureBat"
  }

  return (Resolve-Path $allureBat).Path
}

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot ".."))
Set-Location $projectRoot

$resultsPath = Join-Path $projectRoot $ResultsDir
if (-not (Test-Path $resultsPath)) {
  throw "Results directory not found: $resultsPath"
}

$version = Get-LatestAllureVersion
$allure = Ensure-AllureCli -Version $version

if (Test-Path $OutDir) {
  Remove-Item -Recurse -Force $OutDir
}

Write-Host "Generating report from '$ResultsDir' to '$OutDir'..."
& $allure generate $ResultsDir -o $OutDir --clean

Write-Host "Done. Report folder: $OutDir"
