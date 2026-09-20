# ToDo App

## Running modes

| | Local / Docker | Wasmer Edge (`WASMER=true`) |
| --- | --- | --- |
| Requirements | `requirements-docker.txt` (adds `psycopg2-binary`) | `requirements.txt` (no native-DB driver) |
| Database | SQLite when `DEBUG=True`, otherwise PostgreSQL | SQLite (`core/db.sqlite3`, override with `SQLITE_PATH`) |
| Cache | Redis (`django-redis`) | In-process `LocMemCache` |
| Celery | Redis broker | `memory://` broker, tasks run eagerly (no worker/beat) |

Wasmer installs only `requirements.txt` for `wasix_wasm32` with
`--only-binary=:all:`, so packages without a WASIX wheel must not be added
there. WASIX wheels exist only for Python 3.13/3.14, which is why `Anybuild`
uses Python 3.13 (the Docker image still uses 3.11).

Set these environment variables in the Wasmer app (never commit them):
`SECRET_KEY`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` and `ALLOWED_HOSTS`
(e.g. `.wasmer.app`). `WASMER=true` and `DEBUG=False` are already set in
`Anybuild`.

The Wasmer filesystem is not guaranteed to be persistent, so the SQLite
database may be reset on redeploy or restart.
