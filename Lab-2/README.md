# Lab 2: Agile Backlog Creation & Sprint Simulation in Jira

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Course:** Software Engineering Laboratory  
**Problem Statement #43:** Feature Flag & Dynamic Config Manager  
**Reference Lab 1 Repository:** [LAB1-Developer-Tools-IT-Operations-43](https://github.com/Nagashri2304/LAB1-Developer-Tools-IT-Operations-43)  

---

## 1. Executive Summary

This laboratory exercise translates the functional and non-functional requirements identified in **Lab 1 (Problem Statement #43 – Feature Flag & Dynamic Config Manager)** into structured Agile backlog artifacts within **Atlassian Jira**. 

The goal of this project is to simulate an Agile-Scrum engineering lifecycle by:
1. Decomposing system requirements and use cases into thematic **Epics** and user-centric **User Stories**.
2. Conducting **Planning Poker** estimations using the **Fibonacci sequence** to calibrate task complexity, uncertainty, and development effort.
3. Prioritizing the product backlog using value-vs-risk criteria.
4. Simulating **two consecutive 1-week Sprints (Sprint 1 and Sprint 2)** by progressing work items across *To Do* → *In Progress* → *Done*.
5. Evaluating Sprint performance and team velocity using Jira's **Burndown Charts** and answering critical reflective prompts on estimation accuracy, backlog prioritization, and capacity forecasting.

---

## 2. Epics Breakdown

The system requirements from Lab 1 (UC-01 through UC-07, FR-001 through FR-005, NFR-001, NFR-002) are structured into four core Epics:

| Epic ID | Epic Summary | Description | Mapped Requirements & Use Cases |
| :--- | :--- | :--- | :--- |
| **FFM-EPIC-1** | Flag Lifecycle & Metadata Management | Enable Software Engineers to define, configure, and maintain feature flags with unique keys, default states, and multi-environment overrides (Dev, Staging, Prod) to prevent configuration drift and safely test features. | FR-002, FR-004, UC-01, UC-04 |
| **FFM-EPIC-2** | Targeting Rules & Gradual Rollouts | Enable engineering teams to configure granular user cohort targeting (e.g., beta groups, user ID attributes) and deterministic percentage rollouts (0-100%) to safely limit blast radius and validate releases. | FR-001, FR-003, UC-02, UC-03 |
| **FFM-EPIC-3** | Governance, Approval Workflows & Audit Logging | Provide Release Managers with an approval gate to inspect configuration diffs, enforce 4-eyes principle before production changes, and maintain an immutable audit trail for compliance and rollbacks. | UC-06, UC-07, NFR-002 |
| **FFM-EPIC-4** | High-Performance Evaluation & Real-Time SDK Sync | Deliver low-latency flag evaluation API (< 15ms p95) and push instantaneous configuration changes to connected client SDKs via persistent WebSockets/streaming connections without requiring client redeployments. | FR-005, NFR-001, UC-05, UC-03 |

---

## 3. Product Backlog & User Stories Catalog

Each User Story follows the standard Agile template:  
`As a [user role], I want [goal], So that [benefit].`

| Story ID | Parent Epic | User Story Statement | Priority | Story Points | Sprint | Acceptance Criteria |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **US-01** | FFM-EPIC-1 | **As a** Software Engineer, **I want** to create a feature flag with a unique key, description, and default state, **so that** my client application can reference the flag unambiguously. | High | 3 | Sprint 1 | **Pass:** Duplicate keys return a 409 conflict error; unique key is registered and indexed within 2 seconds.<br>**Fail:** Duplicate keys are accepted. |
| **US-02** | FFM-EPIC-2 | **As a** Software Engineer, **I want** to configure a percentage rollout (0-100%) based on a deterministic hash of user IDs, **so that** I can gradually release features and limit blast radius. | High | 5 | Sprint 1 | **Pass:** 25% rollout allocates 25% (±2%) of 10,000 simulated user IDs; same user ID always yields identical evaluation.<br>**Fail:** Cohort changes between evaluations. |
| **US-03** | FFM-EPIC-2 | **As a** Software Engineer, **I want** to evaluate user targeting rules for specific cohorts (e.g. beta users, role), **so that** targeted users receive early feature access. | High | 5 | Sprint 1 | **Pass:** User with targeted attribute receives `true`; non-targeted receives fallback default.<br>**Fail:** Untargeted users receive experimental feature. |
| **US-04** | FFM-EPIC-4 | **As a** Software Engineer, **I want** the evaluation API to execute in under 15ms, **so that** embedding flag checks into client critical paths adds negligible latency. | High | 8 | Sprint 1 | **Pass:** p95 latency under simulated peak load is < 15ms; in-memory cache lookup avoids disk I/O.<br>**Fail:** Evaluation p95 exceeds 15ms. |
| **US-05** | FFM-EPIC-4 | **As a** Client SDK Developer, **I want** the SDK to maintain a local in-memory cache with fallback defaults, **so that** temporary network partitions do not break host application features. | Medium | 3 | Sprint 1 | **Pass:** In-memory evaluations return in < 1ms during offline conditions; system falls back safely.<br>**Fail:** Application blocks on disconnected socket. |
| **US-06** | FFM-EPIC-1 | **As a** Software Engineer, **I want** to define environment-specific overrides (Dev, Staging, Prod), **so that** I can test flags in lower environments without exposing unverified code in Production. | Medium | 5 | Sprint 2 | **Pass:** Prod override set to OFF while Staging is ON returns false for Prod and true for Staging.<br>**Fail:** Overrides leak between environments. |
| **US-07** | FFM-EPIC-3 | **As a** Software Engineer, **I want** to save changes as pending drafts and preview a visual diff, **so that** I can verify proposed modifications before requesting approval. | Medium | 3 | Sprint 2 | **Pass:** Draft changes do not alter runtime configurations; diff clearly highlights altered rules.<br>**Fail:** Draft changes alter live evaluations. |
| **US-08** | FFM-EPIC-3 | **As a** Release Manager, **I want** to review, approve, or reject pending flag changes with validation checks, **so that** unauthorized or invalid configs never reach production. | High | 5 | Sprint 2 | **Pass:** Only authenticated Release Managers can publish; invalid rules (e.g., rollout >100%) are rejected.<br>**Fail:** Unauthorized user publishes changes. |
| **US-09** | FFM-EPIC-3 | **As a** Release Manager, **I want** all configuration changes logged in an immutable audit trail with one-click rollback, **so that** actions are auditable and regressions can be reverted instantly. | High | 5 | Sprint 2 | **Pass:** Tamper-proof audit record created for every publish; one-click rollback restores prior state in < 3s.<br>**Fail:** Change occurs without audit entry. |
| **US-10** | FFM-EPIC-4 | **As a** Client SDK Developer, **I want** updated flag states streamed via WebSockets in real time, **so that** clients update within 5 seconds without redeployment. | High | 5 | Sprint 2 | **Pass:** 95% of active SDK connections receive updates within 5s; automatic reconnect upon disconnection.<br>**Fail:** Clients take > 30s to synchronize. |

---

## 4. Estimation & Planning Poker Rationale

Story points were estimated using the **Fibonacci Sequence** (`1, 2, 3, 5, 8, 13`), which reflects non-linear growth in uncertainty and complexity:

- **3 Points (Low Complexity, Low Uncertainty):** e.g., **US-01** (Standard CRUD operation for flag creation with database unique constraints) and **US-05** / **US-07** (Standard diff rendering and local caching).
- **5 Points (Moderate Complexity, Moderate Uncertainty):** e.g., **US-02** (Deterministic SHA-256 hashing and bucket distribution), **US-03** (Rule engine condition evaluator), **US-06** (Multi-environment configuration isolation), **US-08** (Two-party authorization gating), **US-09** (Cryptographic audit logging and state rollback), **US-10** (WebSocket push event architecture).
- **8 Points (High Complexity, High Uncertainty, Performance Critical):** e.g., **US-04** (High-throughput, low-latency API optimization requiring p95 < 15ms SLA, memory indexing, benchmark stress testing, and concurrency locking).

---

## 5. Sprint Simulation & Execution

### Sprint 1: Core Lifecycle, Deterministic Targeting & Engine Foundation
- **Sprint Goal:** Establish core flag persistence, deterministic percentage rollouts, user cohort evaluation, and sub-15ms evaluation engine performance.
- **Planned Work:** US-01 (3 pts), US-02 (5 pts), US-03 (5 pts), US-04 (8 pts), US-05 (3 pts).
- **Total Committed Velocity:** **24 Story Points**
- **Actual Completed Velocity:** **24 Story Points** (100% completion)

### Sprint 2: Multi-Environment Governance, Approval Gate & Real-Time Sync
- **Sprint Goal:** Implement multi-environment isolation, release manager approval workflow, immutable audit logging with rollback, and real-time SDK WebSocket streaming.
- **Planned Work:** US-06 (5 pts), US-07 (3 pts), US-08 (5 pts), US-09 (5 pts), US-10 (5 pts).
- **Total Committed Velocity:** **23 Story Points**
- **Actual Completed Velocity:** **23 Story Points** (100% completion)

---

## 6. Reflection Questions & Analytical Answers

### Question 1: Did your estimations reflect the actual effort?
**Answer:**  
Yes, the relative estimation using the Fibonacci sequence closely tracked the developmental complexity and actual effort required for each feature. 
Using Planning Poker allowed the team to distinguish between pure code volume and architectural uncertainty:
1. **Low Uncertainty Items (3 pts):** User stories like *US-01 (Create Feature Flag)* and *US-07 (Draft Flag Revisions)* involved well-understood database CRUD models and UI form components. As predicted, they required minimal debugging and were completed early in their respective sprints.
2. **Algorithmic and State Complexity (5 pts):** Stories such as *US-02 (Deterministic Rollout)* and *US-09 (Audit Logging & Rollback)* required mathematical correctness (ensuring uniform hashing across 10,000 users) and tamper-proof state management. Estimating them at 5 points accounted for the substantial unit testing and edge-case verification needed.
3. **High-Risk Performance Items (8 pts):** *US-04 (Sub-15ms Evaluation API)* carried the greatest architectural risk due to the strict non-functional SLA (NFR-001). Allocating 8 points accurately captured the iterative tuning required for in-memory indexing, concurrency profiling, and latency benchmarking. 
Estimating via Fibonacci numbers prevented the common pitfall of anchoring to calendar hours, allowing the team to accommodate cognitive complexity and testing overhead effectively.

---

### Question 2: Was your backlog well-prioritized?
**Answer:**  
Yes, the backlog was systematically prioritized based on **architectural dependency analysis** and **risk-adjusted business value**:
1. **Dependency Sequencing:** A feature flag cannot be evaluated, overridden, or synchronized until its fundamental schema and key identity are established. Therefore, *US-01 (Flag Creation)* was prioritized at the very top of Sprint 1. Similarly, deterministic hashing (*US-02*) and cohort evaluation (*US-03*) formed the essential algorithmic backbone before real-time streaming (*US-10*) or approval gates (*US-08*) could have any functional target to act upon.
2. **De-risking Core Performance in Sprint 1:** Because the system's core value proposition relies on sub-15ms evaluation latency (NFR-001), postponing performance optimization to Sprint 2 would have introduced massive technical debt. Prioritizing *US-04* in Sprint 1 ensured the engine was battle-tested early.
3. **Layering Governance in Sprint 2:** Enterprise features like environment overrides (*US-06*), four-eyes approval workflows (*US-08*), and audit trails (*US-09*) were scheduled into Sprint 2. This followed a disciplined Agile MVP progression—first building a fast, functional evaluation core, then wrapping it with enterprise governance, security, and broadcast distribution.

---

### Question 3: How did your simulated sprint align with your plan?
**Answer:**  
The simulated sprints demonstrated strong alignment with the planned velocity and sprint commitments:
1. **Sprint 1 Execution:** 
   - Committed: 24 Story Points across 5 user stories.
   - Pacing: The team transitioned *US-01* and *US-05* (3 pts each) from *To Do* → *In Progress* → *Done* in the initial days of the sprint, securing immediate progress.
   - Mid-Sprint Work: Complex tasks *US-02* and *US-03* progressed smoothly through unit testing.
   - Sprint Finale: *US-04* (8 pts) spent an extended duration in *In Progress* while p95 benchmark benchmarks were verified, burning down to *Done* near Day 5.
   - Final Result: All 24 points burned down to 0, achieving the Sprint Goal without scope changes.
2. **Sprint 2 Execution:**
   - Committed: 23 Story Points across 5 user stories.
   - Pacing: Governance and streaming items progressed in parallel. *US-07* and *US-08* moved to *Done* once validation gates were verified, followed by *US-06*, *US-09*, and *US-10*.
   - Final Result: The burndown chart reflected steady, daily reductions in remaining work, completing 100% of planned points on schedule.
Simulation showed no scope creep, as all proposed changes were properly funneled into the product backlog rather than mid-sprint injections.

---

### Question 4: What insights did the burndown chart give about your team's capacity?
**Answer:**  
Jira's Burndown Chart provided three critical operational insights regarding team capacity and delivery dynamics:
1. **Velocity Consistency:** The team demonstrated stable capacity across both iterations (Sprint 1: 24 points; Sprint 2: 23 points). This indicates that the team's sustainable velocity is approximately **23–24 story points per 1-week sprint** (or ~47 points per two-week cycle), providing a highly reliable baseline for future release forecasting.
2. **Trajectory vs. Guideline Slope:** 
   - The ideal guideline slope forms a linear downward line from the total commitment (24 pts) to zero.
   - In Sprint 1, because *US-04* was an 8-point story, the actual remaining effort line hovered above the guideline for two days during profiling, before taking a sharp drop once the latency benchmark passed. This highlighted that **large 8-point user stories cause "step-like" burndown plateaus**. In future sprints, breaking 8-point stories into smaller 3-point slices (e.g., separating indexing from load-testing) would yield a smoother burndown curve.
3. **Absence of Scope Creep and Over-commitment:** The red line never trended upward mid-sprint, proving that the team did not introduce unplanned scope after the sprint start date. Furthermore, because the burndown reached exactly 0 points at sprint completion rather than leaving leftover tasks in *In Progress*, the team avoided over-commitment while maximizing output capacity.

---

## 7. Deliverables & Artifacts in this Repository

- `jira_import_lab2.csv`: Direct Jira CSV import file containing all Epics, User Stories, Story Points, Priorities, and Descriptions.
- `Jira_Agile_Backlog_and_Sprint_Simulation.pdf`: Complete submission-ready PDF document including full specifications, sprint workflows, burndown chart analytics, and reflection answers.
- `Reflection_Questions.md`: Standalone reference answering the laboratory reflection questions.
- `JIRA_STEP_BY_STEP_GUIDE.md`: Step-by-step instructions to demonstrate the Jira project to the instructor.
