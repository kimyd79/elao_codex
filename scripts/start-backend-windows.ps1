. (Join-Path $PSScriptRoot 'windows-common.ps1')
Import-EaloEnvironment
Normalize-EaloProcessEnvironment
$python = Get-EaloPython

$runtime = Join-Path $script:RepoRoot '.runtime'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null

$pidFile = Join-Path $runtime 'backend.pid'
if (Test-Path -LiteralPath $pidFile) {
    $existingProcessId = [int](Get-Content -LiteralPath $pidFile)
    $existingProcess = Get-Process -Id $existingProcessId -ErrorAction SilentlyContinue
    if ($existingProcess) {
        throw "Backend is already running (PID $existingProcessId). Run scripts\stop-windows.ps1 first."
    }
    Remove-Item -LiteralPath $pidFile
}

$backend = Start-Process -FilePath $python `
    -ArgumentList 'manage.py','runserver','127.0.0.1:8000','--noreload' `
    -WorkingDirectory (Join-Path $script:RepoRoot 'EALO\backend') `
    -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtime 'backend.out.log') `
    -RedirectStandardError (Join-Path $runtime 'backend.err.log')
$backend.Id | Set-Content -LiteralPath $pidFile

Write-Host "Backend PID: $($backend.Id) - http://127.0.0.1:8000/mwla/"
Write-Host "Python: $python"
Write-Host "Logs: $runtime"
