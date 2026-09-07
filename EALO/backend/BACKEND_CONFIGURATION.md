# Backend dependency and configuration baseline

## Supported baseline

This is the supported backend baseline. Package versions remain pinned so
future intervals can be tested and rolled back independently.

- Python: 3.12
- Django: 5.2.15 LTS
- Django REST Framework: 3.16.1
- pandas: 2.2.3
- NumPy: 1.26.4
- PostgreSQL driver: psycopg2 2.9.10

## Dependency files

- `requirements.in`: direct application dependencies. Framework compatibility
  boundaries may be pinned explicitly.
- `requirements.lock.txt`: complete, pinned runtime environment. Setup scripts
  and container builds install this file.
- `requirements-dev.txt`: runtime lock plus optional legacy development tools.
- `requirements.txt` and `requirements.runtime.txt`: compatibility entry points
  that include the runtime lock.

Do not install the previous `django-rest-framework` package. It was an unrelated
and invalid duplicate of `djangorestframework`. Do not restore the unpinned HTTP
Git dependency for `django-dynamic-model`; the verified environment uses the
PyPI package `django-dynamic-model==0.2.0`.

## High-risk legacy dependencies

| Package | Current role | Upgrade concern |
|---|---|---|
| `django-dynamic-model` | Creates one log-detail table per project | Performs schema synchronization at runtime and conflicts with normal transaction boundaries |
| `django-postgres-copy` | Bulk imports parser CSV output | Does not support Django 5.2 index removal; calls must keep constraint/index dropping disabled |
| `dj-rest-auth` | Login and registration endpoints | Version 7.2.0; preserve token API tests |
| `django-allauth` | Registration dependency | Keep aligned with the selected `dj-rest-auth` interval |
| `pandas` / `numpy` | Access-log parsing | Parser behavior must remain covered by fixture tests |
| `psycopg2` | PostgreSQL connectivity | COPY and dynamic-DDL tests are required for upgrades |

These packages must not be upgraded in the same change. Each compatibility
group needs the access-log regression suite and migration checks.

## Django upgrade intervals

### Django 3.0.4 to 3.2.25

- `django-filter` was upgraded from 2.2.0 to 2.4.0 because 2.2 imports
  `FieldDoesNotExist` from a path removed by Django 3.2.
- `DEFAULT_AUTO_FIELD` remains `AutoField`, preserving existing primary-key
  types and preventing unintended migrations.
- Disabling `DJANGO_LOG_TO_FILE` now omits the file handler definition itself,
  so a read-only log directory no longer prevents startup.
- `requirements-django30.lock.txt` is the rollback dependency set.
- The original unmaintained `django-rest-auth` package was replaced by
  `dj-rest-auth==2.2.8`; the public `/mwla/rest-auth/` paths and token response
  contract remain unchanged.
- DRF was upgraded to 3.12.4 and django-allauth to 0.50.0 as one tested
  authentication compatibility group.
- `requirements-django32-pre-auth.lock.txt` restores the dependency set from
  immediately before the authentication replacement.
### Django 3.2.25 to 4.2.30

- The authentication group is pinned to `dj-rest-auth==6.0.0`, DRF 3.15.2,
  django-allauth 0.61.1, and django-filter 24.3.
- `AccountMiddleware` is enabled as required by the newer allauth release.
- Token authentication remains explicit (`SESSION_LOGIN=False`), preserving
  the existing login and registration `{ "key": "..." }` responses.
- Duplicate DRF router registrations were removed. Contract tests verify all
  SPA action URLs still resolve with their original HTTP methods.
- `django-dynamic-model==0.2.0` required no source patch in this interval; its
  runtime DDL creation/deletion and COPY workflows passed the PostgreSQL tests.
- `requirements-django32.lock.txt` is the immediate rollback dependency set.
- Django 4.2 support ended in April 2026. This is a temporary Python 3.8 bridge,
  not the final supported target; the next major interval requires a newer
  Python runtime and Django 5.2 LTS.

### pandas 1.0.3 to 2.0.3 and NumPy 1.18.2 to 1.24.4

- Deprecated `read_csv(error_bad_lines=False)` calls now use
  `on_bad_lines='skip'`, preserving the previous skip behavior.
- `np.NaN` usages in production parsing paths now use `np.nan`.
- Invalid Python string escapes in parser separators and regular expressions
  were converted to raw strings without changing their matching intent.
- The full parser fixture suite passed with warnings promoted to errors.
- `requirements-python38-pre-data.lock.txt` is the immediate rollback set.
- These are bridge versions for Python 3.8. A supported Python runtime is still
  required before moving to current pandas, NumPy, and Django 5.2 LTS.

### Python 3.8 / Django 4.2 to Python 3.12 / Django 5.2.15

- The Windows runtime now uses `.venv312`; the old `.venv` is retained locally
  as an emergency rollback environment.
- Authentication is aligned on `dj-rest-auth==7.2.0`,
  `django-allauth==65.13.1`, and DRF 3.16.1. Social-account migrations are
  installed because current registration URLs import those models.
- pandas 2.2.3 deprecations were removed with `ffill()` and `bfill()` calls.
- `django-postgres-copy` constraint/index dropping is disabled. Its legacy
  schema helper uses an API removed by Django 5.2, while dropping indexes for
  each import is unnecessary and unsafe inside transactions.
- `requirements-python38-django42.lock.txt` preserves the immediate dependency
  rollback set. A full rollback also requires reverting the corresponding
  source and database migration state from the existing backup/Git baseline.
- Dependency checks, Django checks, migration drift checks, and all 16 parser,
  dynamic-DDL, COPY, authentication, and router tests pass with warnings treated
  as errors.

## Environment rules

Native Windows commands load `.env` through `scripts/windows-common.ps1`.
Docker Compose supplies the same variable names to the backend container.

Important variables:

| Variable | Development default | Production rule |
|---|---|---|
| `DJANGO_SECRET_KEY` | local placeholder | Must be explicitly set |
| `DJANGO_DEBUG` | `True` | Must be `False` |
| `DJANGO_ALLOWED_HOSTS` | localhost values | Set explicit hostnames |
| `DJANGO_CORS_ALLOW_ALL` | follows DEBUG | Must be `False` |
| `DJANGO_CORS_ORIGINS` | local frontend URLs | Set explicit HTTPS origins |
| `DJANGO_MEDIA_ROOT` | `EALO/backend/media` | Set a persistent absolute path |
| `DJANGO_LOG_TO_FILE` | `True` | May be disabled when logs are collected from stdout |
| `DJANGO_LOG_DIR` | `EALO/backend/logs` | Set a writable persistent path when file logging is enabled |
| `LOG_PARSER_SPLIT_SIZE_BYTES` | 1.5 GiB | Tune only with performance evidence |

`DJANGO_DEBUG=False` with the placeholder secret key or unrestricted CORS now
raises `ImproperlyConfigured` during startup.

`manage.py check --deploy` still reports HTTPS, HSTS, secure-cookie, and referrer
policy recommendations. These are intentionally not forced in the local
baseline because the production TLS termination and reverse-proxy design is not
yet defined. They must be resolved before an internet-facing deployment.

## Verification commands

From the repository root:

```powershell
& .\.venv312\Scripts\python.exe -m pip check
& .\.venv312\Scripts\python.exe EALO\backend\manage.py check
& .\.venv312\Scripts\python.exe EALO\backend\manage.py test loganalyzerapi --verbosity 1
```

To run a Django command with the local `.env` loaded:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\scripts\manage-windows.ps1 check
```
