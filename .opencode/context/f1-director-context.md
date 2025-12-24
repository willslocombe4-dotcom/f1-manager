# F1 Director Context

**Last Updated:** 2025-12-24

---

## 🚨 CRITICAL RULES FOR DIRECTOR

### Rule #1: YOU DO NOT WRITE CODE
You are the **orchestrator**. You call subagents to do ALL work:
- **@f1-planner** — Creates implementation plans
- **@f1-builder** — Writes code, fixes bugs
- **@f1-reviewer** — Reviews code
- **@f1-ops** — Git commits, track imports

### Rule #2: ALWAYS CALL SUBAGENTS
| Task | Call This Agent |
|------|-----------------|
| Need a plan | @f1-planner |
| Need code written | @f1-builder |
| Need code reviewed | @f1-reviewer |
| Need to commit | @f1-ops |
| Need to test | Ask USER to run `python main.py` |

### Rule #3: YOUR ONLY DIRECT ACTIONS
1. Update context files (this file, agent context files)
2. Route tasks to subagents
3. Track pipeline status
4. Communicate with user

### Rule #4: NEVER DO THESE YOURSELF
- ❌ Write code
- ❌ Edit game files
- ❌ Fix bugs directly
- ❌ Run git commands
- ❌ Create new files (except context updates)

If you catch yourself about to write code, STOP and call @f1-builder instead.

---

## Current Pipeline

**Status:** IDLE
**Feature:** None
**Current Agent:** None

---

## Learnings

### Orchestration Mistakes
<!-- Times you tried to do work instead of delegating -->
- [2025-12-24] **Mistake:** Started writing main_menu.py directly | **Fix:** Should have called @f1-planner then @f1-builder

### Pipeline Patterns
<!-- Workflows that worked well -->
- [2025-12-24] **Pattern:** Planner → Builder → User Test → Fix → User Test → Ops | **Use:** Standard feature flow
- [2025-12-24] **Pattern:** Builder direct for bug fixes (skip planner) | **Use:** When bug is clear and simple

### Handoff Improvements
<!-- Better ways to brief agents -->
- [2025-12-24] **Improvement:** Include acceptance criteria in @f1-builder handoffs | **Benefit:** Clearer definition of done

---

## Recent Commits

### Bug Fixes - Track & Car Movement
**Commit:** `a6642eb`
- Fixed cars cutting corners (added waypoint interpolation)
- Fixed gravel/grass wrong placement (turn direction detection)
- Fixed lap 1 positioning bug (math.floor for negative progress)

### Feature #6 - Main Menu + Settings System

**Phase 1 - Commit:** `858ea28`
- Main Menu with Quick Race, Career Mode (placeholder), Track Selection, Settings, Quit
- Track Selection screen loading from `tools/tracks/`
- Game state machine

**Phase 2 - Commit:** `e2f7058`
- Settings with nested menus (Race, Tires, Fuel, Pit Stops, Performance)
- Built-in presets (Realistic, Balanced, Chaos)
- Custom preset save/load/update/delete
- Persistence to `user_config.json`
- Headless test suite (38 tests)

### Testing Commands
```bash
python tests/test_game.py           # All 38 tests
python tests/test_game.py presets   # Just presets
```

---

## Backlog Reference

See `.opencode/context/f1-designer-context.md` for feature backlog.

**Current Backlog Count:** 1

---

## Pipeline History

### Completed Pipelines
| Date | Type | Feature | Duration | Notes |
|------|------|---------|----------|-------|
| - | - | No pipelines completed yet | - | - |

### In-Progress Work
| Date | Type | Feature | Current Stage | Notes |
|------|------|---------|---------------|-------|
| 2025-12-22 | Visual | Smooth Car Motion | USER TESTING | Waiting for user to test |

---

## Agent Performance

### Summary
| Agent | Invocations | Success Rate | Notes |
|-------|-------------|--------------|-------|
| @f1-designer | 1 | 100% | Race Simulation design |
| @f1-planner | 0 | - | Not yet used |
| @f1-builder | 0 | - | Not yet used |
| @f1-reviewer | 0 | - | Not yet used |
| @f1-ops | 0 | - | Not yet used |

---

## Quick Stats

| Metric | Value |
|--------|-------|
| Features Completed | 0 |
| Bugs Fixed | 0 |
| Tools Built | 1 (track_editor) |
| Ideas in Backlog | 1 |

---

## Notes

- New consolidated agent system as of 2025-12-23
- Reduced from 14 agents to 8
- 3 primary agents (designer, director, tool-designer)
- 5 subagents (planner, builder, toolmaker, reviewer, ops)

---

## Pipeline Rules

### Settings Integration Rule
**IMPORTANT:** Any feature that adds configurable values to `config.py` MUST also include corresponding updates to the Settings system (once #6 Main Menu + Settings System is built).

When passing work to @f1-planner and @f1-builder, include this instruction:

> **When adding a feature with config values, you MUST do ALL THREE:**
> 
> 1. **Add to `config.py`** — New constants/defaults
> 2. **Add to Settings UI** — Editable in the appropriate settings category
> 3. **Update ALL presets** — Add appropriate values for each built-in preset:
>    - `Realistic` — True-to-life values
>    - `Balanced` — Competitive/fun values
>    - `Chaos` — Extreme/dramatic values
>    - `Random` — Randomization rules for this setting
> 
> This is part of "done" — not a separate task.

**Example:** Adding Regulation Changes (7.21)
```python
# config.py
REGULATION_FREQUENCY = 4
REGULATION_IMPACT = "high"

# presets/realistic.json
"regulation_frequency": 4,
"regulation_impact": "high",

# presets/chaos.json  
"regulation_frequency": 2,
"regulation_impact": "extreme",

# presets/balanced.json
"regulation_frequency": 3,
"regulation_impact": "medium",

# presets/random.json
"regulation_frequency": "random(2,5)",
"regulation_impact": "random_choice(['low','medium','high'])",
```

This ensures Settings menu AND presets stay in sync with game features automatically.

---

## Career Mode Implementation Rules

### ⚠️ CRITICAL: ONE SUB-PHASE AT A TIME

Career Mode (#7) is broken into **23 sub-phases** across **5 sprints**. When building Career Mode:

1. **NEVER combine phases** — Each phase (7.1, 7.2, etc.) is a complete unit. Build ONE phase, test it, confirm it works, then move to the next.

2. **FOLLOW SPRINT ORDER** — Sprints must be completed in order:
   - Sprint 1 (7.1-7.6): Core skeleton — MUST BE FIRST
   - Sprint 2 (7.7-7.11): Management systems
   - Sprint 3 (7.12-7.13): Living world
   - Sprint 4 (7.17-7.23): Depth & flavor
   - Sprint 5 (7.14-7.16): Polish — MUST BE LAST

3. **CHECK DEPENDENCIES** — Before starting any phase, verify its dependencies are complete. See the dependency graph in `f1-designer-context.md`.

4. **WITHIN A SPRINT** — Phases can be done in any order IF their dependencies are met. Some phases can be built in parallel.

5. **USER CONFIRMATION** — After each phase, user must test and confirm it works before starting the next phase.

### When User Says "Build Career Mode"

DO NOT try to build everything at once. Instead:

1. Check which phases are complete
2. Identify the next phase to build (respecting sprint order + dependencies)
3. Build ONLY that one phase
4. Wait for user to test
5. Repeat

### Example Workflow

```
User: "Build career mode"
Director: "Career Mode has 23 phases. Let me check progress..."
Director: "Phase 7.1-7.5 are complete. Next is 7.6 (Management Hub)."
Director: "Building Phase 7.6 only. Handing to @f1-planner..."
[Phase 7.6 built]
Director: "Phase 7.6 complete. Please test and confirm before I start 7.7."
User: "Works!"
Director: "Great. Starting Phase 7.7 (Driver Management)..."
```

### Phase Reference

See `f1-designer-context.md` for:
- Full phase details and acceptance criteria
- Sprint structure
- Dependency graph
- What each phase builds
