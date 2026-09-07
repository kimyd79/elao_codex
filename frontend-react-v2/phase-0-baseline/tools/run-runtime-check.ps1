$ErrorActionPreference = 'Stop'

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$runtime = Join-Path $repo '.runtime'
$backendDir = Join-Path $repo 'EALO\backend'
$frontendDir = Join-Path $repo 'EALO\frontend'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null

# PowerShell can expose PATH and Path as separate keys. Remove the duplicate
# before Start-Process so child processes receive a valid environment block.
$pathKeys = [Environment]::GetEnvironmentVariables('Process').Keys |
    Where-Object { [string]::Equals($_, 'Path', 'OrdinalIgnoreCase') }
$pathValue = ($pathKeys | ForEach-Object { [string][Environment]::GetEnvironmentVariable($_, 'Process') } | Select-Object -First 1)
foreach ($key in $pathKeys) { [Environment]::SetEnvironmentVariable($key, $null, 'Process') }
[Environment]::SetEnvironmentVariable('Path', $pathValue, 'Process')

$python = Join-Path $repo '.venv312\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw "Python not found: $python" }
$npm = (Get-Command npm.cmd -ErrorAction Stop).Source

foreach ($port in @(8000, 8080)) {
    $listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($listener) { throw "Port $port is already in use by PID $($listener.OwningProcess)" }
}

$backend = Start-Process -FilePath $python -ArgumentList 'manage.py','runserver','127.0.0.1:8000','--noreload' -WorkingDirectory $backendDir -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtime 'phase0-backend.out.log') -RedirectStandardError (Join-Path $runtime 'phase0-backend.err.log')
$frontend = Start-Process -FilePath $npm -ArgumentList 'run','serve','--','--host','127.0.0.1','--port','8080' -WorkingDirectory $frontendDir -PassThru -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtime 'phase0-frontend.out.log') -RedirectStandardError (Join-Path $runtime 'phase0-frontend.err.log')

try {
    $deadline = (Get-Date).AddSeconds(45)
    do {
        Start-Sleep -Milliseconds 500
        $backendReady = [bool](Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue)
        $frontendReady = [bool](Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue)
        if ($backendReady -and $frontendReady) { break }
    } while ((Get-Date) -lt $deadline)

    $result = [ordered]@{ backend = $backendReady; frontend = $frontendReady; backend_pid = $backend.Id; frontend_pid = $frontend.Id; checks = @() }
    foreach ($uri in @('http://127.0.0.1:8000/mwla/','http://127.0.0.1:8000/mwla/logmaster/','http://127.0.0.1:8000/mwla/logfile/','http://127.0.0.1:8080/')) {
        try {
            $samples = @()
            $status = 0
            $bytes = 0
            1..3 | ForEach-Object { $sw = [Diagnostics.Stopwatch]::StartNew(); $response = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 10; $sw.Stop(); $status = [int]$response.StatusCode; $bytes = $response.RawContentLength; $samples += [math]::Round($sw.Elapsed.TotalMilliseconds, 2) }
            $sorted = @($samples | Sort-Object)
            $p95Index = [math]::Min($sorted.Count - 1, [math]::Ceiling($sorted.Count * 0.95) - 1)
            $result.checks += [ordered]@{ uri = $uri; status = $status; samples_ms = $samples; median_ms = $sorted[[int][math]::Floor($sorted.Count / 2)]; p95_ms = $sorted[[int]$p95Index]; bytes = $bytes }
        }
        catch { $result.checks += [ordered]@{ uri = $uri; error = $_.Exception.Message } }
    }
    $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'runtime-check.json') -Encoding utf8
    $result | ConvertTo-Json -Depth 5
}
finally {
    foreach ($process in @($frontend, $backend)) {
        if ($process -and -not $process.HasExited) { & taskkill.exe /PID $process.Id /T /F | Out-Null }
    }
}
