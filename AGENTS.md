# F1 Manager Agent System

A streamlined multi-agent development pipeline for the F1 Manager game. **8 agents** (down from 14) with clear responsibilities.

---

## Quick Start

| I want to... | Do this |
|--------------|---------|
| **Brainstorm features** | Tab to `@f1-designer` |
| **Build a feature** | Tab to `@f1-director` → "build [feature]" |
| **Build from backlog** | Tab to `@f1-director` → "process backlog" |
| **Design a tool** | Tab to `@f1-tool-designer` |
| **Create a track** | `python tools/track_editor.py` |

---

## Agent Overview

### Primary Agents (Tab to switch)

| Agent | Model | Purpose |
|-------|-------|---------|
| `@f1-designer` | Gemini | Brainstorms game features, codebase-aware |
| `@f1-director` | Gemini | Orchestrates build pipeline |
| `@f1-tool-designer` | Gemini | Designs dev tools |

### Subagents (Invoked automatically or via @mention)

| Agent | Model | Purpose |
|-------|-------|---------|
| `@f1-planner` | Gemini | Analyzes codebase, creates implementation plans |
| `@f1-builder` | Opus | Implements features, fixes bugs |
| `@f1-toolmaker` | Opus | Builds dev tools |
| `@f1-reviewer` | Gemini | Reviews code before commit |
| `@f1-ops` | Opus | Git commits, track imports |

### Model Strategy
- **Gemini** = Reading, analyzing, deciding (2M context)
- **Opus** = Writing code (best code generation)

---

## Workflows

### Feature Pipeline
```
You ↔ @f1-designer (brainstorm)
         ↓ "save to backlog" or "build this"
    @f1-director
         ↓
    @f1-planner (analyze + plan)
         ↓
    @f1-builder (implement)
         ↓
    @f1-reviewer (review)
         ↓
    YOU TEST
         ↓ "works!" or "bug: [description]"
    @f1-ops (commit)
```

### Bug Fix Pipeline
```
You → @f1-director → "fix [bug]"
                          ↓
                    @f1-builder (analyze + fix)
                          ↓
                    @f1-reviewer
                          ↓
                    YOU TEST → @f1-ops
```

### Tool Pipeline
```
You ↔ @f1-tool-designer (design)
         ↓ "build this"
    @f1-toolmaker (implement)
         ↓
    @f1-reviewer → YOU TEST → @f1-ops
```

---

## Feature Backlog

Ideas are saved in `@f1-designer`'s context file. To build one:

1. Tab to `@f1-director`
2. Say "process backlog"
3. Pick an idea
4. Pipeline runs automatically

---

## Agent Files

### Active Agents
```
.opencode/agent/
├── f1-designer.md       # Primary - feature brainstorming
├── f1-director.md       # Primary - pipeline orchestration
├── f1-tool-designer.md  # Primary - tool design
├── f1-planner.md        # Subagent - analysis + planning
├── f1-builder.md        # Subagent - implementation
├── f1-toolmaker.md      # Subagent - tool building
├── f1-reviewer.md       # Subagent - code review
└── f1-ops.md            # Subagent - git + imports
```

### Archived Agents
```
.opencode/agent/archived/
├── f1-bug-fixer.md      # → merged into f1-builder
├── f1-debugger.md       # → merged into f1-builder
├── f1-feature-coder.md  # → merged into f1-builder
├── f1-feature-planner.md # → merged into f1-planner
├── f1-git-manager.md    # → renamed to f1-ops
├── f1-idea-designer.md  # → renamed to f1-designer
├── f1-onboarding.md     # → merged into f1-planner
├── f1-prompt-builder.md # → merged into f1-designer
├── f1-refactor.md       # → merged into f1-planner
├── f1-tool-builder.md   # → renamed to f1-toolmaker
└── f1-track-importer.md # → merged into f1-ops
```

### Context Files
```
.opencode/context/
├── f1-designer-context.md      # Feature backlog, preferences
├── f1-director-context.md      # Pipeline status
├── f1-tool-designer-context.md # Tool ideas
├── f1-planner-context.md       # Codebase knowledge
├── f1-builder-context.md       # Implementation patterns
├── f1-toolmaker-context.md     # Tool patterns
├── f1-reviewer-context.md      # Review history
└── f1-ops-context.md           # Commit history, backups
```

---

## Architecture Reference

### Game Structure
```
main.py                 # Game loop, F1Manager class
config.py               # All constants
race/
├── race_engine.py      # RaceEngine: simulation
├── car.py              # Car: state, movement
└── track.py            # Track: waypoints
ui/
├── renderer.py         # TrackRenderer: visuals
├── timing_screen.py    # TimingScreen: timing tower
└── results_screen.py   # ResultsScreen: final standings
data/
└── teams.py            # Team/driver data
assets/
└── colors.py           # Color mappings
tools/
├── track_editor.py     # Track creation tool
└── tracks/             # Saved/exported tracks
```

### Data Flow
```
F1Manager.run() loop:
  → handle_events()        # User input
  → RaceEngine.update()    # Move cars, calc positions
  → TrackRenderer.render() # Draw track/cars
  → TimingScreen.render()  # Draw timing
```

---

## Best Practices

### For Users
1. **Brainstorm with @f1-designer** — ideas get saved to backlog
2. **Build with @f1-director** — say "process backlog" or describe feature
3. **Test before commit** — you're the final quality gate
4. **Be specific** — clear requests = better results

### For Agents
1. Update context files after actions
2. Follow handoff protocols
3. Test changes before handoff
4. Document decisions made

---

## Migration Notes (Dec 2025)

Consolidated from 14 agents to 8:

| Old Agents | New Agent |
|------------|-----------|
| idea-designer + prompt-builder | `@f1-designer` |
| onboarding + feature-planner + refactor | `@f1-planner` |
| feature-coder + bug-fixer + debugger | `@f1-builder` |
| git-manager + track-importer | `@f1-ops` |
| tool-builder | `@f1-toolmaker` |
| reviewer | `@f1-reviewer` (unchanged) |
| director | `@f1-director` (simplified) |
| (new) | `@f1-tool-designer` |

**Why?** Fewer handoffs = faster iteration. Each agent now does more in one session.
