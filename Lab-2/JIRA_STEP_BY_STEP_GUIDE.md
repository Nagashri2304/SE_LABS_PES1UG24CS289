# Jira Step-by-Step Execution & Demonstration Guide

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Problem Statement #43:** Feature Flag & Dynamic Config Manager  
**Course:** Software Engineering Laboratory – Lab 2  

---

## Overview

This guide walks you through setting up and demonstrating your **Jira Project** for Lab 2 in under 5 minutes using the pre-configured deliverables in this directory (`Lab-2/jira_import_lab2.csv`).

When your instructor evaluates your lab, they will ask you to show:
1. **Backlog view:** Showing all Epics, User Stories, and Story Point assignments.
2. **Active Sprint view:** Demonstrating work items moving across *To Do* → *In Progress* → *Done*.
3. **Reports / Burndown Chart:** Displaying the story point burndown curve over the sprint.

Follow the exact steps below.

---

## Step 1: Create Your Jira Scrum Project

1. Log in to your Atlassian Jira account (e.g. `https://your-domain.atlassian.net`).
2. In the top navigation bar, click **Projects** → **Create project** (or click the **+** logo next to Projects).
3. Under *Software development*, select **Scrum**.
4. Click **Use template**.
5. When prompted to choose a project type, select **Company-managed** (as specified on Page 4 of the lab handout).
6. Fill in the project details:
   - **Name:** `Feature Flag & Dynamic Config Manager` (or `Feature-Flag-Manager`)
   - **Key:** `FFM` (or `DCM`)
7. Click **Create project** / **Next**. Your SCRUM Board is now created!

---

## Step 2: Enable the Epic Panel in Backlog

1. From the left sidebar, click on **Backlog**.
2. Press the **"E"** key on your keyboard, OR click the **Epic** dropdown button at the top of the backlog and toggle on **Show epic panel** (refer to Page 7 of your lab handout).
3. You will now see the Epic panel on the left side of your backlog view.

---

## Step 3: Fast-Track Issue Population (Using CSV Import)

You can import all 4 Epics and 10 User Stories in 30 seconds using the provided `jira_import_lab2.csv`:

1. In Jira, click the **Settings (gear icon)** in the top right → **System** (or click **Filters** → **View all issues** → **... (top right)** → **Import issues from CSV**).
2. Alternatively, in your project view, click the **...** menu in the top right corner of the Backlog and select **Import issues from CSV**.
3. Choose the file `Lab-2/jira_import_lab2.csv` from this repository.
4. Select your project (`FFM - Feature Flag & Dynamic Config Manager`).
5. Map the fields:
   - `Issue Type` → **Issue Type**
   - `Summary` → **Summary**
   - `Description` → **Description**
   - `Priority` → **Priority**
   - `Story Points` → **Story Points**
   - `Epic Name` → **Epic Name**
   - `Sprint` → **Sprint**
6. Click **Begin Import**. All Epics and User Stories are now instantly populated!

*(If you prefer to create items manually, see the Backlog Catalog in `README.md` and follow Pages 6–15 of the lab handout).*

---

## Step 4: Run Sprint 1 Simulation

1. Go to the **Backlog** view.
2. At the top of the Backlog list, you will see **Sprint 1** (or click **Create sprint** to generate it).
3. Ensure the following 5 user stories are inside **Sprint 1** (total 24 story points):
   - `US-01: Create Feature Flag with Unique Key and Default State` (3 pts)
   - `US-02: Configure Deterministic Percentage-Based Rollout` (5 pts)
   - `US-03: Evaluate User Targeting Rules for Cohorts` (5 pts)
   - `US-04: Optimize Evaluation API Engine to Sub-15ms Latency` (8 pts)
   - `US-05: Implement Client SDK Local Cache and Fallback` (3 pts)
4. Click **Start sprint** (top right of the sprint box):
   - **Sprint name:** `FFM Sprint 1`
   - **Duration:** `1 week`
   - **Sprint goal:** `Establish core flag lifecycle management, deterministic percentage rollouts, and sub-15ms engine performance.`
   - Click **Start**.
5. Jira takes you to the **Active sprints** board:
   - All 5 user stories start in the **TO DO** column.
   - Drag **US-01** and **US-05** to **IN PROGRESS**, wait a few seconds, then drag to **DONE**.
   - Drag **US-02** and **US-03** to **IN PROGRESS**, then drag to **DONE**.
   - Drag **US-04** to **IN PROGRESS**, then drag to **DONE**.
6. When all tasks are in **DONE**, click the blue button **Complete sprint** in the top right corner.
7. Click **Complete sprint** in the confirmation dialog. Sprint 1 is complete!

---

## Step 5: Run Sprint 2 Simulation

1. Go back to the **Backlog** view.
2. Click **Create sprint** to create **Sprint 2**.
3. Drag the remaining 5 user stories from the Backlog into **Sprint 2** (total 23 story points):
   - `US-06: Define Environment-Specific Configuration Overrides` (5 pts)
   - `US-07: Draft Flag Revisions and Preview Visual Configuration Diff` (3 pts)
   - `US-08: Release Manager Review, Approval Gate, and Validation` (5 pts)
   - `US-09: Immutable Audit Logging and One-Click Rollback` (5 pts)
   - `US-10: Real-Time Flag State Streaming to Connected SDKs` (5 pts)
4. Click **Start sprint**:
   - **Sprint name:** `FFM Sprint 2`
   - **Duration:** `1 week`
   - **Sprint goal:** `Implement multi-environment isolation, release manager approval workflow, immutable audit logging, and real-time SDK streaming.`
   - Click **Start**.
5. On the **Active sprints** board, simulate progress by dragging work items from **TO DO** → **IN PROGRESS** → **DONE**.
6. Once all tasks are in **DONE**, click **Complete sprint**. Sprint 2 is complete!

---

## Step 6: View and Screenshot the Burndown Chart

1. From the project left navigation pane, click **Reports** (or click the **Reports** tab at the top of the board).
2. Click on **Burndown Chart**.
3. Under the sprint dropdown, select **FFM Sprint 1** (or **FFM Sprint 2**).
4. Select the estimation statistic as **Story Points**.
5. Take screenshots of:
   - Backlog with Epics and Story Points
   - Active Sprint board with items in To Do / In Progress / Done
   - Burndown Chart report
6. Save these screenshots into your lab folder for submission alongside the generated PDF!
