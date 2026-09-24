# UC43 Kanban Board - Implementation Plan

**TL;DR:** Implement Usecase 4.3 "Quản lý tiến độ trên bảng Kanban" featuring a 4-column drag-and-drop board for support tickets, strict one-way state transitions, role-based permission checks, and mandatory resolution notes when closing tickets, along with SLA timer integration.

## 1. Overview
This plan covers the implementation of a Kanban board to manage customer support tickets based on Usecase 4.3 specifications.

## 2. Touchpoints
- `frontend/src/components/KanbanBoard/`: New Kanban board component, columns, and drag-and-drop logic.
- `frontend/src/components/TicketDetail/`: Ticket detail modal with status update functionality.
- `frontend/src/services/ticket.service.ts`: API client calls for updating ticket status.
- `backend/src/controllers/ticket.controller.ts`: Endpoint for updating ticket status.
- `backend/src/services/ticket.service.ts`: Business logic for ticket updates, state transitions, SLA timer stop, and permission checks.
- `backend/src/models/ticket.model.ts`: Ticket schema definitions (if adjustments are needed).

## 3. Public Contracts
- **API `PUT /api/tickets/:id/status`**: 
  - Request Body: `{ status: string, resolutionNote?: string }`
  - Validation: `id` (UUID v4), `status` (must be a valid transition), `resolutionNote` (required if moving to "Đã giải quyết", 10-1000 characters).
  - Responses:
    - 200 OK: Status updated.
    - 400 Bad Request: Invalid transition or missing resolution note.
    - 403 Forbidden: User not authorized to update this ticket.
    - 404 Not Found: Ticket not found.

## 4. Blast Radius
- **Scope**: Frontend Kanban UI, Ticket Service (Backend & Frontend).
- **Risk Class**: Medium. Incorrect state transitions could corrupt support ticket flow or incorrectly halt SLA timers.
- **Packages**: `frontend`, `backend`.

## 5. Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC criterion |
|---|---|---|
| Card display data | Fully-Automated | Displays ID, priority, summary, timer correctly. |
| Drag & drop state transition | Agent-Probe | UI correctly calls API on drop and handles error state (reverts card). |
| Role-based permissions | Fully-Automated | Only assigned staff, Manager, or Admin can update status (E-1). |
| One-way transition rule | Fully-Automated | Reject backward transitions (e.g., "Đã giải quyết" to "Đang xử lý") (E-2). |
| Resolution note validation | Fully-Automated | Require 10-1000 chars when moving to "Đã giải quyết" (E-3). |
| SLA Timer halt | Fully-Automated | SLA timer stops correctly upon moving to "Đã giải quyết". |

## 6. Test Infra Improvement Notes
(none identified yet)

## 7. Resume and Execution Handoff
1. **Selected plan file path**: `process/features/customer-assistant/active/uc43-kanban-board_23-09-26/uc43-kanban-board_PLAN_23-09-26.md`
2. **Last completed phase or step**: Plan generation.
3. **Validate contract status**: Pending.
4. **Supporting context files loaded**: `docs/overview/usecase4.md`
5. **Next step**: Run `vc-validate-findings` to validate this plan, then proceed to implementation of backend services followed by frontend UI.

## 8. Validate Contract

### Layer 1 dimensions

| Layer 1 dimensions | Status |
|---|---|
| Infra fit | ✅ PASS |
| Test coverage | ✅ PASS |
| Breaking changes | ✅ PASS |
| Security surface | ✅ PASS |

### Layer 2 sections

| Layer 2 sections | Status |
|---|---|
| Touchpoints & Contracts | ✅ PASS |
| Verification Evidence | ✅ PASS |

**Totals: 0 FAILs / 0 CONCERNs / 6 PASSes**

**→ Net Gate: PASS**

### Section I: Findings

| Finding | Severity | Proposed fix |
|---|---|---|
| All paths and logic verify mechanically | ✅ PASS | — |
| Permissions and RBAC are properly specified | ✅ PASS | — |
| Edge cases for empty resolution note and rollback on failure covered | ✅ PASS | — |

### Section IV: Execute-Agent Instructions

| # | Instruction | Trigger condition |
|---|---|---|
| E1 | Ensure frontend Kanban drag-and-drop handles network errors (E-4) by rolling back the card to its original position. | Frontend implementation |
| E2 | Verify UUID v4 format explicitly in the backend controller before processing status update. | Backend implementation |

## Autonomous Goal Block

SESSION GOAL: Implement Kanban board support for Support Tickets (UC43) across backend and frontend.
Autonomy rules: Follow standard backend/frontend separation. Ensure tests pass before finishing.
Hard stops: If database schema requires large restructuring, block and ask user.
Next phase: EXECUTE
Contract summary: Add ticket status update endpoint with strict transition validation, SLA timer pause, and build Kanban board UI with drag-and-drop.
Execute start command: `npm run dev` in both frontend and backend to verify locally.
