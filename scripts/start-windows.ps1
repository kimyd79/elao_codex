. (Join-Path $PSScriptRoot 'windows-common.ps1')
Import-EaloEnvironment
Enable-EaloNode
$python = Get-EaloPython

$runtime = Join-Path $script:RepoRoot '.runtime'
New-Item -ItemType Directory -Path $runtime -Force | Out-Null

$backend = Start-Process -FilePath $python `
    -ArgumentList 'manage.py','runserver','127.0.0.1:8000','--noreload' `
    -WorkingDirectory (Join-Path $script:RepoRoot 'EALO\backend') `
    -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtime 'backend.out.log') `
    -RedirectStandardError (Join-Path $runtime 'backend.err.log')
$backend.Id | Set-Content -LiteralPath (Join-Path $runtime 'backend.pid')

$frontend = Start-Process -FilePath $script:EaloNpm `
    -ArgumentList 'run','serve','--','--host','127.0.0.1','--port','8080' `
    -WorkingDirectory (Join-Path $script:RepoRoot 'EALO\frontend') `
    -WindowStyle Hidden -PassThru `
    -RedirectStandardOutput (Join-Path $runtime 'frontend.out.log') `
    -RedirectStandardError (Join-Path $runtime 'frontend.err.log')
$frontend.Id | Set-Content -LiteralPath (Join-Path $runtime 'frontend.pid')

Write-Host "Backend PID: $($backend.Id) - http://127.0.0.1:8000/mwla/"
Write-Host "Frontend PID: $($frontend.Id) - http://127.0.0.1:8080"
Write-Host "Logs: $runtime"
