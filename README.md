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

## CI/CD

**CI** (`.github/workflows/docker-image-todo-app.yml`, job `Todo-app`) runs on
every push and pull request to `main`: it builds the Docker Compose stack,
then runs `pytest`, `flake8` and `python manage.py check` inside the backend
container.

**CD** (`.github/workflows/cd.yml`) deploys to production. It runs:

- automatically, via `workflow_run`, once the `Todo-app` CI workflow
  finishes successfully for a **push to `main`** (pull requests and other
  branches never trigger a deployment), or
- manually, via `workflow_dispatch`, from the Actions tab.

Flow: `CI success on main` → build image with Buildx → push to
[GHCR](https://ghcr.io) as `ghcr.io/<owner>/<repo>:<commit-sha>` and
`ghcr.io/<owner>/<repo>:latest` → SSH into the production host → `docker
compose -f docker-compose.prod.yml pull && up -d --remove-orphans` → health
check → **automatic rollback** to the previously deployed image if the
health check fails. The deployed tag is always the exact commit SHA that CI
passed on; `latest` is pushed alongside it but is never what gets deployed.

Both jobs run under the `production`
[GitHub Environment](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment),
and a `production-deploy` concurrency group stops two deployments from
running at the same time.

### Production topology

`docker-compose.prod.yml` is the production counterpart of the local/CI
`docker-compose.yml`: same services (`backend`, `postgres`, `redis`,
`worker`, `beat`, `nginx`), but it pulls the prebuilt `IMAGE:IMAGE_TAG`
image instead of building from source, and it never bind-mounts the
repository into the containers. Nginx still serves `/static/` and
`/media/` directly and proxies everything else to the backend;
`collectstatic` and `migrate` still run at container startup via the
existing `entrypoint.sh` (unchanged).

### Required GitHub configuration

Create a `production` Environment (Settings → Environments) and add:

**Secrets**

| Name | Purpose |
| --- | --- |
| `DEPLOY_HOST` | Production server hostname/IP |
| `DEPLOY_PORT` | SSH port |
| `DEPLOY_USER` | SSH user |
| `DEPLOY_SSH_KEY` | Private key for that user (key-based auth only) |
| `DEPLOY_KNOWN_HOSTS` | Output of `ssh-keyscan -p <port> <host>`, pinned ahead of time |
| `GHCR_USERNAME` | GHCR login used on the server to pull images |
| `GHCR_TOKEN` | GHCR **pull-only** access token for that login |

**Variables**

| Name | Purpose |
| --- | --- |
| `DEPLOY_PATH` | Directory on the server that holds `docker-compose.prod.yml`, `default.conf`, `deploy/deploy.sh` and the production `.env` |
| `APP_URL` | Optional external URL used for the post-deploy smoke test; if unset, the health check runs the existing `/api/schema/` route from inside the backend container |

No real values for any of the above are stored in this repository.

### Production server prerequisites

- Linux host with Docker and the Docker Compose plugin installed
- `DEPLOY_PATH` directory already exists (or can be created by `DEPLOY_USER`)
- A production `.env` file already present in `DEPLOY_PATH`, with
  `POSTGRES_*`, `SECRET_KEY`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`,
  `ALLOWED_HOSTS`, etc. — this file is managed on the server and is
  **never** created, copied or read by CI/CD
- SSH access for `DEPLOY_USER` using the `DEPLOY_SSH_KEY` key pair only
  (no password authentication)

### Rollback

`deploy/deploy.sh` (run on the server by the CD workflow) records the last
successfully deployed image tag in `.last_successful_tag` next to the
compose file. If the health check fails after deploying a new tag, it
automatically redeploys that previous tag and health-checks it again;
database migrations are never rolled back automatically.

### Manual deploy

Actions tab → **CD** → **Run workflow** on `main` triggers the same
build-push-deploy flow via `workflow_dispatch`.
