# ELAO backend tests

Run the backend regression suite from the repository root:

```powershell
$env:DJANGO_LOG_TO_FILE = 'False'
& .\.venv312\Scripts\python.exe EALO\backend\manage.py test loganalyzerapi --verbosity 1
Remove-Item Env:DJANGO_LOG_TO_FILE
```

The command creates and destroys PostgreSQL's `test_mwla2` test database. It
does not modify the development `mwla2` database or development media files.
The configured PostgreSQL user must be allowed to create a test database.

The suite currently covers:

- fixture counts and expected-result invariants;
- Apache, Nginx, IIS-W3C, and application-log parsing;
- project and logfile model relationships;
- username/password login;
- dynamic log-detail table creation and deletion;
- the minimal project, upload, analysis, and storage API workflow.
- completed, partial, and failed analysis-job states;
- compensating cleanup after a PostgreSQL COPY failure;
- safe repeated analysis without duplicate log-detail rows.

Before a V2 storage cutover, run `powershell.exe -ExecutionPolicy Bypass -File
..\..\scripts\manage-windows.ps1 check_v2_readiness --require-match` and
confirm that the report has `ready_for_v2: true`.

On Windows, prefer the command above while the development server is running.
Starting a second Django process from `EALO\backend` can fail when the server
holds `EALO\backend\logs\mwla.log` open. The logging configuration will be
separated from test execution in a later environment-normalization task.
