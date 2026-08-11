param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$DjangoArguments
)

. (Join-Path $PSScriptRoot 'windows-common.ps1')
Import-EaloEnvironment
$python = Get-EaloPython

if (-not $DjangoArguments -or $DjangoArguments.Count -eq 0) {
    throw 'Provide a Django command, for example: createsuperuser'
}

Push-Location (Join-Path $script:RepoRoot 'EALO\backend')
try {
    & $python manage.py @DjangoArguments
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
