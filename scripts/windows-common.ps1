$ErrorActionPreference = 'Stop'

$script:RepoRoot = Split-Path -Parent $PSScriptRoot

function Import-EaloEnvironment {
    $envFile = Join-Path $script:RepoRoot '.env'
    if (-not (Test-Path -LiteralPath $envFile)) {
        throw "Missing $envFile. Run: Copy-Item .env.example .env"
    }

    foreach ($line in Get-Content -LiteralPath $envFile) {
        $trimmed = $line.Trim()
        if (-not $trimmed -or $trimmed.StartsWith('#')) { continue }
        $parts = $trimmed.Split('=', 2)
        if ($parts.Count -ne 2) { continue }
        [Environment]::SetEnvironmentVariable($parts[0].Trim(), $parts[1].Trim(), 'Process')
    }
}

function Get-EaloPython {
    $python = Join-Path $script:RepoRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path -LiteralPath $python)) {
        throw 'Python virtual environment is missing. Run scripts\setup-windows.ps1 first.'
    }
    return $python
}

function Enable-EaloNode {
    if ($env:EALO_NODE_HOME) {
        $nodeCommand = Join-Path $env:EALO_NODE_HOME 'node.exe'
        $npmCommand = Join-Path $env:EALO_NODE_HOME 'npm.cmd'
    } else {
        $nodeCommand = (Get-Command node.exe -ErrorAction SilentlyContinue).Source
        $npmCommand = (Get-Command npm.cmd -ErrorAction SilentlyContinue).Source
    }
    if (-not $nodeCommand -or -not (Test-Path -LiteralPath $nodeCommand)) {
        throw 'Node.js was not found. Set EALO_NODE_HOME to the Node 14 directory.'
    }
    $version = & $nodeCommand --version 2>$null
    if (-not $version -or $version -notmatch '^v14\.') {
        throw "Node.js 14.x is required; detected '$version'. Set EALO_NODE_HOME to a Node 14 directory."
    }
    $script:EaloNode = $nodeCommand
    $script:EaloNpm = $npmCommand
}
