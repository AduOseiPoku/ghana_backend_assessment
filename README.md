# Ghana School Fees API — Django assessment starter

This is a **local-only, fictional** dataset for a backend skills assessment. No live MoMo, school, or bank integration is included.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_ghana
python manage.py runserver
```

`python manage.py test` runs the included baseline tests.

## Demo accounts (local test only)

| Account | Password | Access |
|---|---|---|
| accra_admin | AccraDemo2026! | Harbour View Academy (Demo) |
| kumasi_admin | KumasiDemo2026! | Asante Learning Centre (Demo) |
| viewer | ViewerDemo2026! | No schools |

Use browser login via `/api-auth/login/` or HTTP Basic auth in a local API client. Do not use these passwords for any real system.

## Existing endpoints

- `GET /api/schools/`
- `GET /api/students/`
- `GET /api/payments/`
- Detail GET endpoints are also available.

These endpoints already restrict records by the logged-in school's administrator.

## Your work

Read `ASSIGNMENT.md`. The reconciliation and summary features are intentionally **not implemented**. Write tests for your changes and document your design decisions.
