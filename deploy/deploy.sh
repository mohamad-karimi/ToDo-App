#!/bin/sh
# Runs on the production host (invoked over SSH by .github/workflows/cd.yml).
#
# Pulls the image built for this commit, brings the stack up, health-checks
# it, and rolls back to the previously deployed tag if the health check
# fails. Never printed: GHCR_TOKEN.
#
# Required environment variables:
#   GHCR_USERNAME, GHCR_TOKEN  - GHCR login (pull-only token)
#   IMAGE                      - e.g. ghcr.io/owner/repo
#   IMAGE_TAG                  - commit SHA to deploy
# Optional:
#   APP_URL                    - external URL to smoke-test; defaults to
#                                 the backend's internal port via nginx
#
# Usage: deploy.sh <deploy-path>
# <deploy-path> must contain docker-compose.prod.yml, default.conf and the
# production .env file (the .env is managed on the server, never sent by CI).

set -eu

DEPLOY_PATH="${1:?usage: deploy.sh <deploy-path>}"
cd "$DEPLOY_PATH"

: "${GHCR_USERNAME:?GHCR_USERNAME is required}"
: "${GHCR_TOKEN:?GHCR_TOKEN is required}"
: "${IMAGE:?IMAGE is required}"
: "${IMAGE_TAG:?IMAGE_TAG is required}"

if [ ! -f .env ]; then
  echo "ERROR: $DEPLOY_PATH/.env not found. Production secrets must already" >&2
  echo "       exist on this host; CD never uploads them." >&2
  exit 1
fi

COMPOSE="docker compose -f docker-compose.prod.yml"
STATE_FILE=".last_successful_tag"
PREVIOUS_TAG=""
[ -f "$STATE_FILE" ] && PREVIOUS_TAG="$(cat "$STATE_FILE")"

echo "$GHCR_TOKEN" | docker login ghcr.io -u "$GHCR_USERNAME" --password-stdin

deploy_tag() {
  tag="$1"
  export IMAGE="$IMAGE"
  export IMAGE_TAG="$tag"
  $COMPOSE pull
  $COMPOSE up -d --remove-orphans
}

health_check() {
  url="${APP_URL:-}"
  attempt=1
  max_attempts=15
  while [ "$attempt" -le "$max_attempts" ]; do
    if [ -n "$url" ]; then
      if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
        return 0
      fi
    else
      # No external URL configured: hit the existing schema route directly
      # inside the backend container (it always has Python, no extra tools
      # needed).
      if $COMPOSE exec -T backend python -c \
        "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/schema/', timeout=5)" \
        >/dev/null 2>&1; then
        return 0
      fi
    fi
    attempt=$((attempt + 1))
    sleep 4
  done
  return 1
}

echo "Deploying $IMAGE:$IMAGE_TAG ..."
deploy_tag "$IMAGE_TAG"

echo "Waiting for health check ..."
if health_check; then
  echo "$IMAGE_TAG" > "$STATE_FILE"
  echo "Deployment healthy: $IMAGE_TAG"
  docker image prune -f >/dev/null 2>&1 || true
  exit 0
fi

echo "Health check failed for $IMAGE_TAG." >&2

if [ -n "$PREVIOUS_TAG" ] && [ "$PREVIOUS_TAG" != "$IMAGE_TAG" ]; then
  echo "Rolling back to previously deployed tag: $PREVIOUS_TAG" >&2
  if deploy_tag "$PREVIOUS_TAG" && health_check; then
    echo "Rollback to $PREVIOUS_TAG succeeded." >&2
    exit 1
  fi
  echo "Rollback to $PREVIOUS_TAG also failed health check." >&2
else
  echo "No previous known-good tag recorded; nothing to roll back to." >&2
fi

exit 1
