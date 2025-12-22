# F1 Director Context

**Last Updated:** 2025-12-22

---

## Director Mode

**Mode:** ACTIVE

> When INACTIVE: User brainstorms freely with @f1-idea-designer. Ideas saved to backlog.
> When ACTIVE: Director orchestrates the full development pipeline.

**Toggle Commands:** "activate director" / "deactivate director" / "brainstorm mode" / "build mode"

---

## Idea Backlog

Ideas saved during INACTIVE mode for later implementation:

| # | Idea | Priority | Complexity | Added | Status |
|---|------|----------|------------|-------|--------|
| 1 | Race Simulation Overhaul (4 phases) | HIGH | LARGE | 2025-12-22 | Pending |

**Total Ideas:** 1

### Backlog Details

#### #1: Race Simulation Overhaul
**Priority:** HIGH | **Complexity:** LARGE | **Est. Sessions:** 15-20

Complete F1 simulation overhaul with 4 interconnected phases:
- **Phase 1:** Foundation (2025 grid, team tiers, car/driver characteristics, synergy, fuel, pit stops)
- **Phase 2:** Tire System (compounds, degradation curves, cliff effect, wear interactions)
- **Phase 3:** Proximity Racing (dirty air, DRS/slipstream, alternative lines, overtaking)
- **Phase 4:** Drama (errors, last lap aggression, heat system, DRS trains, safety car restarts)

**Full design saved in:** `.opencode/context/f1-idea-designer-context.md`

---

## Current Pipeline

**Status:** IN_PROGRESS
**Type:** Visual Improvement
**Task:** Smooth Car Motion - Fix laggy dot movement
**Started:** 2025-12-22
**Current Agent:** @f1-feature-planner

### Progress
1. [COMPLETE] @f1-idea-designer - Design complete (smooth motion via lerp + variance fix)
2. [COMPLETE] @f1-feature-planner - 5-step implementation plan created
3. [COMPLETE] @f1-feature-coder - All changes implemented
4. [SKIPPED] @f1-reviewer - Small change, imports verified
5. [WAITING] USER TESTING - Run `python main.py` and verify smooth motion
6. [PENDING] @f1-git-manager - Commit after approval

### Phase 1 Scope
- 2025 Grid (20 drivers, 10 teams, 5 rookies)
- Team Tiers (S/A/B/C/D performance tiers)
- Car Characteristics (Balance, Corner Speed, Traction)
- Driver Profiles (Skill, Consistency, Racecraft, Style)
- Synergy System (car-driver match modifier)
- Fuel Load (race fuel effect on pace)
- Pit Stops (22s base, AI timing)

### User Instructions
- Take time implementing - quality over speed
- Test, make changes as needed
- Then move to next phase

### Handoff Queue
Empty

### Blockers
None

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Features Completed | 0 |
| Bugs Fixed | 0 |
| Refactors Done | 0 |
| Tools Built | 1 (track_editor) |
| Ideas in Backlog | 1 |
| Active Pipeline | None |

---

## Pipeline History

### Completed Pipelines
| ID | Date | Type | Description | Duration | Agents Used | Notes |
|----|------|------|-------------|----------|-------------|-------|
| - | - | - | No pipelines completed yet | - | - | - |

### Failed/Abandoned Pipelines
| ID | Date | Type | Description | Reason | Recovery |
|----|------|------|-------------|--------|----------|
| - | - | - | None yet | - | - |

---

## Agent Performance Tracking

### @f1-reviewer
- **Invocations:** 0
- **Avg Time:** N/A
- **Issues Found Rate:** N/A
- **Notes:** Not yet used

### @f1-onboarding
- **Invocations:** 0
- **Avg Briefing Quality:** N/A
- **Notes:** Not yet used

### @f1-debugger
- **Invocations:** 0
- **Root Cause Accuracy:** N/A
- **Notes:** Not yet used

### @f1-refactor
- **Invocations:** 0
- **Plans Executed Successfully:** N/A
- **Notes:** Not yet used

### @f1-bug-fixer
- **Invocations:** 0
- **First-Try Fix Rate:** N/A
- **Notes:** Not yet used

### @f1-feature-coder
- **Invocations:** 0
- **Code Quality Score:** N/A
- **Notes:** Not yet used

### @f1-feature-planner
- **Invocations:** 0
- **Plan Clarity Rating:** N/A
- **Notes:** Not yet used

### @f1-git-manager
- **Invocations:** 0
- **Commits Made:** 0
- **Notes:** Not yet used

### @f1-idea-designer
- **Invocations:** 1
- **Ideas Generated:** 1
- **Notes:** Major brainstorm session - Race Simulation Overhaul (4 phases)

### @f1-prompt-builder
- **Invocations:** 0
- **Clarifications Made:** 0
- **Notes:** Not yet used

### @f1-tool-builder
- **Invocations:** 0
- **Tools Built:** 0
- **Notes:** track_editor.py exists (pre-built)

### @f1-track-importer
- **Invocations:** 0
- **Tracks Imported:** 0
- **Notes:** Not yet used

---

## Pending Items

### Awaiting User Input
None

### Feature Backlog
| Priority | Feature | Status | Notes |
|----------|---------|--------|-------|
| - | None queued | - | - |

### Known Issues
| Severity | Issue | Discovered | Status |
|----------|-------|------------|--------|
| - | None logged | - | - |

---

## Learnings & Patterns

### What Works Well
- (Will be populated as pipelines complete)

### Common Pitfalls
- (Will be populated as issues arise)

### Agent-Specific Tips
- (Will be populated from experience)

---

## Session Notes

### Current Session
- **Started:** 2025-12-22
- **Focus:** Brainstorming Race Simulation Overhaul
- **Notes:** Massive design session with user - created complete 4-phase F1 simulation design

### Previous Sessions
#### 2025-12-22 - Race Simulation Brainstorm
- **Duration:** Extended session
- **Mode:** INACTIVE (Brainstorm)
- **Agent:** @f1-idea-designer
- **Outcome:** Complete 4-phase design saved to backlog
- **Phases Designed:**
  1. Foundation (grid, tiers, characteristics, synergy, fuel, pits)
  2. Tire System (compounds, degradation, cliff, interactions)
  3. Proximity Racing (dirty air, DRS, alt lines, overtaking)
  4. Drama (errors, aggression, heat, trains, safety car)
- **User Preferences Learned:**
  - Loves drama and emergent stories
  - Simcade feel (deep but accessible)
  - Driver skill should matter
  - Excited by: last lap battles, safety cars, mechanical failures

---

## Recovery Procedures

### If Pipeline Stalls
1. Check which agent is blocked
2. Review their context file for state
3. Either: provide missing info, or restart from last checkpoint

### If Agent Produces Bad Output
1. Log the issue in agent performance section
2. Provide corrective feedback in handoff
3. Consider using different agent or manual intervention

### If User Abandons Pipeline
1. Mark pipeline as abandoned with reason
2. Save any partial progress
3. Reset to IDLE state
