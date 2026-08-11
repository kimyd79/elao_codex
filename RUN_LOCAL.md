# EALO local execution

## Windows without Docker

The current source is a legacy stack. Install these versions side-by-side so
that the existing Node.js 24 installation does not have to be removed:

- Python 3.8.10 x64
- Node.js 14.21.1 x64 (use the ZIP distribution in a separate directory)
- PostgreSQL 16 x64

After installing PostgreSQL, copy the environment file and change its database
password to the password selected during PostgreSQL installation:

```powershell
cd C:\Codex\ELAO
Copy-Item .env.example .env
notepad .env
```

For example, if Node 14 was extracted to `C:\Tools\node-v14.21.1-win-x64`
and Python 3.8 was installed in the default per-user location:

```powershell
$env:EALO_NODE_HOME = 'C:\Tools\node-v14.21.1-win-x64'
$python38 = "$env:LocalAppData\Programs\Python\Python38\python.exe"

powershell -ExecutionPolicy Bypass -File .\scripts\setup-windows.ps1 `
  -Python $python38 `
  -PostgresBin 'C:\Program Files\PostgreSQL\16\bin'
```

The setup script creates `.venv`, installs backend and frontend dependencies,
creates the separate `mwla2` development database if needed, runs migrations,
and verifies both applications.

Start and stop the application with:

```powershell
$env:EALO_NODE_HOME = 'C:\Tools\node-v14.21.1-win-x64'
powershell -ExecutionPolicy Bypass -File .\scripts\start-windows.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\stop-windows.ps1
```

Runtime logs are written under `.runtime`. The application URLs are:

- Application: http://127.0.0.1:8080
- API root: http://127.0.0.1:8000/mwla/
- Django admin: http://127.0.0.1:8000/mwla/admin/

Run Django management commands through the environment-aware wrapper:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\manage-windows.ps1 createsuperuser
powershell -ExecutionPolicy Bypass -File .\scripts\manage-windows.ps1 check
```

## Docker alternative

This setup reproduces the legacy application without connecting to the
existing operational database:

- Python 3.8 / Django 3.0.4
- Node.js 14 / Vue 2.6
- PostgreSQL 12

## Prerequisite

Install Docker Desktop and confirm that `docker compose version` succeeds.

## Start

Run these commands from the repository root:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Open the following URLs:

- Application: http://127.0.0.1:8080
- API root: http://127.0.0.1:8000/mwla/
- Django admin: http://127.0.0.1:8000/mwla/admin/

The example environment creates the local administrator `admin` / `admin`.
Change or remove these values in `.env` when they are not needed.

## Verification and shutdown

```powershell
docker compose ps
docker compose logs -f backend
docker compose exec backend python manage.py check
docker compose exec backend python manage.py showmigrations
docker compose down
```

`docker compose down` preserves database and uploaded-file volumes. To remove
the disposable local data as well, use `docker compose down --volumes` only
after confirming it is no longer needed.

## Existing database

The default setup creates an empty local database. It does not load or connect
to the approximately 50 GB database described by `elao_table_info.txt`.
Restoring existing data should be handled separately after taking a backup and
validating the 85 project-specific dynamic tables.
