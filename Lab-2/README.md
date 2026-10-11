# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Course:** Software Engineering Laboratory  
**Problem Statement #43:** Feature Flag & Dynamic Config Manager  
**Reference Lab 1 Repository:** [LAB1-Developer-Tools-IT-Operations-43](https://github.com/Nagashri2304/LAB1-Developer-Tools-IT-Operations-43)  

---

## 1. Directory Structure & Deliverables

This directory contains all required lab deliverables matching the evaluation criteria:

```text
Lab-2/
├── screenshots/
│   ├── 01_jira_backlog_epics_user_stories.png
│   ├── 02_story_point_assignments.png
│   ├── 03_active_sprint_board.png
│   ├── 04_burndown_chart_sprint1.png
│   └── 05_burndown_chart_sprint2.png
├── Burndown_Chart_Analysis.pdf
├── Burndown_Chart_and_Sprint_Analysis.docx
├── Burndown_Chart_and_Sprint_Analysis.pdf
├── Burndown_chart.pdf
├── EPICs.pdf
├── EPICs_and_User_Stories.docx
├── EPICs_and_User_Stories.pdf
├── Jira_Backlog_Import.csv
├── Lab2_Agile_Backlog_and_Sprint_Simulation.docx
├── Lab2_Agile_Backlog_and_Sprint_Simulation.pdf
├── README.md
├── Reflection_Questions.docx
└── Reflection_Questions.pdf
```

---

## 2. Epics Architecture

The requirements from Lab 1 (FR-001 to FR-005, NFR-001, NFR-002, UC-01 to UC-07) are decomposed into four core Epics:

| Epic ID | Epic Summary | Scope & Description | Lab 1 Mapping |
| :--- | :--- | :--- | :--- |
| **FFM-EPIC-1** | Flag Lifecycle & Metadata Management | Enable Software Engineers to define, configure, and maintain feature flags with unique keys, default states, and multi-environment overrides (Dev, Staging, Prod). | FR-002, FR-004, UC-01, UC-04 |
| **FFM-EPIC-2** | Targeting Rules & Gradual Rollouts | Enable teams to configure granular cohort targeting (e.g. beta groups) and deterministic percentage rollouts (0–100%) to safely limit blast radius. | FR-001, FR-003, UC-02, UC-03 |
| **FFM-EPIC-3** | Governance, Approval Workflows & Audit Logging | Provide Release Managers with an approval gate to inspect configuration diffs, enforce 4-eyes principle, and maintain an immutable audit trail with one-click rollback. | UC-06, UC-07, NFR-002 |
| **FFM-EPIC-4** | High-Performance Evaluation & Real-Time SDK Sync | Deliver low-latency flag evaluation API (< 15ms p95) and push instantaneous updates to connected client SDKs via persistent WebSockets without redeployment. | FR-005, NFR-001, UC-05, UC-03 |

---

## 3. Product Backlog & User Stories Catalog

Each User Story follows the standard Agile template: `As a [user role], I want [goal], So that [benefit]`.

| Story ID | Epic | User Story Statement | Priority | Points | Sprint | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **US-01** | EPIC-1 | **As a** Software Engineer, **I want** to create a feature flag with a unique key, description, and default state, **so that** my client application can reference the flag unambiguously. | High | 3 | Sprint 1 | **Pass:** Duplicate keys return a 409 conflict error; unique key is registered and indexed within 2 seconds.<br>**Fail:** Duplicate keys are accepted. |
| **US-02** | EPIC-2 | **As a** Software Engineer, **I want** to configure a percentage rollout (0-100%) based on a deterministic hash of user IDs, **so that** I can gradually release features and limit blast radius. | High | 5 | Sprint 1 | **Pass:** 25% rollout allocates 25% (±2%) of 10,000 simulated user IDs; same user ID always yields identical evaluation.<br>**Fail:** Cohort changes between evaluations. |
| **US-03** | EPIC-2 | **As a** Software Engineer, **I want** to evaluate user targeting rules for specific cohorts, **so that** targeted users receive early feature access. | High | 5 | Sprint 1 | **Pass:** User with targeted attribute receives `true`; non-targeted receives fallback default.<br>**Fail:** Untargeted users receive experimental feature. |
| **US-04** | EPIC-4 | **As a** Software Engineer, **I want** the evaluation API to execute in under 15ms, **so that** embedding flag checks into client critical paths adds negligible latency. | High | 8 | Sprint 1 | **Pass:** p95 latency under simulated peak load is < 15ms; in-memory cache lookup avoids disk I/O.<br>**Fail:** Evaluation p95 exceeds 15ms. |
| **US-05** | EPIC-4 | **As a** Client SDK Developer, **I want** the SDK to maintain a local in-memory cache with fallback defaults, **so that** temporary network partitions do not break host application features. | Medium | 3 | Sprint 1 | **Pass:** In-memory evaluations return in < 1ms during offline conditions; system falls back safely.<br>**Fail:** Application blocks on disconnected socket. |
| **US-06** | EPIC-1 | **As a** Software Engineer, **I want** to define environment-specific overrides (Dev, Staging, Prod), **so that** I can test flags in lower environments without exposing unverified code in Production. | Medium | 5 | Sprint 2 | **Pass:** Prod override set to OFF while Staging is ON returns false for Prod and true for Staging.<br>**Fail:** Overrides leak between environments. |
| **US-07** | EPIC-3 | **As a** Software Engineer, **I want** to save changes as pending drafts and preview a visual diff, **so that** I can verify proposed modifications before requesting approval. | Medium | 3 | Sprint 2 | **Pass:** Draft changes do not alter runtime configurations; diff clearly highlights altered rules.<br>**Fail:** Draft changes alter live evaluations. |
| **US-08** | EPIC-3 | **As a** Release Manager, **I want** to review, approve, or reject pending flag changes with validation checks, **so that** unauthorized or invalid configs never reach production. | High | 5 | Sprint 2 | **Pass:** Only authenticated Release Managers can publish; invalid rules (e.g., rollout >100%) are rejected.<br>**Fail:** Unauthorized user publishes changes. |
| **US-09** | EPIC-3 | **As a** Release Manager, **I want** all configuration changes logged in an immutable audit trail with one-click rollback, **so that** actions are auditable and regressions can be reverted instantly. | High | 5 | Sprint 2 | **Pass:** Tamper-proof audit record created for every publish; one-click rollback restores prior state in < 3s.<br>**Fail:** Change occurs without audit entry. |
| **US-10** | EPIC-4 | **As a** Client SDK Developer, **I want** updated flag states streamed via WebSockets in real time, **so that** clients update within 5 seconds without redeployment. | High | 5 | Sprint 2 | **Pass:** 95% of active SDK connections receive updates within 5s; automatic reconnect upon disconnection.<br>**Fail:** Clients take > 30s to synchronize. |

---

## 4. Estimation & Planning Poker Rationale

Story points were estimated using the **Fibonacci Sequence** (`1, 2, 3, 5, 8, 13`):
- **3 Points (Low Complexity, Low Uncertainty):** `US-01` (CRUD models), `US-05` (In-memory cache), `US-07` (Visual diff preview).
- **5 Points (Moderate Complexity & State):** `US-02` (Deterministic hashing), `US-03` (Rule matching), `US-06` (Multi-env overrides), `US-08` (Approval gate), `US-09` (Audit trail & rollback), `US-10` (WebSocket streaming).
- **8 Points (High Uncertainty, Performance Critical):** `US-04` (Sub-15ms p95 evaluation engine latency SLA).

---

## 5. Sprint Simulation & Execution

### Sprint 1: Core Engine & Deterministic Targeting
- **Sprint Goal:** Establish core flag persistence, deterministic percentage rollouts, user cohort evaluation, and sub-15ms evaluation engine performance.
- **Committed Points:** 24 Story Points (US-01, US-02, US-03, US-04, US-05)
- **Completed Points:** 24 Story Points (100% completion)

### Sprint 2: Multi-Environment Governance, Approval Gate & Real-Time Sync
- **Sprint Goal:** Implement multi-environment isolation, release manager approval workflow, immutable audit logging with rollback, and real-time SDK WebSocket streaming.
- **Committed Points:** 23 Story Points (US-06, US-07, US-08, US-09, US-10)
- **Completed Points:** 23 Story Points (100% completion)

---

## 6. Reflection Questions & Technical Answers

### Question 1: Did your estimations reflect the actual effort?
**Answer:**  
Yes, the relative estimation using the Fibonacci sequence closely tracked the developmental complexity and actual effort required for each feature. Using Planning Poker allowed the team to distinguish between pure code volume and architectural uncertainty:
1. Low-uncertainty items (3 pts) like *US-01* and *US-07* involved standard CRUD and UI rendering, requiring minimal troubleshooting.
2. Moderate items (5 pts) like *US-02* and *US-09* required mathematical correctness (deterministic hashing across 10,000 users) and tamper-proof state management.
3. High-risk items (8 pts) like *US-04* accounted for the strict sub-15ms p95 latency threshold (NFR-001), capturing iterative profiling, memory caching, and benchmark testing.

### Question 2: Was your backlog well-prioritized?
**Answer:**  
Yes, the product backlog was prioritized based on architectural dependencies and risk reduction:
1. Prerequisite infrastructure was built first: *US-01 (Flag Creation)* was prioritized at the top of Sprint 1 because flags cannot be evaluated, overridden, or synchronized until their key identity is established.
2. High-risk performance requirements (*US-04: Sub-15ms API*) were scheduled in Sprint 1 to eliminate architectural bottlenecks early.
3. Enterprise governance (*US-06, US-07, US-08, US-09*) and real-time streaming (*US-10*) were scheduled into Sprint 2 once the core evaluation engine was verified.

### Question 3: How did your simulated sprint align with your plan?
**Answer:**  
The simulated sprints closely matched planned execution. In Sprint 1, all 24 planned points were completed across 5 user stories with zero scope creep. In Sprint 2, all 23 planned points were delivered. Pacing was disciplined: smaller 3-point stories moved to *Done* early in both sprints, while complex 5-point and 8-point items progressed through comprehensive unit and load verification before transitioning to *Done* by Day 5.

### Question 4: What insights did the burndown chart give about your team's capacity?
**Answer:**  
Jira's Burndown Chart revealed three critical operational insights:
1. **Predictable Capacity:** Completing 24 points in Sprint 1 and 23 points in Sprint 2 established that the team has a reliable, sustainable velocity of **~23–24 points per 1-week sprint**.
2. **Work Item Granularity:** Large 8-point stories (*US-04*) created a temporary step-like plateau on the burndown chart because points only burn when the entire story meets the Definition of Done. Breaking 8-point stories into smaller 3-point slices in future sprints will yield a smoother burndown curve.
3. **Discipline & Zero Scope Creep:** The remaining values curve showed a strictly downward trajectory with no mid-sprint upward spikes, confirming protected sprint boundaries.

---

## 7. Fast-Track Jira Demonstration Instructions

1. Create a **Scrum** project in Jira (**Company-managed**): Name: `Feature Flag & Dynamic Config Manager`, Key: `FFM`.
2. Go to **Backlog**, press **E** to enable the **Epic Panel**.
3. Import `Jira_Backlog_Import.csv` via the Backlog menu (`...` → **Import issues from CSV**).
4. Start **Sprint 1** (24 pts) → move cards across **To Do** → **In Progress** → **Done** → click **Complete sprint**.
5. Repeat for **Sprint 2** (23 pts) → click **Complete sprint**.
6. View **Reports → Burndown Chart** to demonstrate the velocity and burndown charts to the instructor.
