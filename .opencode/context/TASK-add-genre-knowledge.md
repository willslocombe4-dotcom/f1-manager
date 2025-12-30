# Task: Add F1 Manager Genre Knowledge to All Agents

## Context

The F1 Manager project has an 8-agent development pipeline located in `.opencode/agent/`. These agents help design, plan, build, review, and deploy features for a pygame-based F1 racing manager game.

**Current agents:**
- `f1-designer.md` - Brainstorms features with user
- `f1-director.md` - Orchestrates the build pipeline
- `f1-tool-designer.md` - Designs development tools
- `f1-planner.md` - Creates implementation plans
- `f1-builder.md` - Implements features
- `f1-toolmaker.md` - Builds dev tools
- `f1-reviewer.md` - Reviews code quality
- `f1-ops.md` - Handles git/deployment

## The Task

Add comprehensive F1 Manager genre knowledge to help agents make better decisions. This knowledge should come from successful games in the genre.

## Games to Research

### Primary References
1. **F1 Manager 2022/2023/2024** (Frontier Developments) - The official F1 management games
2. **Motorsport Manager** (Playsport Games) - Highly acclaimed racing management
3. **Grand Prix Manager 1 & 2** (MicroProse) - Classic deep simulations

### Secondary References
4. **iGP Manager** - Browser-based, good mobile patterns
5. **GPRO** - Online multiplayer management
6. **Racing Manager** - Mobile-focused design

## What to Create

### 1. Shared Knowledge Base File
Create: `.opencode/context/f1-genre-knowledge.md`

Include sections:
```markdown
# F1 Manager Genre Knowledge Base

## Core Gameplay Loops
[What makes these games satisfying - the moment-to-moment and season-long loops]

## Standard Features (Table Stakes)
[Features players EXPECT - race day, driver management, car development, etc.]

## Advanced Features (Differentiators)
[Features that make games stand out - unique systems, innovations]

## UI Patterns
### Timing Tower
[How games display race positions, gaps, tire info]

### Strategy Screen  
[Pit stop planning, tire strategy, fuel management UIs]

### Car Development
[R&D trees, upgrade systems, testing interfaces]

### Team Management
[Staff, facilities, sponsors, finances]

## Data Structures (Common Patterns)
[How games typically structure driver stats, car performance, etc.]

## Player Expectations
### What Players Love
[Features and polish that get praised]

### What Players Hate  
[Common complaints, things to avoid]

### Accessibility Levels
[Casual vs Simulation - how games handle difficulty/depth]

## Complexity Reference
[How complex each feature type typically is to implement]
```

### 2. Update Each Agent

Add a new section to each agent file referencing the knowledge base:

**For f1-designer.md** - Add:
```markdown
## Genre Knowledge

Read `.opencode/context/f1-genre-knowledge.md` when:
- User asks for feature ideas
- Evaluating if a feature is "standard" or "innovative"
- Estimating complexity
- Suggesting UI patterns

Key questions to consider:
- Does F1 Manager 2024 have this?
- How does Motorsport Manager handle this?
- Is this a "table stakes" feature?
```

**For f1-planner.md** - Add:
```markdown
## Genre Reference

Consult `.opencode/context/f1-genre-knowledge.md` for:
- Complexity estimates based on industry implementations
- Data structure patterns that work well
- UI layout conventions
- Integration considerations
```

**For f1-builder.md** - Add:
```markdown
## Genre Patterns

Reference `.opencode/context/f1-genre-knowledge.md` for:
- UI component patterns (timing towers, strategy screens)
- Data structures for driver/car/team management
- Performance considerations from similar games
```

**For f1-reviewer.md** - Add:
```markdown
## Genre Standards

Check against `.opencode/context/f1-genre-knowledge.md`:
- Does this match player expectations?
- Is the UI pattern familiar to genre fans?
- Are we missing standard functionality?
```

## Research Approach

1. **Official Game Features** - List what F1 Manager 2024 includes
2. **Steam Reviews** - What do players praise/criticize?
3. **YouTube Playthroughs** - See actual UI and gameplay
4. **Wiki/Fan Sites** - Detailed feature breakdowns
5. **Reddit Discussions** - r/F1Manager, r/MotorsportManagerPC

## Deliverables

1. [ ] Create `.opencode/context/f1-genre-knowledge.md` (comprehensive knowledge base)
2. [ ] Update `f1-designer.md` with genre reference section
3. [ ] Update `f1-planner.md` with genre reference section  
4. [ ] Update `f1-builder.md` with genre reference section
5. [ ] Update `f1-reviewer.md` with genre reference section
6. [ ] Optionally update other agents if relevant

## File Locations

All files are in: `D:\game dev\f1_manager\`

```
.opencode/
├── agent/
│   ├── f1-designer.md      # UPDATE
│   ├── f1-director.md      
│   ├── f1-tool-designer.md 
│   ├── f1-planner.md       # UPDATE
│   ├── f1-builder.md       # UPDATE
│   ├── f1-toolmaker.md     
│   ├── f1-reviewer.md      # UPDATE
│   └── f1-ops.md           
└── context/
    ├── f1-genre-knowledge.md  # CREATE (new file)
    └── [other context files]
```

## Success Criteria

- Agents can reference real games when discussing features
- Complexity estimates grounded in industry reality
- UI patterns match genre conventions
- Players get features they expect from the genre
- Agents avoid "reinventing the wheel"

---

## Quick Start Prompt

Copy this to start the task:

```
I need you to add F1 Manager genre knowledge to my agent system.

Read `.opencode/context/TASK-add-genre-knowledge.md` for full instructions.

In summary:
1. Research F1 Manager 2024, Motorsport Manager, and Grand Prix Manager
2. Create a knowledge base at `.opencode/context/f1-genre-knowledge.md`
3. Update f1-designer, f1-planner, f1-builder, and f1-reviewer agents to reference it

Focus on: core features, UI patterns, player expectations, and complexity benchmarks.
```
