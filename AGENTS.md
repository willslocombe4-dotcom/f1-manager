# F1 Manager Agent System

A multi-agent development pipeline for the F1 Manager game. Agents collaborate to implement features, fix bugs, and maintain code quality.

---

## Quick Start

| I want to... | Start with |
|--------------|------------|
| Add a new feature | `@f1-director` → routes to pipeline |
| Fix a bug | `@f1-director` → routes to `@f1-debugger` |
| Refactor code | `@f1-director` → routes to `@f1-refactor` |
| Brainstorm ideas | `@f1-idea-designer` |
| Create a track | `python tools/track_editor.py` |
| Check pipeline status | `.opencode/context/f1-director-context.md` |

---

## Agent Overview

### 🎯 Director (Orchestration)
| Agent | Model | Purpose |
|-------|-------|---------|
| `@f1-director` | Claude Opus | Routes tasks, tracks pipeline, coordinates handoffs |

### 🔍 Analysis Agents (Gemini 3 Pro - 2M context)
| Agent | Purpose | Produces |
|-------|---------|----------|
| `@f1-reviewer` | Code review | Approval / change requests |
| `@f1-onboarding` | Feature briefings | Codebase analysis for new features |
| `@f1-debugger` | Bug tracing | Root cause analysis |
| `@f1-refactor` | Refactoring plans | Step-by-step refactor plan |

### 🔨 Implementation Agents (Claude Opus)
| Agent | Purpose | Produces |
|-------|---------|----------|
| `@f1-bug-fixer` | Fix bugs | Minimal, tested fixes |
| `@f1-feature-coder` | Implement features | Working code |
| `@f1-feature-planner` | Plan implementation | Detailed step-by-step plan |
| `@f1-git-manager` | Version control | Clean commits |

### 🛠️ Support Agents (Claude Opus)
| Agent | Purpose | Produces |
|-------|---------|----------|
| `@f1-idea-designer` | Feature design | Feature specifications |
| `@f1-prompt-builder` | Clarify requests | Refined prompts |
| `@f1-tool-builder` | Build dev tools | Standalone tools |
| `@f1-track-importer` | Import tracks | Updated track.py |

---

## Workflows

### 🆕 New Feature
```
User → @f1-director → @f1-prompt-builder (if vague)
                    → @f1-idea-designer (design)
                    → @f1-onboarding (briefing)
                    → @f1-feature-planner (plan)
                    → @f1-feature-coder (implement)
                    → @f1-reviewer (review)
                    → @f1-git-manager (commit)
```

### 🐛 Bug Fix
```
Bug → @f1-director → @f1-debugger (find root cause)
                   → @f1-bug-fixer (fix)
                   → @f1-reviewer (review)
                   → @f1-git-manager (commit)
```

### 🔧 Refactor
```
Request → @f1-director → @f1-refactor (plan)
                       → @f1-feature-coder (implement)
                       → @f1-reviewer (review)
                       → @f1-git-manager (commit)
```

### 🛠️ Tool Building
```
Request → @f1-director → @f1-tool-builder (build)
                       → @f1-reviewer (review)
                       → @f1-git-manager (commit)
```

### 🏎️ Track Import
```
Request → @f1-director → @f1-track-importer (import)
                       → @f1-reviewer (review)
                       → @f1-git-manager (commit)
```

---

## Pipeline Status

Check current pipeline state:
```
.opencode/context/f1-director-context.md
```

Status values:
- `IDLE` - No active pipeline
- `IN_PROGRESS` - Pipeline running
- `BLOCKED` - Waiting for something
- `WAITING_FOR_USER` - User input needed

---

## Agent Files

### Agent Definitions
```
.opencode/agent/
├── f1-director.md          # Orchestrator
├── f1-reviewer.md          # Code review
├── f1-onboarding.md        # Feature briefings
├── f1-debugger.md          # Bug tracing
├── f1-refactor.md          # Refactor planning
├── f1-bug-fixer.md         # Bug fixing
├── f1-feature-coder.md     # Feature implementation
├── f1-feature-planner.md   # Implementation planning
├── f1-git-manager.md       # Git operations
├── f1-idea-designer.md     # Feature design
├── f1-prompt-builder.md    # Request clarification
├── f1-tool-builder.md      # Tool building
└── f1-track-importer.md    # Track import
```

### Context Files (Agent Memory)
```
.opencode/context/
├── f1-director-context.md          # Pipeline status, history
├── f1-reviewer-context.md          # Review history, patterns
├── f1-onboarding-context.md        # Codebase knowledge
├── f1-debugger-context.md          # Bug patterns, history
├── f1-refactor-context.md          # Architecture notes
├── f1-bug-fixer-context.md         # Fix patterns
├── f1-feature-coder-context.md     # Implementation patterns
├── f1-feature-planner-context.md   # Planning templates
├── f1-git-manager-context.md       # Commit history
├── f1-idea-designer-context.md     # Feature backlog
├── f1-prompt-builder-context.md    # Question patterns
├── f1-tool-builder-context.md      # Tool catalog
└── f1-track-importer-context.md    # Track backups
```

---

## Key Handoff Points

### Director → Analysis
- Feature request → `@f1-onboarding`
- Bug report → `@f1-debugger`
- Refactor request → `@f1-refactor`

### Analysis → Implementation
- `@f1-onboarding` → `@f1-feature-planner`
- `@f1-debugger` → `@f1-bug-fixer`
- `@f1-refactor` → `@f1-feature-coder`

### Implementation → Review
- `@f1-feature-coder` → `@f1-reviewer`
- `@f1-bug-fixer` → `@f1-reviewer`

### Review → Git
- `@f1-reviewer` (APPROVED) → `@f1-git-manager`
- `@f1-reviewer` (NEEDS CHANGES) → Back to implementation

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
1. Start with `@f1-director` for new requests
2. Check pipeline status for ongoing work
3. Be specific about what you want
4. Let the pipeline complete before new requests

### For Agents
1. Always update context files
2. Follow handoff protocols exactly
3. Test changes before handoff
4. Document decisions made

---

## Troubleshooting

### Pipeline Stuck?
1. Check `f1-director-context.md` for status
2. Identify blocked agent
3. Check their context file
4. Provide missing info or restart

### Agent Produced Bad Output?
1. Note in agent's context file
2. Provide corrective handoff
3. Consider using different agent

### Need to Rollback?
1. Git: `git checkout -- <files>`
2. Track: Check `f1-track-importer-context.md` for backup

---

## Models Used

| Agent Type | Model | Why |
|------------|-------|-----|
| Analysis | Gemini 3 Pro | 2M context for full codebase |
| Implementation | Claude Opus | Best code generation |
| Director | Claude Opus | Complex orchestration |
