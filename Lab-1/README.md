# Lab 1: Developer Tools & IT Operations

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Course:** Software Engineering Laboratory  
**Problem Statement #43:** Feature Flag & Dynamic Config Manager  
**Source Repository:** [Nagashri2304/LAB1-Developer-Tools-IT-Operations-43](https://github.com/Nagashri2304/LAB1-Developer-Tools-IT-Operations-43)  

---

## Deliverables in this Directory

| File | Type | Description |
| :--- | :---: | :--- |
| [`Lab1_UseCase_Diagram.pdf`](./Lab1_UseCase_Diagram.pdf) | PDF | UML Use-Case Diagram for Feature Flag & Dynamic Config Platform (Actors: Software Engineer, Release Manager, Client App SDK; Use Cases: UC-01 to UC-07). |
| [`Lab1_UseCase_Flow_UC06.docx`](./Lab1_UseCase_Flow_UC06.docx) | Word | Use-Case Flow Specification for **UC-06: Approve & Publish Flag Change** (Main Success Scenario, Preconditions, Postconditions, and Alternate Flows). |
| [`requirments_table.xlsx`](./requirments_table.xlsx) | Excel | Functional & Non-Functional Requirements Table (FR-001 through FR-005, NFR-001, NFR-002) with Descriptions, Priorities, Rationale, and Acceptance Criteria. |

---

## Requirements Summary

- **FR-001:** Evaluate user targeting rules and return accurate boolean feature-flag state (High Priority).
- **FR-002:** Create new feature flag with unique key, description, and default state (High Priority).
- **FR-003:** Configure percentage-based rollout (0–100%) using deterministic hash of user ID (High Priority).
- **FR-004:** Define environment-specific overrides (Development, Staging, Production) (Medium Priority).
- **FR-005:** Push updated flag states to connected client SDKs in real time via streaming connection (High Priority).
- **NFR-001:** Feature-flag evaluation API executes in under 15 ms p95 (High Priority).
- **NFR-002:** Role-based access control and immutable audit logging for all configuration changes (High Priority).
