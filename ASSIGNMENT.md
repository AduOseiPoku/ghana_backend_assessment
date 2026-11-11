# MFIDIE SOLUTIONS — BACKEND PRACTICAL ASSESSMENT

**Candidate:** __________________________  
**Date:** 11 November 2026  
**Suggested time:** 90 minutes  
**Stack:** Python, Django, Django REST Framework, SQLite (provided)  
**Theme:** Ghanaian school-fee payments (fictional demo records)

## Scenario

Two schools in Ghana use a basic system to view student fees and payment records. Administrators sometimes need to mark a **pending** payment as successfully verified after checking their internal reconciliation records. Each school must only see or change **its own** records.

A starter project with schools, students, payment data, authentication and read-only endpoints has been provided. Your job is to add the requested backend features, not build a frontend.

## Part A — Payment reconciliation endpoint (45 marks)

Implement `POST /api/payments/<id>/reconcile/` with JSON body:

```json
{"verified_reference": "GH-MOMO-260001"}
```

Rules:
1. User must be authenticated.
2. Only the administrator of the student's school may reconcile the payment. A user without access must not be able to change it.
3. `verified_reference` is mandatory, must be a string, and must exactly match that payment's stored `reference`.
4. Only payments in `PENDING` status may be changed to `SUCCESS`.
5. Successful reconciliation sets `status=SUCCESS` and `reconciled_at` to the current time and returns the updated payment.
6. Repeating the reconciliation of an already successful payment must **not** update the timestamp or duplicate any operation. Return a clear error response.
7. Failed payments must not be marked successful by this endpoint.
8. Return sensible HTTP status codes for success, validation errors, not-found and forbidden operations. You may conceal inaccessible objects as `404`.

**Important:** There is no external payment provider here. Do not simulate real MoMo charges or invent transaction confirmations. Verification is represented only by matching the existing fictional reference.

## Part B — Student fee summary endpoint (25 marks)

Implement `GET /api/students/<id>/fee-summary/` returning at least:

```json
{
  "admission_number": "HV-2026-001",
  "fee_due_ghs": "950.00",
  "successful_payments_ghs": "100.00",
  "outstanding_ghs": "850.00"
}
```

Rules:
1. The user may view only students in schools they administer.
2. Only `SUCCESS` payments count toward `successful_payments_ghs`; ignore `PENDING` and `FAILED`.
3. Use decimal-safe calculations. Format money to two decimal places.
4. After reconciling the pending GH₵250 payment for `HV-2026-001`, successful payments should become GH₵350 and outstanding should become GH₵600.
5. If payments exceed the fees due, return a signed outstanding amount; do not silently discard the overpayment.

## Part C — Tests, security, and code quality (20 marks)

Add tests demonstrating at least:
- Correct reconciliation of a pending payment.
- Wrong reference is rejected.
- User of another school cannot reconcile or view another school's details.
- Already successful and failed payments are rejected for reconciliation.
- Fee summary correctly excludes pending and failed transactions.

Use sensible design, readable code and clear validation. The starter's existing read endpoints and tests must continue working.

## Part D — Delivery and explanation (10 marks)

- Add a short `NOTES.md` summarising your approach, assumptions, and anything incomplete.
- Demonstrate both endpoints using the seeded example data.
- Run the tests and show the results.
- Commit only source code, tests, and relevant documentation. Do **not** commit `.venv`, `.env`, local database files or secrets.

## Running the starter

```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\\Scripts\\activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_ghana
python manage.py runserver
```

Run tests with `python manage.py test`.

Demo accounts and existing API endpoints are documented in `README.md`.

## Submission

Submit your updated source-code folder or Git repository link, plus `NOTES.md`. Be prepared to explain your code and make a small change to it during the review.

**Scoring:** Part A 45 + Part B 25 + Part C 20 + Part D 10 = **100 marks**.
