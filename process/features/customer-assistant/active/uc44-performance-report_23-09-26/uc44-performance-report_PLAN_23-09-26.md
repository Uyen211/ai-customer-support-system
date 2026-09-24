# UC44 Performance Statistics Report - Implementation Plan

**TL;DR:** Implement Usecase 4.4 "Báo cáo thống kê hiệu suất", an admin/manager dashboard for visualizing ticket metrics (total, resolved, SLA breaches, sentiment) filtered by a strict date range (max 365 days) and other optional parameters, including fast date selection and robust error handling.

## 1. Overview
This plan outlines the development of the Performance Statistics Report, accessible only to Managers and Admins. It includes a frontend filtering interface with quick-select options, robust date validation, and read-only charting components, powered by a new backend aggregation endpoint.

## 2. Touchpoints
- `frontend/src/pages/admin/PerformanceReportPage.jsx`: New page for the report dashboard.
- `frontend/src/components/report/ReportFilters.jsx`: Component for date, agent, priority, and category filters (including fast select buttons).
- `frontend/src/components/report/ReportCharts.jsx`: Component for rendering the pie chart (SLA) and bar chart (agent performance).
- `frontend/src/services/report.service.ts`: API client calls for fetching report data.
- `frontend/src/App.jsx`: Add routing for `/admin/reports` mapped to `PerformanceReportPage`.
- `backend/src/api/v1/endpoints/reports.py`: New router and endpoint for performance statistics.
- `backend/src/schemas/report.py`: Request and response schemas for report data.
- `backend/src/services/report_service.py`: Business logic for querying and aggregating ticket and conversation metrics based on filters.

## 3. Public Contracts
- **API `GET /api/v1/reports/performance`**: 
  - Query Parameters:
    - `start_date` (string, DD/MM/YYYY, required)
    - `end_date` (string, DD/MM/YYYY, required)
    - `agent_id` (UUID, optional)
    - `priority` (string, optional)
    - `category` (string, optional)
  - Validation: 
    - `start_date` <= `end_date`
    - `end_date` <= current date
    - `end_date` - `start_date` <= 365 days
  - Responses:
    - 200 OK: Returns aggregated metrics (`n_total`, `n_resolved`, `n_in_progress`, `n_breached`, `sla_breach_rate`, `sentiment_distribution`, `agent_performance`).
    - 400 Bad Request: Invalid date range (E-1).
    - 403 Forbidden: User lacks MANAGER or ADMIN roles.

## 4. Blast Radius
- **Scope**: New Frontend Reporting Page, New Backend Reporting API.
- **Risk Class**: Low/Medium. Purely read-only data aggregation. Performance impact on large queries is the primary risk.
- **Packages**: `frontend`, `backend`.

## 5. Verification Evidence

| Gate / Scenario | Strategy | Proves SPEC criterion |
|---|---|---|
| Role-based Access | Fully-Automated | Only MANAGER or ADMIN can view the report (Rule 1). |
| Valid Date Range Filter | Fully-Automated | Accepts DD/MM/YYYY, calculates $\Delta T \le 365$ days correctly. |
| Invalid Date Range (E-1) | Fully-Automated | Rejects end < start, end > today, or $\Delta T > 365$ with proper error messages and red borders. |
| Fast Date Selection (A-1) | Agent-Probe | Clicking "Hôm nay", "7 ngày qua", etc., auto-fills date inputs correctly. |
| Empty Data State (E-3) | Agent-Probe | Displays empty state illustration and sets all metrics to 0/0% when $N_{tổng} = 0$. |
| SLA Formula Verification | Fully-Automated | Verifies `Tỷ lệ vi phạm (%) = (N_vi_phạm / N_tổng) * 100%` is rounded to 1 decimal place (Rule 3). |
| Network Error Handling (E-2) | Agent-Probe | Displays orange warning banner with "Thử lại" button on fetch failure. |


## 6. Test Infra Improvement Notes
(none identified yet)

## 7. Resume and Execution Handoff
1. **Selected plan file path**: `process/features/customer-assistant/active/uc44-performance-report_23-09-26/uc44-performance-report_PLAN_23-09-26.md`
2. **Last completed phase or step**: Validate Contract.
3. **Validate contract status**: Written.
4. **Supporting context files loaded**: `docs/overview/usecase.md`
5. **Next step**: Proceed to implementation.

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
| Read-only aggregation query is safe | ✅ PASS | — |
| Strict RBAC applied (MANAGER/ADMIN) | ✅ PASS | — |
| Exception paths explicitly mapped to UI handling | ✅ PASS | — |

### Section IV: Execute-Agent Instructions

| # | Instruction | Trigger condition |
|---|---|---|
| E1 | Ensure SQLAlchemy aggregation queries use proper date filtering (ignore timezone mismatches if storing dates without timezone, but stick to UTC if applicable). | Backend implementation |
| E2 | Handle E-2 (Network error) state gracefully in `ReportFilters.jsx` so users can click "Thử lại". | Frontend implementation |

## Autonomous Goal Block

SESSION GOAL: Implement Performance Statistics Report (UC44) for Managers and Admins.
Autonomy rules: Only add read-only endpoints. Adhere strictly to the defined Usecase 4.4 flow.
Hard stops: If complex SQL aggregations impact performance significantly, pause and consult user.
Next phase: EXECUTE
Contract summary: Build `GET /api/v1/reports/performance` with strict date validation, and create the frontend `PerformanceReportPage` with date filters and empty/error state handling.
Execute start command: `npm run dev` in both frontend and backend to verify locally.
