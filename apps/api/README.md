# MirrorOS API

FastAPI backend for MirrorOS.

## Run Locally

From the repository root:

```bash
make api-dev
```

Or run directly from `apps/api` with `PYTHONPATH` pointed to the repository root:

```bash
cd apps/api
PYTHONPATH=../.. uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Migrations

Run Alembic from `apps/api`:

```bash
cd apps/api
uv run alembic upgrade head
```
