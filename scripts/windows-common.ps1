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
    $python312 = Join-Path $script:RepoRoot '.venv312\Scripts\python.exe'
    if (Test-Path -LiteralPath $python312) {
        return $python312
    }

    $legacyPython = Join-Path $script:RepoRoot '.venv\Scripts\python.exe'
    if (Test-Path -LiteralPath $legacyPython) {
        return $legacyPython
    }

    throw 'Python virtual environment is missing. Run scripts\setup-windows.ps1 first.'
}

function Normalize-EaloProcessEnvironment {
    $processEnvironment = [Environment]::GetEnvironmentVariables('Process')
    $pathKeys = @(
        $processEnvironment.Keys |
            Where-Object { [string]::Equals($_, 'Path', 'OrdinalIgnoreCase') }
    )
    if ($pathKeys.Count -le 1) { return }

    $pathValue = ($pathKeys | ForEach-Object {
        [string]$processEnvironment[$_]
    }) -join ';'
    foreach ($pathKey in $pathKeys) {
        [Environment]::SetEnvironmentVariable($pathKey, $null, 'Process')
    }
    [Environment]::SetEnvironmentVariable('Path', $pathValue, 'Process')
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
        throw 'Node.js was not found. Install Node.js 20.19 or newer, or set EALO_NODE_HOME.'
    }
    $version = & $nodeCommand --version 2>$null
    $parsedVersion = $null
    if ($version) {
        [version]::TryParse($version.TrimStart('v'), [ref]$parsedVersion) | Out-Null
    }
    if (-not $parsedVersion -or $parsedVersion -lt [version]'20.19.0') {
        throw "Node.js 20.19 or newer is required; detected '$version'. Set EALO_NODE_HOME to a supported Node directory."
    }
    $script:EaloNode = $nodeCommand
    $script:EaloNpm = $npmCommand
}
