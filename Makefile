.PHONY: api-dev web-dev dev

API_CMD=if command -v uv >/dev/null 2>&1; then PYTHONPATH=../.. uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000; else PYTHONPATH=../.. .venv/bin/uvicorn app.main:app --reload --host 127.0.0.1 --port 8000; fi

api-dev:
	cd apps/api && $(API_CMD)

web-dev:
	cd apps/web && pnpm dev

dev:
	@trap 'kill 0' EXIT; \
	(cd apps/api && $(API_CMD)) & \
	(cd apps/web && pnpm dev) & \
	wait
