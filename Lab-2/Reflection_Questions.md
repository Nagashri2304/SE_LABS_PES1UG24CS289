# Lab 2: Reflection Questions & Technical Analysis

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Course:** Software Engineering Laboratory  
**Problem Statement #43:** Feature Flag & Dynamic Config Manager  

---

### Question 1: Did your estimations reflect the actual effort?

**Detailed Evaluation:**  
Yes, our relative estimation using the Fibonacci sequence (`1, 2, 3, 5, 8, 13`) reflected the actual effort and implementation complexity with a high degree of fidelity. In Agile software development, estimating effort is not merely about counting lines of code or predicting exact calendar hours; it is about calibrating **technical complexity, cognitive effort, and environmental uncertainty**.

1. **Low Uncertainty Items (3 Story Points):**
   - **US-01 (Create Feature Flag with Unique Key and Default State):** Estimated at 3 points. The data modeling, primary key uniqueness constraints, and basic CRUD API are well-defined architectural patterns. Actual development required minimal troubleshooting, aligning exactly with the 3-point estimate.
   - **US-05 (Client SDK Local In-Memory Cache) & US-07 (Draft Revisions & Diff Preview):** Estimated at 3 points each. The SDK cache leveraged standard key-value map structures with mutex synchronization, and the diff view utilized established JSON-patch comparisons. These tasks were delivered with rapid turnaround.

2. **Moderate Algorithmic & Stateful Complexity (5 Story Points):**
   - **US-02 (Deterministic Percentage-Based Rollout):** Estimated at 5 points. Ensuring that a user ID deterministically hashes (e.g. via MurmurHash3 or SHA-256 modulo 100) and produces uniform distribution within 25% (±2%) across 10,000 simulated evaluations required rigorous statistical validation.
   - **US-08 (Release Manager Approval Gate) & US-09 (Immutable Audit Logging & One-Click Rollback):** Estimated at 5 points each. These stories required multi-tenant role-based access control (RBAC), approval state machines, cryptographic hashing for audit log tamper-resistance, and atomic snapshot restores. The 5-point allocation provided the necessary buffer for comprehensive integration testing.
   - **US-10 (Real-Time Flag State Streaming via WebSockets):** Estimated at 5 points. Managing persistent socket connections, ping/pong heartbeats, reconnect backoffs, and broadcasting updates to hundreds of connected SDKs justified a 5-point estimate over simple HTTP polling.

3. **High Uncertainty & Performance-Critical Work (8 Story Points):**
   - **US-04 (Sub-15ms Evaluation API Optimization):** Estimated at 8 points. Satisfying the non-functional requirement (NFR-001) that flag evaluations execute in under 15ms p95 under peak production load was technically demanding. The team had to eliminate cold-start database queries by introducing in-memory L1/L2 caching, benchmark garbage collection pauses, and stress-test concurrent requests. The 8-point estimate accounted for iterative profiling and optimization loops.

**Takeaway:** By applying Planning Poker, our team avoided Parkinson's Law and false precision, achieving consensus on relative task difficulty before entering active sprints.

---

### Question 2: Was your backlog well-prioritized?

**Detailed Evaluation:**  
Yes, the product backlog was prioritized using a combination of **Architectural Dependency Sequencing**, **Risk Reduction (De-risking)**, and **Core Value Delivery (MoSCoW framework)**:

1. **Foundational Architectural Dependencies:**
   - Agile development demands that prerequisite infrastructure be built before dependent features. A feature flag cannot be evaluated, overridden, or synchronized if the entity cannot first be authored and persisted in the system. Consequently, **US-01 (Flag Creation)** was prioritized as the top backlog item.
   - Deterministic hashing (**US-02**) and attribute targeting (**US-03**) were scheduled immediately following creation, establishing the computational rules engine before downstream systems interacted with it.

2. **De-risking High-Impact Performance Bottlenecks Early (Sprint 1):**
   - The primary technical risk in Problem Statement #43 was the low-latency threshold (**US-04: Sub-15ms latency**). Flag checks sit directly on the hot code path of client applications; any latency penalty degrades the host application.
   - Had this requirement been deferred to Sprint 2, an architectural flaw discovered late in the cycle would have required rewriting the data layer. Prioritizing **US-04** in Sprint 1 allowed the team to validate the latency SLA while the codebase was still lightweight.

3. **Progressive Layering of Enterprise Governance & Distribution (Sprint 2):**
   - Multi-environment overrides (**US-06**), visual configuration diffs (**US-07**), approval gating (**US-08**), immutable audit logs (**US-09**), and WebSocket streaming (**US-10**) represent enterprise reliability and operational governance.
   - These features depend on a mature, verified evaluation core. Placing them in Sprint 2 enabled a clean architectural progression: build the working evaluation engine in Sprint 1, then harden it with governance, security, and real-time distribution in Sprint 2.

---

### Question 3: How did your simulated sprint align with your plan?

**Detailed Evaluation:**  
The execution of our simulated sprints closely mirrored the sprint plans, with planned commitments matching team delivery:

1. **Sprint 1 Execution Alignment:**
   - **Planned Velocity:** 24 Story Points (5 User Stories).
   - **Execution Cadence:** The sprint began by moving **US-01** (3 pts) and **US-05** (3 pts) to *In Progress* on Day 1. Both were completed and transitioned to *Done* by Day 2.
   - Mid-sprint, development focused on **US-02** (5 pts) and **US-03** (5 pts), achieving functional verification by Day 3 and Day 4.
   - **US-04** (8 pts) remained in *In Progress* from Day 2 through Day 5 while load testing and profiling were executed. Upon passing the latency benchmark, it was moved to *Done*.
   - **Sprint 1 Outcome:** 24 of 24 planned points completed (100% completion rate). Zero scope changes were introduced mid-sprint.

2. **Sprint 2 Execution Alignment:**
   - **Planned Velocity:** 23 Story Points (5 User Stories).
   - **Execution Cadence:** Work commenced concurrently on **US-07** (Draft & Diff Preview - 3 pts) and **US-06** (Environment Overrides - 5 pts). Both reached *Done* by Day 2.
   - The approval gate (**US-08** - 5 pts) was completed on Day 3, unlocking final end-to-end testing for the audit logger (**US-09** - 5 pts) and WebSocket sync engine (**US-10** - 5 pts), which transitioned to *Done* by Day 5.
   - **Sprint 2 Outcome:** 23 of 23 planned points completed (100% completion rate).

3. **Variance and Control:**
   - No unplanned tasks or emergency bug fixes bypassed the backlog. Any potential scope expansion (e.g., adding automated email alerts to approval requests) was captured as future backlog candidates rather than injected into the running sprints.

---

### Question 4: What insights did the burndown chart give about your team's capacity?

**Detailed Evaluation:**  
Jira's Burndown Chart generated valuable quantitative insights into the team's operational velocity, pacing characteristics, and capacity forecasting:

1. **Sustainable Velocity Determination:**
   - Across the two simulated sprints, the team completed **24 story points** in Sprint 1 and **23 story points** in Sprint 2.
   - This minimal variance (±1 point) establishes that the team's reliable, sustainable velocity is **~23 to 24 story points per 1-week sprint**. For subsequent sprint planning, product owners can forecast future release milestones with high statistical confidence.

2. **Work Item Granularity & Plateaus vs. Guideline Slope:**
   - The ideal guideline slope shows a continuous linear reduction in remaining story points from 24 to 0 over the 5 working days.
   - In Sprint 1, the burndown chart exhibited a noticeable **plateau between Day 2 and Day 4**. This occurred because **US-04** was sized at 8 story points; while engineers were actively writing and optimizing code, no points were burned on the board until the entire story met the "Definition of Done".
   - *Key Agile Insight:* High-estimate stories (8+ points) obscure daily progress on burndown charts. In future iterations, decomposing 8-point stories into smaller, independently testable 3-point or 2-point increments (e.g., separating cache design from benchmark verification) will ensure a smoother, more predictable burndown trajectory.

3. **Absence of Scope Creep:**
   - In poorly managed sprints, burndown charts frequently show upward spikes (where remaining points increase mid-sprint due to scope creep or unestimated subtasks).
   - Our burndown chart maintained a strictly monotonic non-increasing curve, confirming strong sprint discipline, well-defined acceptance criteria, and protected sprint boundaries.
