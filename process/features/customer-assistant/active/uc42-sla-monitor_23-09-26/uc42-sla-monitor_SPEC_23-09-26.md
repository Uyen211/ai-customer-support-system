---
name: spec:uc42-sla-monitor
description: "Locked requirements for UC 4.2 SLA deadline monitoring — customer-assistant"
date: 23-09-26
feature: customer-assistant
type: SPEC
---

# SPEC — UC 4.2 Giám sát thời hạn xử lý cam kết

**Date:** 23-09-26  
**Source of truth:** `docs/overview/usecase.md` (UC 4.2). Cross-check: `docs/overview/usecase4.md`, `docs/overview/phantichhethong.md` §4.2.  
**INNOVATE:** skipped (mechanical “how” from locked use case).

## Actors

- Primary: background system (SLA monitor).
- Receivers: CSKH agent (countdown, warning, complete), CSKH manager (escalation alarm).

## Preconditions

1. Ticket is assigned and status is `IN_PROGRESS`.
2. Priority SLA policy exists: P1 = 900s, P2 = 3600s, P3 = 14400s.

## Acceptance criteria

Each criterion names `proven by` and `strategy` (Fully-Automated | Hybrid | Agent-Probe). Known-Gap is not a proving strategy.

| ID | Criterion | proven by | strategy |
|---|---|---|---|
| AC-01 | Ticket id on resolve/list is UUID v4, exactly 36 characters (hex + hyphens). Invalid id is rejected; monitor ignores missing rows. | `tests.test_sla_monitor.TestSlaResolve.test_invalid_ticket_id` | Fully-Automated |
| AC-02 | Durations: P1 900s, P2 3600s, P3 14400s (15 / 60 / 240 minutes). | `tests.test_sla_monitor.TestSlaState.test_priority_durations` | Fully-Automated |
| AC-03 | Stored `tickets.sla_deadline` is the clock origin. Remaining seconds = `sla_deadline - now` (UTC). Client must not decide on-time vs late. | `tests.test_sla_monitor.TestSlaState.test_remaining_from_deadline` | Fully-Automated |
| AC-04 | NORMAL: remaining > 20% of duration. Thresholds: P1 > 180s, P2 > 720s, P3 > 2880s. | `tests.test_sla_monitor.TestSlaState.test_normal_above_threshold` | Fully-Automated |
| AC-05 | WARNING: 1s ≤ remaining ≤ 20% of duration (inclusive upper bound). | `tests.test_sla_monitor.TestSlaState.test_warning_inclusive_threshold` | Fully-Automated |
| AC-06 | E-1: remaining ≤ 0 while status is `IN_PROGRESS` → `sla_breached = TRUE` exactly once. | `tests.test_sla_monitor.TestSlaWorker.test_breach_once` | Fully-Automated |
| AC-07 | Worker does not newly breach `RESOLVED` or `CLOSED` tickets. | `tests.test_sla_monitor.TestSlaWorker.test_skips_terminal_status` | Fully-Automated |
| AC-08 | Completion requires `resolution_summary` trimmed length in [10, 1000]. Length 9, 1001, empty, whitespace-only fail. | `tests.test_sla_monitor.TestSlaResolve.test_summary_boundaries` | Fully-Automated |
| AC-09 | E-2: invalid summary returns field error; ticket stays `IN_PROGRESS`; monitor stays active. Exact UI copy: `Vui lòng nhập tóm tắt kết quả đã xử lý cho khách hàng trước khi đóng phiếu`. | `tests.test_sla_monitor.TestSlaResolve.test_invalid_summary_keeps_in_progress` + StaffConsole complete dialog | Fully-Automated + Agent-Probe |
| AC-10 | Complete when `now <= sla_deadline`: status `RESOLVED`, `resolved_at` set, `sla_breached` remains false unless already true from a prior true overdue, countdown stops, label `Đạt chuẩn cam kết`, toast `Phiếu hỗ trợ đã được xử lý thành công đúng thời hạn!`. | `tests.test_sla_monitor.TestSlaResolve.test_complete_on_time` + StaffConsole | Fully-Automated + Agent-Probe |
| AC-11 | Complete when `now > sla_deadline`: still allowed; record late; label `Hoàn thành quá hạn`; `sla_breached = TRUE`. | `tests.test_sla_monitor.TestSlaResolve.test_complete_late` + StaffConsole | Fully-Automated + Agent-Probe |
| AC-12 | Manager escalation text: `Phiếu hỗ trợ [Mã phiếu] do nhân viên [Tên nhân viên] phụ trách đã quá hạn xử lý!`. Event once per ticket. | `tests.test_sla_monitor.TestSlaWorker.test_escalation_payload_once` | Fully-Automated |
| AC-13 | `sla_breached = TRUE` is the performance-penalty fact consumed by UC 4.4. No numeric score formula in this SPEC. | `tests.test_sla_monitor.TestSlaWorker.test_breach_flag_persisted` | Fully-Automated |
| AC-14 | Agent/manager ticket cards: warning (amber), overdue flashing red, on-time green. Countdown ticks from deadline snapshot. | StaffConsole ticket card visual check | Agent-Probe |
| AC-15 | Reload/reconnect restores SLA from GET list/detail, not from missed WS events. | GET `/api/v1/admin/tickets` after simulated disconnect | Hybrid |
| AC-16 | SLA worker runs on API process startup, scan period 30s. | `main.py` startup registers worker; worker uses 30s sleep | Hybrid |
| AC-17 | Redis publish channel is `channel:ws_alerts`. Events: `SLA_WARNING`, `SLA_BREACH_ALERT`, `TICKET_RESOLVED`. | `tests.test_sla_monitor.TestSlaWorker.test_publishes_ws_alerts_channel` | Fully-Automated |
| AC-18 | AGENT may complete only assigned tickets; MANAGER/ADMIN any ticket. Unauthenticated/wrong role rejected. | `tests.test_sla_monitor.TestSlaResolve.test_resolve_authorization` | Fully-Automated |

## Main flow (locked)

1. Validate ticket id + priority ∈ {P1,P2,P3}.
2. Display countdown on the work card using `sla_deadline`.
3. Classify NORMAL / WARNING / E-1.
4. Agent clicks **Hoàn tất xử lý**.
5–7. Require valid `resolution_summary`.
8–9. Stop clock, `RESOLVED`, on-time labeling if still before deadline.

## Exceptions (locked)

- E-1 overdue: flag, flashing red, manager alarm + copy in AC-12, persist `sla_breached` for reports, late complete allowed.
- E-2 empty/invalid summary: red border + AC-09 copy; stay `IN_PROGRESS`.

## Explicit non-goals

- UC 4.3 Kanban drag/drop and reverse-status rules (except resolve contract shared with 4.3).
- UC 4.4 charts/export.
- Numeric SLA penalty points beyond `sla_breached`.
- Resetting `sla_deadline` on assignment (deadline is set at ticket create / priority upgrade in UC 2.2).
