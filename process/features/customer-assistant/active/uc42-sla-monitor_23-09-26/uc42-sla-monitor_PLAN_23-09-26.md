---
name: plan:uc42-sla-monitor
description: "COMPLEX plan: implement UC 4.2 SLA monitor, resolve API, StaffConsole countdown and manager escalation"
date: 23-09-26
feature: customer-assistant
---

# UC 4.2 — Giám sát thời hạn xử lý cam kết (SLA)

**Date:** 23-09-26  
**Complexity:** COMPLEX (standard — one execution stream, not a phase program)  
**Status:** ⏳ PLANNED  
**Feature:** `customer-assistant`  
**SPEC:** `process/features/customer-assistant/active/uc42-sla-monitor_23-09-26/uc42-sla-monitor_SPEC_23-09-26.md`  
**Primary requirement:** `docs/overview/usecase.md` UC 4.2

**TL;DR:** Implement the empty SLA worker, resolve API, and StaffConsole countdown/alerts using existing `tickets.sla_deadline` / `sla_breached` and Redis `channel:ws_alerts`. Do not start code until VALIDATE writes a contract and the user says ENTER EXECUTE MODE.

## Context Envelope

| Field | Value |
|---|---|
| feature | customer-assistant |
| phase | PLAN |
| session-goal | Lock UC 4.2 implementation so EXECUTE needs no architecture guesses |
| branch | current working tree (see vc-review-situation at VALIDATE) |
| worktree | `/home/minh/kiem-thu/ai-customer-support-system` |
| context-group | tickets / SLA / staff console / websocket alerts |
| blast-radius-packages | `code/backend` (workers, tickets API, ticket model/schema, main), `code/frontend` (StaffConsole, ticketService) |
| active-plan | `process/features/customer-assistant/active/uc42-sla-monitor_23-09-26/uc42-sla-monitor_PLAN_23-09-26.md` |
| test-runner | `python -m unittest` (`code/backend/tests/run_tests.py`) |
| validate-contract | pending — placeholder heading only |

Context router files `process/context/all-context.md` and `process/context/tests/all-tests.md` are **absent** in this repo. Test commands below are taken from discovered files: `code/backend/tests/run_tests.py`, `code/backend/tests/test_ticket_dispatcher.py`, `code/frontend/package.json` (`lint` / `build` only). VALIDATE must re-check this; do not invent a bun/vitest runner.

## Overview

Use Case 4.2 starts after assignment (`IN_PROGRESS`). The system must show remaining time, enter WARNING at ≤20% remaining, mark overdue once, escalate to managers, and record on-time vs late completion from a required resolution summary.

**Scout finding (must not duplicate):** `start_sla_monitor_worker()` only sleeps 30s. It is exported from `app/workers/__init__.py` but **not** started in `app/main.py` (startup starts dispatcher + presence + Redis listener only). Tickets already have `sla_deadline` (set in `pipeline._create_or_update_ticket`) and `sla_breached`. There is no GET ticket list and no resolve endpoint. Frontend `ticketService.js` only calls assign. StaffConsole already consumes `/ws/alerts`.

Related active plans (do not overlap): `customer-services_*` (customer UI), `delete-conv-citations-markdown_*` (conversation delete / ticket disable). UC 4.1 dispatcher exists; this plan consumes `IN_PROGRESS` + `TICKET_ASSIGNED` and does not rewrite assignment.

## Goals

- Worker scans every 30s, marks breach once, publishes `SLA_WARNING` / `SLA_BREACH_ALERT`.
- Resolve API validates summary [10,1000], classifies on-time/late from server clock vs `sla_deadline`.
- StaffConsole shows countdown, visual states, complete dialog, manager alarm; reload hydrates from GET.

## Scope

**In:** worker, SLA state helper, ticket GET + resolve, schema field for summary if missing, WS payloads, StaffConsole cards/dialog/sound, unittest suite, register tests in `run_tests.py`, fix assign publish channel mismatch (`ws_alerts` → `channel:ws_alerts`).

**Out:** Kanban columns/drag (UC 4.3), analytics charts (UC 4.4), numeric penalty formula, resetting SLA on assign, customer-facing UI.

## Phase Completion Rules

A phase is NOT complete until:

1. **Integration Test** — Works with Redis WS + DB ticket rows.
2. **Manual Test** — Agent can see countdown and complete; manager sees overdue alarm.
3. **Data Verification** — `sla_breached`, `resolved_at`, `status` confirmed in DB.
4. **Error Handling** — Invalid summary and missing ticket fail without flipping status.
5. **User Confirmation** — User says it works.

Status meanings: ⏳ PLANNED · 🔨 CODE DONE · 🧪 TESTING · ✅ VERIFIED (only after user confirmation) · 🚧 BLOCKED.

Never mark ✅ VERIFIED from compile-only success.

## Execution Brief

### RFC-001 Foundation — SLA math + worker (⏳ PLANNED)

**What happens:** Pure functions for duration/state; worker `scan_sla_once`; start worker on API startup; publish on `channel:ws_alerts`.

**Integration points:** `Ticket`, `SLAPolicy`, Redis same channel as dispatcher, `main.py` startup.

**Test:** unittest with frozen `now` and mocked DB/Redis (same pattern as `test_ticket_dispatcher.py`).

**Verify:** `SELECT sla_breached FROM tickets WHERE id = …` after a forced past deadline.

**Done when:** AC-02..AC-07, AC-12, AC-13, AC-17 unit tests green; worker task visible in startup.

### RFC-002 Resolve + list API (⏳ PLANNED)

**What happens:** GET tickets for hydrate; POST resolve with summary; authz; persist outcome.

**Integration points:** `tickets.py`, schemas, StaffConsole later.

**Test:** unittest/API tests for summary bounds, on-time/late, 403.

**Verify:** after resolve, status `RESOLVED` and countdown source `resolved_at` set.

**Done when:** AC-01, AC-08, AC-09 (API), AC-10/11 (API), AC-18 green.

### RFC-003 StaffConsole UX (⏳ PLANNED)

**What happens:** Ticket cards, 1s tick from `sla_deadline`, warning/overdue/on-time styles, complete modal, manager copy + sound, GET on load.

**Integration points:** existing `useWebSocket`, `StaffConsole.jsx`.

**Test:** Agent-probe in browser; `npm run build` / `npm run lint` must not regress.

**Done when:** AC-09/10/11/14 UI copy and colors confirmed by user; AC-15 hydrate after refresh.

## Phased Execution Workflow

For each RFC:

1. **Pre-Phase Research** — Re-read the listed files. STOP if a path is gone. Do not bundle research + implementation in one leap if the file shape changed.
2. **Detailed Planning** — Follow this plan’s checklist; no new public routes beyond those named.
3. **Implementation** — Exact files below. No example-only code in other packages.
4. **Testing** — Commands in Verification Evidence.
5. **User Confirmation** — post-stage summary (What’s Functional Now / What Was Tested / What You Can Test / Ready For).

Do not start RFC-002 UI consumption before GET/resolve exist. RFC-003 may begin after RFC-002 handlers return the DTO. Worker (RFC-001) can land in parallel with RFC-002 **only if** both use the same helper module and Redis channel; prefer sequential RFC-001 → RFC-002 → RFC-003 to avoid contract drift.

**PAUSE:** Do not enter EXECUTE from this PLAN session.

## Architecture Decisions (Final)

1. **Clock origin is `tickets.sla_deadline` already set at create/priority-upgrade (UC 2.2).** Do not recompute on assignment. UC 4.2 text says T_start at IN_PROGRESS; existing data and `phantichhethong.md` already store deadline at create. Resetting on assign would extend SLA for tickets that waited in PENDING. Monitor **observes** only `IN_PROGRESS` (UC 4.2 precondition). PENDING overdue is out of scope.

2. **Duration source:** `sla_policies.resolution_time_minutes` with hardcoded fallback `{P1:15,P2:60,P3:240}` if row missing. Warning threshold = `0.20 * minutes * 60` seconds. Inclusive WARNING at remaining == threshold.

3. **Completeness vs worker:** `now` vs `sla_deadline` inside the resolve transaction is authoritative. Worker UPDATE must be `WHERE status = 'IN_PROGRESS' AND sla_breached IS FALSE AND sla_deadline <= now()`. Resolved rows cannot be flipped.

4. **Penalty = `sla_breached` boolean** for UC 4.4. Do not add a points column.

5. **Resolution text:** add nullable `tickets.resolution_summary TEXT`. Also copy into `ai_metadata` only if already used elsewhere; prefer the column as source of truth.

6. **Realtime:** publish JSON `{ "event": "...", "payload": {...} }` to **`channel:ws_alerts` only**. Fix `tickets.py` assign which currently publishes `ws_alerts` (listener never receives it).

7. **Manager alarm audience:** payload is broadcast to all `/ws/alerts` staff (current hub). Frontend plays sound and shows manager banner only for `role` MANAGER or ADMIN. Agents still restyle the card on `SLA_BREACH_ALERT` / GET `sla_breached`.

8. **Warning spam:** set `ai_metadata.sla_warning_sent = true` (JSONB merge) the first time remaining enters WARNING; publish `SLA_WARNING` once.

9. **Injected clock:** `sla_service` functions take `now: datetime | None = None` defaulting to `datetime.now(timezone.utc)`. Tests pass a fixed datetime. Do not use `time.sleep` to wait for real 15-minute P1 windows.

10. **No new test framework.** Backend: unittest + MagicMock like dispatcher tests. Frontend: no unit runner — UI is Agent-Probe; lint/build are regression only (they do not prove SLA).

## High-level Data Flow

1. Ticket created (UC 2.2) with `sla_deadline`.
2. Dispatcher/manual assign → `IN_PROGRESS` (UC 4.1). SLA clock already running.
3. Every 30s worker: load IN_PROGRESS tickets; compute remaining; maybe warn once; maybe breach once + Redis.
4. `listen_to_redis_alerts` fans out to StaffConsole sockets.
5. Agent GET `/admin/tickets` on load; local 1s ticker uses `sla_deadline`.
6. POST resolve → lock row → validate summary → compare now/deadline → `RESOLVED` → publish `TICKET_RESOLVED`.

## Failure Modes

| Failure | Handling |
|---|---|
| Worker exception on one ticket | log, continue other tickets, sleep 30s |
| Redis down | persist DB flags anyway; UI recovers on GET |
| Duplicate worker tasks | startup must create **one** `asyncio.create_task(start_sla_monitor_worker())`; scan is idempotent |
| Complete vs breach race | `SELECT … FOR UPDATE` on resolve; worker conditional UPDATE |
| Invalid summary | 422, no status change |
| Legacy DB without new column | document `ALTER TABLE tickets ADD COLUMN resolution_summary TEXT`; `create_all` will not alter existing tables |
| P3 policy `escalation_notify_to = AGENT` in seed | ignore for UC 4.2; always manager/admin UI for sound |

## Security Posture

- Resolve/list: `require_roles("AGENT","MANAGER","ADMIN")` (exact helper already in `app.api.deps`).
- AGENT: `ticket.assigned_to == current_user.id` else 403 with existing Vietnamese style.
- WS already rejects CUSTOMER. Do not put resolution text on manager-only fields beyond ticket id + agent name (already operational data).
- No new secrets.

## Touchpoints

| Path | Action |
|---|---|
| `code/backend/app/services/sla_service.py` | **Create.** `duration_seconds(priority, policy_minutes)`, `remaining_seconds(deadline, now)`, `sla_ui_state(...)`, `warning_threshold_seconds(priority)`, `format_breach_message(ticket_id, agent_name)`. |
| `code/backend/app/workers/sla_monitor_worker.py` | Replace stub with `scan_sla_once(db, redis, now)` + 30s loop; per-ticket try/except. |
| `code/backend/app/main.py` | `asyncio.create_task(start_sla_monitor_worker())` in `startup_event`. |
| `code/backend/app/models/ticket.py` | Add `resolution_summary = Column(Text, nullable=True)`. |
| `docs/database/sql.md` | Same column + comment; additive `ALTER` snippet for existing DBs. |
| `code/backend/app/schemas/ticket.py` | `TicketResolveRequest`; extend `TicketResponse` with `resolution_summary`, `remaining_seconds`, `sla_state`. |
| `code/backend/app/api/v1/endpoints/tickets.py` | GET list; POST `/{ticket_id}/resolve`; fix Redis channel on assign. |
| `code/backend/tests/test_sla_monitor.py` | **Create** unittest module covering AC rows tagged Fully-Automated. |
| `code/backend/tests/run_tests.py` | Register `TestSlaState`, `TestSlaWorker`, `TestSlaResolve`. |
| `code/frontend/src/services/ticketService.js` | `listTickets()`, `resolveTicket(id, summary)`. |
| `code/frontend/src/pages/admin/StaffConsole.jsx` | Cards, ticker, modal, WS handlers, GET hydrate, manager sound. |
| `code/frontend/src/components/agent/SlaTicketCard.jsx` | **Create** if StaffConsole would exceed ~reasonable size; otherwise keep in StaffConsole. Prefer a small card component. |
| `code/backend/app/api/v1/endpoints/ws_alerts.py` | Read-only unless broadcast bug found; do not change channel name. |

Do not modify RAG pipeline SLA create logic in this plan except reading it.

## Public Contracts

### GET `/api/v1/admin/tickets`

Auth: AGENT/MANAGER/ADMIN.

Response: `TicketResponse[]`.

- AGENT: `assigned_to == me`, statuses `IN_PROGRESS` plus `RESOLVED` from last 24h optional — **lock: AGENT sees own `IN_PROGRESS` and `RESOLVED` (unfiltered by time) so reload shows green/late labels.**
- MANAGER/ADMIN: all `IN_PROGRESS` plus `sla_breached` tickets still `IN_PROGRESS`.

`TicketResponse` fields (keep existing + add): `id`, `conversation_id`, `assigned_to`, `category`, `priority`, `status`, `summary`, `ai_metadata`, `sla_deadline`, `sla_breached`, `resolved_at`, `created_at`, `updated_at`, `resolution_summary`, `remaining_seconds` (int, may be negative), `sla_state` ∈ `NORMAL | WARNING | BREACHED | COMPLETED_ON_TIME | COMPLETED_LATE`.

`sla_state` is computed in the service, not stored.

### POST `/api/v1/admin/tickets/{ticket_id}/resolve`

Body: `{ "resolution_summary": string }`.

Rules:

- 404 unknown id.
- 403 AGENT on another’s ticket.
- 409 if status not `IN_PROGRESS`.
- 422 if trimmed length not in [10,1000]; `detail` includes AC-09 sentence for empty/whitespace; for length, same sentence is acceptable (do not invent a second copy).
- Success 200 `TicketResponse`; `status=RESOLVED`; `resolved_at=now`; late ⇒ `sla_breached=true`.

### WS events (payload)

`SLA_WARNING`: `{ ticket_id, priority, remaining_seconds, sla_deadline }`

`SLA_BREACH_ALERT`: `{ ticket_id, priority, assigned_to, agent_name, sla_deadline, breached_at, message }` where `message` is AC-12 with raw UUID string and `users.full_name` (`"chưa phân công"` if null).

`TICKET_RESOLVED`: `{ ticket_id, sla_state, sla_breached }`

Channel: `channel:ws_alerts`.

## Blast Radius

- **Packages:** backend app + backend tests + frontend StaffConsole/ticketService.
- **File count:** ~10–14 files (including 1 new service, 1 new test module, 1 optional card component).
- **Risk class:** public API + schema additive column + realtime + role checks (high-risk: API, schema, authz). Hybrid/automated gates required for API/schema; UI Agent-Probe.
- **Runtime:** extra asyncio task on API process; 30s DB scan — use existing index `idx_tickets_sla_check` (covers PENDING+IN_PROGRESS; filter IN_PROGRESS in query).
- **Rollback:** stop worker task; leave columns; clients ignore unknown JSON fields.

## Database Schema

Additive only:

```sql
ALTER TABLE tickets ADD COLUMN IF NOT EXISTS resolution_summary TEXT NULL;
```

No drop. `sla_deadline` / `sla_breached` unchanged.

## Backend Endpoints and Workers

- Worker query: `status == 'IN_PROGRESS'` AND (`sla_breached` is false OR warning not sent).
- Load assignee `full_name` via join/`User` for breach message.
- Session: `SessionLocal()` per scan, close in `finally` (copy dispatcher).
- Redis: `get_redis().publish("channel:ws_alerts", json.dumps(..., ensure_ascii=False))`.

## Implementation Checklist

RFC-001:

1. [ ] Create `code/backend/app/services/sla_service.py` with duration, remaining, state, warning threshold, breach message helpers; injectable `now`.
2. [ ] Write failing tests in `code/backend/tests/test_sla_monitor.py` for AC-02, AC-04, AC-05, AC-03 (TDD).
3. [ ] Run `cd code/backend && python -m unittest tests.test_sla_monitor.TestSlaState -v` — red then green after helpers.
4. [ ] Implement `scan_sla_once` in `sla_monitor_worker.py`: warning once, breach once, skip terminal, isolate per-ticket errors.
5. [ ] Write `TestSlaWorker` for AC-06, AC-07, AC-12, AC-13, AC-17.
6. [ ] Register `asyncio.create_task(start_sla_monitor_worker())` in `main.py` `startup_event` (single task).
7. [ ] Run `cd code/backend && python -m unittest tests.test_sla_monitor -v` — all worker/state tests pass.

RFC-002:

8. [ ] Add `resolution_summary` to Ticket model and `docs/database/sql.md` plus ALTER snippet.
9. [ ] Extend schemas: `TicketResolveRequest`, response SLA fields.
10. [ ] Implement GET `/admin/tickets` and POST `/admin/tickets/{id}/resolve` with lock, authz, 422/409/403/404 as specified; fix assign `publish` channel to `channel:ws_alerts`.
11. [ ] Write `TestSlaResolve` for AC-01, AC-08, AC-09 (API), AC-10/11 (API), AC-18.
12. [ ] Add suites to `code/backend/tests/run_tests.py`.
13. [ ] Run `cd code/backend && python tests/run_tests.py` — existing suites still pass plus new ones.

RFC-003:

14. [ ] Add `listTickets` / `resolveTicket` in `ticketService.js`.
15. [ ] StaffConsole: hydrate GET on login; 1s countdown from `sla_deadline`; states NORMAL/WARNING/BREACHED/completed; Hoàn tất modal; E-2 red border + AC-09 copy; on-time toast AC-10; late label AC-11; manager banner+sound on `SLA_BREACH_ALERT` for MANAGER/ADMIN; flashing red for breach.
16. [ ] Handle `SLA_WARNING`, `SLA_BREACH_ALERT`, `TICKET_RESOLVED`, keep `TICKET_ASSIGNED` / `UNASSIGNED_TICKET_ALERT`.
17. [ ] Run `cd code/frontend && npm run lint` and `npm run build`.
18. [ ] Agent-probe: P1 card above 180s normal; at 180s warning; at 0 red + manager text; invalid summary stays open; refresh restores state.

## Acceptance Criteria

See SPEC table AC-01–AC-18. Every AC has `proven by` + `strategy`. Developed UI behavior is not Known-Gap; it is Agent-Probe. Numeric penalty formula is explicitly non-goal (not a developed behavior).

## High-risk class gates

| Area | High-risk class | Minimum tier | Gap rationale |
|---|---|---|---|
| Resolve/list API + authz | public API + permission | Fully-Automated | — |
| `resolution_summary` column | schema | Hybrid (ALTER on running DB) + model unit import | `create_all` will not migrate live DBs |
| WS escalation | runtime/pubsub | Fully-Automated publish mock + Hybrid live Redis | — |
| StaffConsole visuals/sound | UI judgment | Agent-Probe | no frontend test runner |

## Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC criterion |
|---|---|---|
| `python -m unittest tests.test_sla_monitor.TestSlaState -v` | Fully-Automated | AC-02, AC-03, AC-04, AC-05 |
| `python -m unittest tests.test_sla_monitor.TestSlaWorker -v` | Fully-Automated | AC-06, AC-07, AC-12, AC-13, AC-17 |
| `python -m unittest tests.test_sla_monitor.TestSlaResolve -v` | Fully-Automated | AC-01, AC-08, AC-09 (API), AC-10/11 (API), AC-18 |
| `python tests/run_tests.py` | Fully-Automated | regression vs dispatcher/auth/canned |
| Apply ALTER + GET/POST against running API+Postgres+Redis | Hybrid | AC-15, AC-16, schema on live DB |
| StaffConsole browser: colors, copy, sound, modal, refresh | Agent-Probe | AC-09 UI, AC-10/11 UI, AC-14 |
| Frontend unit tests for countdown helper | Known-Gap residual | **not a proving strategy** — backlog stub below; UI still proven by Agent-Probe |

## Test Infra Improvement Notes

- Repo has no `process/context/tests/all-tests.md`. Gate commands are from `code/backend/tests/run_tests.py` (unittest) and frontend `package.json` (no test script).
- Prefer injectable `now` in `sla_service` / `scan_sla_once` so boundaries are deterministic.
- Frontend has no Vitest/Jest. Do not add a runner in this plan. Residual: countdown helper could be extracted later for unit tests (`uc42-frontend-sla-ticker` backlog).
- `test_ticket_dispatcher.py` is not in `run_tests.py` today; do not silently add it unless a test fails due to our assign-channel fix — if assign tests exist only in that file, run `python -m unittest tests.test_ticket_dispatcher -v` as extra Fully-Automated regression after the channel fix.

## Known Gaps (Resolved via Backlog)

None that block developed backend behavior. Named residual (not PASS-by-itself):

- Frontend countdown unit tests — NEW PLAN REQUIRED later if a JS test runner is introduced. UI remains Agent-Probe in this plan.

## Risks and Mitigations

- **Deadline-at-create vs T_start-at-assign:** Decision 1 locked; VALIDATE may flag CONCERN vs usecase wording — do not silently reset clocks in EXECUTE.
- **Worker not started today:** easy to forget `main.py`; checklist item 6 is mandatory.
- **Wrong Redis channel on assign:** already a production bug; fix in this blast radius.
- **Live schema:** EXECUTE must run ALTER on existing Postgres; Hybrid gate.
- **Sound autoplay:** browsers may block; Agent-Probe notes if gesture required — first StaffConsole click may unlock AudioContext.

## Integration Notes

- Docker/API process must include the new asyncio task (same process as FastAPI).
- Seed `sla_policies` already P1/P2/P3 minutes.
- Design tokens: StaffConsole already editorial; warning amber, breach flashing red, on-time green — do not restyle the whole console.

## Cursor + RIPER-5 Guidance

- PLAN is complete after artifact validation. Next user command: **ENTER VALIDATE MODE** (required). VALIDATE writes `## Validate Contract`. Only then **ENTER EXECUTE MODE**.
- EXECUTE receives this exact file path. Do not implement from chat memory.
- If scope grows to Kanban (4.3) or reports (4.4), stop and new plan.

## Test Procedure (post-EXECUTE manual)

1. Create/assign a ticket (or SQL-update `sla_deadline` to now+20s).
2. Agent console: countdown visible; near end card warning.
3. Let it expire: `sla_breached` true once; manager message exact; red flash.
4. Agent completes with 9-char summary: error, still IN_PROGRESS.
5. Agent completes with 10+ chars: RESOLVED, late label.
6. Repeat with future deadline: on-time green + toast.
7. Refresh page: states match GET.

**Data verification:** `SELECT id, status, sla_deadline, sla_breached, resolved_at, resolution_summary FROM tickets WHERE id = :id;`

## Resume and Execution Handoff

1. **Selected plan file path:** `process/features/customer-assistant/active/uc42-sla-monitor_23-09-26/uc42-sla-monitor_PLAN_23-09-26.md`
2. **Last completed phase or step:** PLAN draft written; VALIDATE not started.
3. **validate-contract status:** pending (placeholder below).
4. **Supporting context files loaded:** usecase.md UC 4.2, usecase4.md, phantichhethong.md §4.2, sql.md tickets/sla_policies, sla_monitor_worker.py, ticket model/schema/endpoints, main.py, ws_alerts.py, ticket_dispatcher_worker.py, pipeline ticket create, StaffConsole.jsx, ticketService.js, test_ticket_dispatcher.py, run_tests.py, sibling plans in `process/features/customer-assistant/active/`. Missing: `process/context/all-context.md`, `process/context/tests/all-tests.md`.
5. **Next step for a fresh agent:** run `node .claude/skills/vc-generate-plan/scripts/validate-plan-artifact.mjs` on this file if not just run; then wait for user **ENTER VALIDATE MODE**. Do not edit application source.

Validator note: `node .claude/skills/vc-generate-plan/scripts/validate-plan-artifact.mjs process/features/customer-assistant/active/uc42-sla-monitor_23-09-26/uc42-sla-monitor_PLAN_23-09-26.md`

## Agent strategy (PLAN → VALIDATE)

| Option | Agents | Fit |
|---|---|---|
| Sequential | 1 | Strong: single plan, files already scouted |
| Parallel subagents | 4 Layer-1 + ~3 sections ≈ 7–10 | VALIDATE V2 fan-out (no cross-talk) |
| Agent team | members × rounds | Overkill; no blast-radius negotiation across phases |
| Workflow | pipeline | Not needed |

**Recommendation for VALIDATE:** sequential if one validator; if V2 fan-out is required by protocol, **parallel-subagents** for Layer 1 dimensions (infra, tests, breaking, security) then synthesize. Dominant signal: one artifact, known blast radius, missing all-tests.md (test-coverage agent must use discovered unittest commands). Cost < 30 agents.

**Recommendation for later EXECUTE:** sequential (one worker, shared Ticket row + Redis contract).

## Validate Contract

(placeholder — vc-validate-agent writes this section before EXECUTE)

## Autonomous Goal Block

(placeholder — vc-validate-agent writes BRANCH A after V6 if no umbrella `## Stable Program Goal` exists; none exists today)
