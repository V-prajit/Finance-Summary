# Finance Summary

A self-hosted personal finance tracker. Upload bank/card statements, and a
rules engine auto-tags transactions (admin-defined rules plus per-user custom
rules) so you can see spending broken down by category.

## Stack
- Backend: Django REST Framework (`backend/`), with apps for accounts, file
  uploads, and transaction storage/tagging (`storage/transaction_analyzer.py`
  matches transactions against rules and generates tags).
- Frontend: React + TypeScript (`frontend/`), with file upload, a
  transaction table, and rule management UI.
- Postgres for storage; nginx reverse-proxies frontend/backend in Docker.

## Running it
```
docker-compose up --build
```
Brings up nginx, Postgres, the Django backend, and the React frontend
together. See `docker-compose.yml` for service config and env vars.

## Status
Experimental / paused. Core upload -> rule-tagging -> transaction table flow
works; not actively developed right now.

## License
No license file yet, so all rights reserved by default until one is added.
