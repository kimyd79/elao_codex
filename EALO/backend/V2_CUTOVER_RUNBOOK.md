# LogDetailV2 cutover runbook

The operational default is `LOG_STORAGE_MODE=dynamic` (2026-09-09). New analyses
write only to the original project-specific dynamic tables; V2 mirroring and
comparison are disabled. Existing V2 rows are retained but can become incomplete
relative to dynamic storage. Do not cut over using historical V2 coverage alone.

The following is an optional future migration procedure, not the current operating
configuration. Enable `dual` explicitly only when migration validation is authorized.

## Pre-cutover gate

Run from the repository root and retain the JSON output as the approval record:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\manage-windows.ps1 check_v2_readiness --require-match
powershell.exe -ExecutionPolicy Bypass -File .\scripts\manage-windows.ps1 test loganalyzerapi --verbosity 1 --noinput
```

The gate must report `ready_for_v2: true`, and the full regression suite must
pass. Take a PostgreSQL backup before changing the mode:

```powershell
pg_dump -Fc -h $env:POSTGRES_HOST -p $env:POSTGRES_PORT `
  -U $env:POSTGRES_USER -d $env:POSTGRES_DB `
  -f .runtime\elao-pre-v2-cutover.dump
```

## Controlled transition

Set `LOG_STORAGE_MODE=v2` in the deployment environment, restart both services,
and verify `/mwla/logdetail_v2/` plus the core UI flows. Keep the dynamic tables
and `django-dynamic-model` dependency during the observation period.

## Rollback

If any comparison, query, or UI flow fails, restore `LOG_STORAGE_MODE=dual` (or
`dynamic` for an immediate fallback), restart the services, and rerun the
readiness gate. Do not delete dynamic tables until the observation period,
backup restore test, and explicit operational approval are complete.
