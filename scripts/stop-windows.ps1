$repoRoot = Split-Path -Parent $PSScriptRoot
$runtime = Join-Path $repoRoot '.runtime'

foreach ($name in 'backend', 'frontend') {
    $pidFile = Join-Path $runtime "$name.pid"
    if (-not (Test-Path -LiteralPath $pidFile)) { continue }
    $processId = [int](Get-Content -LiteralPath $pidFile)
    $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
    if ($process) {
        # npm.cmd and vue-cli spawn child processes. Terminate the complete
        # tree so a hidden node/python child cannot keep ports or dist files
        # locked after the wrapper exits.
        & taskkill.exe /PID $processId /T /F *> $null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Stopped $name process tree (PID $processId)."
        } else {
            Write-Warning "Could not stop $name process tree (PID $processId)."
            continue
        }
    }
    Remove-Item -LiteralPath $pidFile
}
