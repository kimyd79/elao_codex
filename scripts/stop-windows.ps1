$repoRoot = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $repoRoot '.runtime'

foreach ($name in 'backend', 'frontend') {
    $pidFile = Join-Path $runtime "$name.pid"
    if (-not (Test-Path -LiteralPath $pidFile)) { continue }
    $processId = [int](Get-Content -LiteralPath $pidFile)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process) {
        Stop-Process -Id $processId
        Write-Host "Stopped $name (PID $processId)."
    }
    Remove-Item -LiteralPath $pidFile
}
