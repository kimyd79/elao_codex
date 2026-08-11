param(
    [string]$Python = 'python',
    [string]$PostgresBin = ''
)

. (Join-Path $PSScriptRoot 'windows-common.ps1')
Import-EaloEnvironment
Enable-EaloNode

$detectedPython = & $Python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>$null
if ($detectedPython -ne '3.8') {
    throw "Python 3.8 is required; detected '$detectedPython'. Pass its full path with -Python."
}

$venv = Join-Path $script:RepoRoot '.venv'
if (-not (Test-Path -LiteralPath $venv)) {
    & $Python -m venv $venv
}
$venvPython = Join-Path $venv 'Scripts\python.exe'
& $venvPython -m pip install --upgrade "pip<25" "setuptools<70" wheel
& $venvPython -m pip install -r (Join-Path $script:RepoRoot 'EALO\backend\requirements.runtime.txt')

if (-not $PostgresBin) {
    $installRoot = 'C:\Program Files\PostgreSQL'
    if (Test-Path -LiteralPath $installRoot) {
        $PostgresBin = Get-ChildItem -LiteralPath $installRoot -Directory |
            Sort-Object { [version]$_.Name } -Descending |
            ForEach-Object { Join-Path $_.FullName 'bin' } |
            Where-Object { Test-Path (Join-Path $_ 'psql.exe') } |
            Select-Object -First 1
    }
}
if (-not $PostgresBin -or -not (Test-Path (Join-Path $PostgresBin 'psql.exe'))) {
    throw 'PostgreSQL tools were not found. Install PostgreSQL, then pass -PostgresBin "C:\Program Files\PostgreSQL\16\bin".'
}

$env:PGPASSWORD = $env:POSTGRES_PASSWORD
$psql = Join-Path $PostgresBin 'psql.exe'
$createdb = Join-Path $PostgresBin 'createdb.exe'
$existsOutput = & $psql -X -w -v ON_ERROR_STOP=1 `
    -h $env:POSTGRES_HOST `
    -p $env:POSTGRES_PORT `
    -U $env:POSTGRES_USER `
    -d postgres `
    -tAc "SELECT 1 FROM pg_database WHERE datname='$($env:POSTGRES_DB)'" 2>&1
$psqlExitCode = $LASTEXITCODE
if ($psqlExitCode -ne 0) {
    $details = ($existsOutput | Out-String).Trim()
    throw "PostgreSQL connection failed (exit code $psqlExitCode). Check the service and POSTGRES_* values in .env. $details"
}
$exists = (($existsOutput | Out-String).Trim() -eq '1')
if (-not $exists) {
    & $createdb -h $env:POSTGRES_HOST -p $env:POSTGRES_PORT -U $env:POSTGRES_USER $env:POSTGRES_DB
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to create PostgreSQL database '$($env:POSTGRES_DB)'."
    }
}

Push-Location (Join-Path $script:RepoRoot 'EALO\backend')
try {
    & $venvPython manage.py migrate --noinput
    & $venvPython manage.py check
} finally {
    Pop-Location
}

Push-Location (Join-Path $script:RepoRoot 'EALO\frontend')
try {
    & $script:EaloNpm ci
    & $script:EaloNpm run build
} finally {
    Pop-Location
}

Write-Host 'Setup completed. Run scripts\start-windows.ps1.'
