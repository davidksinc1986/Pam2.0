#!/usr/bin/env bash
set -euo pipefail

cp -n .env.example .env || true
docker compose up -d --build db redis api
sleep 5
docker compose exec api python scripts/init_db.py

echo "Bootstrap completado. API: http://localhost:8000/docs"
