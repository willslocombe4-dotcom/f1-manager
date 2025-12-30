# F1 Designer Context

**Last Updated:** 2025-12-28

---

## Feature Backlog

Ideas saved for later implementation:

| # | Feature | Priority | Complexity | Added | Status | Depends On |
|---|---------|----------|------------|-------|--------|------------|
| 1 | Phase 1: Foundation | HIGH | LARGE | 2025-12-22 | ✅ DONE | — |
| 2 | Phase 2: Advanced Tire System | HIGH | MEDIUM | 2025-12-22 | Pending | #1 |
| 3 | Phase 3: Proximity Racing | HIGH | LARGE | 2025-12-22 | Pending | #1 |
| 4 | Phase 4: Drama & Chaos | MEDIUM | LARGE | 2025-12-22 | Pending | #1 |
| 5 | Tire Wear Bar on Timing Screen | LOW | SMALL | 2025-12-24 | Pending | #1 |
| 6 | Main Menu + Settings System | HIGH | HIGH | 2025-12-24 | ✅ DONE | — |
| 7 | Career Mode - Core Systems | HIGH | LARGE | 2025-12-27 | Pending | — |
| 8 | Smart Track Boundaries (Kerb Fix) | HIGH | MEDIUM | 2025-12-25 | ✅ DONE | — |
| 9 | Qualifying Weekend Mode | HIGH | LARGE | 2025-12-27 | Pending | #1 |
| 10 | Dynamic Pit Strategy Manager | HIGH | MEDIUM | 2025-12-27 | Pending | #1 |
| 11 | Tire Performance Graph | HIGH | SMALL | 2025-12-27 | Pending | #1 |
| 12 | Race Strategy Timeline | HIGH | MEDIUM | 2025-12-27 | Pending | #1 |
| 13 | Team Radio Commands (Simplified) | MEDIUM | MEDIUM | 2025-12-27 | Pending | #1 |
| 14 | Pit Window Strategy Overlay | MEDIUM | SMALL | 2025-12-27 | Pending | #1 |
| 15 | Sector Indicators (Refined) | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 16 | Race Start Lights (Refined) | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 17 | Live Position Mini-Map | LOW | SMALL | 2025-12-27 | Pending | #1 |
| 18 | Display Settings & Menu Rename | HIGH | SMALL | 2025-12-28 | Pending | — |

**Status Legend:**
- ✅ DONE - Fully implemented and working
- 🔧 PARTIAL - Started but not complete
- Pending - Not started

**Total:** 18 features (3 complete, 0 partial, 15 pending)

---

## What's Actually In The Game

### ✅ Fully Implemented:
1. **Phase 1: Foundation**
   - 2025 F1 grid (all 10 teams, 20 drivers)
   - Team performance tiers (S/A/B/C/D)
   - Car characteristics (balance, cornering, traction)
   - Driver attributes (skill, consistency, racecraft, style, rookie status)
   - Driver-car synergy system
   - Fuel load effects (heavy → light)
   - AI-controlled pit stops
   - Tire degradation with cliff effect
   - Basic race simulation with timing tower
   - Results screen with scrolling

2. **Main Menu + Settings System**
   - Main menu with all options
   - Track selection screen (working)
   - Settings menu with categories
   - Runtime config system
   - Settings persistence (save/load)
   - Most gameplay settings implemented
   - Teams/Drivers settings are placeholders

3. **Smart Track Boundaries**
   - Fixed kerb rendering at hairpins
   - Bevel-join system for corners
   - No more visual glitches

### ❌ Not Implemented:
- Advanced tire thermal model
- Proximity racing (dirty air, DRS, slipstream)
- Drama systems (errors, safety cars, failures)
- Career mode (entire system)
- Strategic features (manual pit stops, radio commands, etc.)
- Display/resolution settings

---

## Feature Details

### #18: Display Settings & Menu Rename
**Priority:** HIGH | **Complexity:** SMALL | **Added:** 2025-12-28 | **Status:** Pending

Rename current "Settings" to "Config" and add new "Settings" for display options.

**Changes:**
1. **Main Menu rename:**
   - "SETTINGS" → "CONFIG" (for gameplay configuration)
   - Add new "SETTINGS" option (for display/video settings)

2. **New Settings Screen features:**
   - Fullscreen mode (always on)
   - Resolution display (auto-detected, e.g., 3840x2160)
   - UI scaling (automatic based on resolution)
   - Future: UI scale slider, performance options

**Implementation:**
- Auto-detect native screen resolution on startup
- Calculate scale factor from base 1600x900
- Scale all UI elements proportionally (track, cars, fonts, spacing)
- Game always launches in fullscreen at native resolution
- Settings screen shows current resolution for reference

**Why needed:**
- Current 1600x900 window is too small on 4K displays
- Fullscreen provides better immersion
- Auto-scaling ensures UI is readable at any resolution

---

## Learnings

### User Preferences
<!-- What they like, what they reject, their style -->
- [2025-12-24] **Preference:** User wants agents to learn and improve over time | **Lesson:** Build learning systems into agent workflows
- [2025-12-27] **Preference:** User likes using multiple agents in parallel for brainstorming | **Lesson:** Kick off 10 agents to explore different angles of complex features
- [2025-12-28] **Preference:** User has 4K display (3840x2160) and wants fullscreen | **Lesson:** Consider high-res displays in UI design

### Conversation Wins
<!-- Approaches that led to good designs -->
- [2025-12-24] **Win:** Ask 1-2 questions per exchange, not 5+ | **Lesson:** Keeps conversation flowing naturally
- [2025-12-27] **Win:** Parallel agent exploration for complex features | **Lesson:** 10 agents exploring different aspects (UI, mechanics, AI, etc.) produces comprehensive designs quickly
- [2025-12-28] **Win:** Quick clarification on naming confusion | **Lesson:** Verify understanding before assuming intent

### Codebase Constraints
<!-- Technical limits that affect design -->
- [2025-12-24] **Constraint:** Settings system uses RuntimeConfig singleton | **Lesson:** New features with config must integrate with it
- [2025-12-24] **Constraint:** UI screens cache values at creation | **Lesson:** Designs must account for cache invalidation
- [2025-12-28] **Constraint:** Game hardcoded to 1600x900 resolution | **Lesson:** Need dynamic sizing for different displays

### Design Revisions
<!-- Designs that needed changes, why -->
- [2025-12-24] **Revision:** Track selection initially started race on select | **Lesson:** Confirm UX flow with user before finalizing

---

### ⚠️ Build Order Note
Career Mode can now be built since Main Menu exists.

### 📋 Career Mode Design
**Full design document saved at:** `.opencode/context/f1-career-mode-design.md`
- Streamlined from 23 phases to 8 core systems
- Ready for implementation by @f1-director

---

#### #7: Career Mode - Core Systems (Streamlined to 8 Phases)
**Priority:** HIGH | **Complexity:** LARGE | **Est. Sessions:** 15-20

Full team principal career spanning multiple seasons. Manage finances, develop your car, hire staff, negotiate contracts.

**Design Philosophy:**
- AI teams use exact same systems as player (no fake bonuses)
- Money is the universal resource connecting all systems
- Simple core systems with expansion hooks for future features
- Every decision has trade-offs

---

**PHASE 1: Team Selection**
Choose from 10 F1 teams, each with different starting conditions:

| Team | Tier | Starting Budget | Car Performance | Expectations |
|------|------|-----------------|-----------------|--------------|
| Red Bull | S | $180M | 95% | Win championship |
| Ferrari | S | $175M | 93% | Win races |
| Mercedes | S | $170M | 92% | Podiums |
| McLaren | A | $140M | 88% | Top 5 finishes |
| Aston Martin | A | $130M | 86% | Points finishes |
| Alpine | B | $100M | 82% | Midfield battles |
| Williams | C | $70M | 78% | Beat teammate |
| Alfa Romeo | C | $65M | 77% | Avoid last |
| Haas | D | $55M | 75% | Survive |
| AlphaTauri | B | $95M | 81% | Development |

AI principals manage the other 9 teams with personality-driven decisions.

---

**PHASE 2: Season Calendar**
- 23 races following real F1 calendar
- Each track has characteristics affecting car performance
- Weather probability per track (Monaco 20% rain, Spa 60% rain)
- Development days between races for upgrades/decisions

---

**PHASE 3: Driver Management**
Drivers have 5 attributes + morale:
- **Skill** (70-99): Raw pace
- **Consistency** (60-95): Lap time variance  
- **Racecraft** (65-95): Overtaking/defending
- **Style**: Aggressive/Smooth/Adaptive
- **Experience** (0-100): Grows over time
- **Morale** (0-100): Affects all performance (-10% when unhappy)

Chemistry with teammate impacts both drivers' morale.

---

**PHASE 4: Contract Negotiations**
Point-allocation negotiation system:

| Demand Type | Description | Points Cost |
|-------------|-------------|-------------|
| Base Salary | $ per year | 1pt = $1M |
| Win Bonus | $ per win | 1pt = $100k |
| Podium Bonus | $ per podium | 1pt = $50k |
| #1 Status | Team priority | 5 points |
| Performance Clause | Can exit if team underperforms | 3 points |

Drivers arrive with point demands based on their tier. You allocate your offer.

---

**PHASE 5: Car Development**
Money-driven upgrade system with cost cap pressure.

**Development Areas:**
1. **Power Unit** - Top speed & acceleration
2. **Aerodynamics** - Cornering & balance
3. **Reliability** - Reduces DNF chance

**Upgrade Pipeline:**
| Type | Cost | Time | Benefit |
|------|------|------|---------|
| Small | $5M | 2 races | +0.5% |
| Medium | $10M | 4 races | +1.0% |
| Major | $20M | 6 races | +2.0% |

**Cost Cap:** $140M per season
- $1-5M over: -10 championship points
- $5-10M over: -25 points + grid penalties  
- $10M+ over: DSQ from constructors

---

**PHASE 6: Financial System**
Income from sponsors during season, prize money at season end.

**Sponsor Slots (3 per team):**

| Slot | Base Payment | Top 5 Bonus | Win/Podium Bonus |
|------|--------------|-------------|------------------|
| Title | $5M/race | +$3M | +$5M |
| Major | $2M/race | +$1M (top 10) | +$2M |
| Minor | $1M/race | +$0.5M (finish) | +$0.5M (points) |

**Prize Money (Season End Only):**
- P1: $100M
- P2: $80M  
- P3: $65M
- P4: $50M
- P5: $40M
- P6: $32M
- P7: $25M
- P8: $20M
- P9: $15M
- P10: $10M

---

**PHASE 7: Staff & Facilities**
Simplified to essential roles that directly impact gameplay.

**Staff (2 key hires):**
1. **Technical Director** (1-5★)
   - Effect: Reduces development time
   - 5★ = upgrades take 50% time
   - Salary: $2-10M/year

2. **Chief Strategist** (1-5★)
   - Effect: Pit stop timing + tire predictions
   - 5★ = optimal strategy calls
   - Salary: $1-5M/year

**Facilities (2 types):**
1. **Factory Level** (Basic/Modern/Advanced)
   - Basic: 1 upgrade at a time
   - Modern: 2 parallel upgrades
   - Advanced: 3 parallel upgrades
   - Upgrade cost: $20M → $50M

2. **Simulator Level** (Basic/Modern/Advanced)
   - Basic: 80% accurate setups
   - Modern: 90% accurate
   - Advanced: 95% accurate
   - Upgrade cost: $10M → $30M

---

**PHASE 8: Save/Load System**
- 3 career save slots
- Auto-save after each race
- Manual save anytime in menus

**Career Data Structure:**
```json
{
  "season": 1,
  "race": 5,
  "team": "McLaren",
  "finances": {
    "balance": 45000000,
    "spent_this_season": 78000000
  },
  "staff": {
    "technical_director": {"name": "James Key", "rating": 4},
    "chief_strategist": {"name": "Andrea Stella", "rating": 4}
  },
  "facilities": {
    "factory": "Modern",
    "simulator": "Basic"
  },
  "upgrades_in_progress": [...],
  "constructor_standings": {...}
}
```

---

**Money Flow Diagram:**
```
Race Performance → Sponsor Bonuses → Team Budget
                                          ↓
                    ┌─────────────────────┴─────────────────┐
                    │                                       │
            Car Development                          Staff Salaries
            ($5-20M/upgrade)                        ($3-15M/year)
                    │                                       │
                    ↓                                       ↓
            Better Performance                      Better Decisions
                    │                                       │
                    └───────────────┬───────────────────────┘
                                    ↓
                            Season End Position
                                    ↓
                            Prize Money Payout
                            ($10-100M based on P1-P10)
```

---

**AI Team Behaviors:**
Each AI team has personality traits:
- **Risk Tolerance**: How close to cost cap they push
- **Development Focus**: Speed vs Reliability priority
- **Staff Priority**: Technical vs Strategy preference
- **Sponsor Realism**: Top teams get premium sponsors

Examples:
- Red Bull: High risk, speed focus, technical priority
- Mercedes: Low risk, balanced focus, strategy priority
- Williams: Low risk, reliability focus, survival mode

---

**Implementation Notes:**
1. Start with financial system (everything needs money)
2. Add save/load early to test persistence
3. Build car development (core progression loop)
4. Layer in staff/facilities
5. Test full season with AI teams
6. Balance and polish

**Expansion Hooks:**
- Development areas stored as config (easy to add more)
- Staff roles list (can add without breaking existing)
- Sponsor types/personalities (same slot system)
- New phases can be added later:
  - Regulations & Politics
  - Young Driver Program
  - Random Events & Drama
  - Media & PR Management

---

**Key Design Principles:**
1. **AI uses same systems** - No fake AI bonuses, they follow same rules
2. **Money drives everything** - Single resource to manage
3. **Every decision has trade-offs** - Spend on drivers or development?
4. **Expansion-friendly** - Core systems can grow without rewrites
5. **Clear feedback** - Player always knows why they succeeded/failed

---

### Backlog Details

#### #1: Phase 1 - Foundation ✅ COMPLETE
**Completed:** 2025-12-24

Implemented features:
- 2025 grid (all 10 teams, correct driver lineups)
- Team tiers (S/A/B/C/D with pace modifiers)
- Car characteristics (balance, cornering, traction)
- Driver attributes (skill, consistency, racecraft, style)
- Driver-car synergy system
- Fuel load system (heavy start → light finish)
- Basic pit stops (AI-triggered, tire swaps)
- Tire degradation with cliff effect

---

#### #2: Phase 2 - Advanced Tire System
**Priority:** HIGH | **Complexity:** MEDIUM | **Est. Sessions:** 3-5

Build on existing tire foundation:
- **Thermal model** - tire temp affects grip (cold = slow, optimal = fast, overheated = degrading)
- **Compound strategies** - soft/medium/hard with distinct windows
- **Wear visualization** - show tire health on timing screen
- **Graining/blistering** - different failure modes per compound
- **Track evolution** - rubber builds up, everyone gets faster

*Note: Basic degradation + cliff already exists in Phase 1*

---

#### #3: Phase 3 - Proximity Racing
**Priority:** HIGH | **Complexity:** LARGE | **Est. Sessions:** 5-8

Car-to-car interactions:
- **Dirty air** - lose downforce when following closely
- **DRS zones** - detection points, 1-second rule, speed boost
- **Slipstream** - draft benefit on straights
- **Alternative lines** - cars can go offline to attack/defend
- **Overtaking mechanics** - success based on delta, racecraft, tire state

---

#### #4: Phase 4 - Drama & Chaos
**Priority:** MEDIUM | **Complexity:** LARGE | **Est. Sessions:** 5-8

Emergent storytelling:
- **Driver errors** - mistakes under pressure, rookie errors
- **Last lap aggression** - drivers take more risks
- **Heat system** - rivalries affect behavior
- **DRS trains** - bunched up cars, hard to escape
- **Safety car** - bunches field, restart drama
- **Mechanical failures** - DNFs based on reliability

---

#### #5: Tire Wear Bar on Timing Screen
**Priority:** LOW | **Complexity:** SMALL | **Est. Sessions:** 1

Visual indicator for tire life:
- Percentage bar next to tire compound on timing screen
- Shows laps remaining until cliff (full bar = fresh, empty = at cliff)
- Bar color matches compound (red = Soft, yellow = Medium, white = Hard)
- Example: `S ████████` (red, fresh) → `S ██░░░░░░` (red, worn)

---

#### #6: Main Menu + Settings System
**Priority:** HIGH | **Complexity:** HIGH | **Est. Sessions:** 8-12

Complete game configuration system:

**Main Menu:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                      F1 MANAGER                             │
│                                                             │
│                   [ QUICK RACE ]                            │
│                                                             │
│                   [ CAREER MODE ]                           │
│                                                             │
│                  [ TRACK SELECTION ]                        │
│                                                             │
│                     [ SETTINGS ]                            │
│                                                             │
│                       [ QUIT ]                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- **Quick Race** — Jump straight into a single race (current behavior)
- **Career Mode** — Full team principal experience (requires #7 to be built)
- **Track Selection** — Pick track for Quick Race (from `tools/tracks/`)
- **Settings** — Configure all game systems
- **Quit** — Exit game

**Settings Structure (nested menus):**
```
SETTINGS
├── Presets
│   └── Load/save/delete custom presets; built-in presets available
├── Teams
│   └── Edit tier, balance, cornering, traction; add/remove teams
├── Drivers
│   └── Edit skill, consistency, racecraft, style; change team (2 per team max); add/remove
├── Race
│   └── Laps, sim speed options
├── Tires
│   └── Deg rates, cliff laps, cliff penalty
├── Fuel
│   └── Start penalty, burn rate
├── Pit Stops
│   └── Base time, variance, strategy thresholds
├── Performance
│   └── Tier modifiers, skill range, synergy bonuses
└── Back
```

---

**Settings Presets:**

Built-in presets for different experiences:

| Preset | Description |
|--------|-------------|
| **Realistic** | 2025 accurate stats, authentic pace gaps, true-to-life tire deg |
| **Balanced** | Tighter field, more competitive midfield, easier overtaking |
| **Chaos** | High variance, fast tire deg, more mechanical failures, drama mode |
| **Random** | Randomizes team tiers, driver skills, shuffles lineups |
| **Custom** | Your own saved configurations |

```
┌─────────────────────────────────────────────────────────────┐
│  PRESETS                                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  BUILT-IN:                                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ○ Realistic    - True to 2025 F1                    │   │
│  │ ○ Balanced     - Tighter, more competitive          │   │
│  │ ○ Chaos        - Maximum drama                      │   │
│  │ ○ Random       - Shuffle everything                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  CUSTOM PRESETS:                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ My Balanced Career    [LOAD] [DELETE]               │   │
│  │ Underdog Challenge    [LOAD] [DELETE]               │   │
│  │ Chaos Mode v2         [LOAD] [DELETE]               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [ SAVE CURRENT AS NEW PRESET ]                             │
│                                                             │
│  [BACK]                                                     │
└─────────────────────────────────────────────────────────────┘
```

Custom presets saved to `presets/` folder as JSON files.

---

**Settings Categories — What's Changeable When:**

| Category | In Quick Race | During Career | Notes |
|----------|---------------|---------------|-------|
| **Tuning (always editable)** ||||
| Race settings | ✅ | ✅ | Laps, sim speed |
| Tire settings | ✅ | ✅ | Deg rates, cliff |
| Fuel settings | ✅ | ✅ | Burn rate, penalty |
| Pit stop settings | ✅ | ✅ | Times, variance |
| Performance modifiers | ✅ | ✅ | Tier bonuses, skill ranges |
| **World State (locked in career)** ||||
| Team roster | ✅ | ❌ | Which teams exist |
| Team stats | ✅ | ❌ | Tier, characteristics |
| Driver lineup | ✅ | ❌ | Who's on which team |
| Driver stats | ✅ | ❌ | Skill, consistency, etc. |

*In Career Mode, world state changes happen through gameplay (contracts, development) not settings.*

---

**Workflow: Test Before You Commit**

1. Pick a preset (or customize from scratch)
2. Run Quick Races to test the feel
3. Tweak settings until happy
4. Save as custom preset (optional)
5. Start Career Mode → settings snapshot saved with career
6. Tuning settings still editable mid-career
7. World state locked — changes happen through gameplay

---

**Key Features:**
- Scrollable lists with clear labels
- Nested navigation (Settings → Teams → Red Bull → edit values)
- 2 drivers per team limit (swap prompt if full)
- Persists to `user_config.json`, loads on game start
- **Presets system** — built-in + custom save slots
- **Living system:** Every new feature adds its configurable values here
- **Career Mode button** — Shows "Coming Soon" until #7 is built, then links to career

**Design Rule:** This is the game's tuning backbone. Test in Quick Race, perfect your balance, then commit to Career.

---

#### #7: Career Mode
**Priority:** HIGH | **Complexity:** MASSIVE | **Est. Sessions:** 20-30+

Full team principal management sim — you're not the only one playing, AI principals fight the same battles.

*(See full 23-phase breakdown below)*

---

#### #8: Smart Track Boundaries (Kerb Fix)
**Priority:** HIGH | **Complexity:** MEDIUM | **Est. Sessions:** 2-3

**The Problem:**
Track boundaries fold over at tight hairpin corners. The current `get_track_boundaries()` uses naive perpendicular offsets from each waypoint. At sharp corners, the inner boundary points cross over each other because perpendicular vectors from adjacent waypoints point in conflicting directions. This causes:
- Kerbs rendering across the racing line at hairpins
- Gravel traps with self-intersecting polygons
- Visual glitches at any corner sharper than ~60°

**The Solution:**
Arc interpolation on inner boundaries at sharp corners. Instead of a single offset point that crosses over, insert multiple points along an arc that follows the corner's natural curve.

**Design Decisions:**
- **Arc interpolation** chosen over miter/bevel because kerbs should look smooth and follow the corner curve (like real F1 kerbs)
- **Fix in `get_track_boundaries()`** rather than separate method — one fix benefits kerbs, gravel traps, and track surface rendering
- **Inner boundary only** needs arc treatment — outer boundary at hairpins has plenty of room and doesn't fold over
- **Configurable corner resolution** — allow tuning how many arc points to insert

**Acceptance Criteria:**
- [ ] Kerbs render correctly at all hairpin corners (no crossing racing line)
- [ ] Gravel traps render without self-intersecting polygons
- [ ] Track surface has no visual glitches at sharp corners
- [ ] Works for any track geometry (imported, hand-drawn, procedural)
- [ ] Performance: boundary calculation still fast (< 1ms for 100 waypoints)
- [ ] Existing tracks look the same or better (no regression on mild corners)

---

#### #9: Qualifying Weekend Mode
**Priority:** HIGH | **Complexity:** LARGE | **Est. Sessions:** 10-15

A complete F1 weekend experience: simulated practice → driver feedback → setup adjustments → full Q1/Q2/Q3 qualifying (player-controlled) → race.

---

**The Core Loop:**
```
Practice (simulated, 5-10 sec) → Practice Summary (driver feedback) → 
Setup Screen (adjust car) → Qualifying (Q1→Q2→Q3, player controls timing) → 
Grid Formation → Race
```

---

**PHASE 1: Practice Session (Simulated)**

Practice is NOT played — it's simulated with a progress bar (5-10 seconds).

**What happens during simulation:**
- Drivers complete 3-5 laps each at varying paces
- Cars test different setups, learn track
- Data generated: lap times, sector performance, tire wear rates

**Skip option:** Yes, with penalty (random setup, no driver feedback)

**New state:** `GAME_STATE_PRACTICE` in main.py

---

**PHASE 2: Practice Summary Screen**

After practice, player sees results and driver feedback.

**Layout:**
```
╔══════════════════════════════════════════════════════════════╗
║  PRACTICE SESSION COMPLETE                    Track: Monaco  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  YOUR TEAM: McLaren                                          ║
║  ┌─────────────────────┐  ┌─────────────────────┐           ║
║  │ NOR - P3            │  │ PIA - P8            │           ║
║  │ Best: 1:23.456      │  │ Best: 1:24.012      │           ║
║  │ Gap to pole: +0.234 │  │ Gap to pole: +0.790 │           ║
║  └─────────────────────┘  └─────────────────────┘           ║
║                                                              ║
║  DRIVER FEEDBACK                                             ║
║  ┌──────────────────────────────────────────────────────┐   ║
║  │ NOR: "Significant understeer in medium-speed corners. │   ║
║  │       Recommend increasing front wing by 1-2 degrees."│   ║
║  │                                                        │   ║
║  │ PIA: "Feels like it's pushing a bit? Maybe we need    │   ║
║  │       more front wing?"                                │   ║
║  └──────────────────────────────────────────────────────┘   ║
║                                                              ║
║  [ADJUST SETUP]              [PROCEED TO QUALIFYING]         ║
╚══════════════════════════════════════════════════════════════╝
```

---

**PHASE 3: Driver Feedback System**

Drivers give radio-style feedback based on their personality.

**Feedback categories:**
- Balance (understeer/oversteer)
- Traction (corner exit grip)
- Braking (stability, locking)
- Cornering (high/low speed)
- Top Speed (aero drag)

**Driver personality affects feedback style:**

| Style | Example (Understeer) |
|-------|---------------------|
| Aggressive | "This thing's understeering like a tractor! Sort the front wing, now!" |
| Smooth | "Significant understeer in medium-speed corners. Recommend +1-2° front wing." |
| Adaptive | "We're losing the front end early. Let's try adjusting the front wing." |
| Rookie | "Feels like it's pushing a bit? Maybe we need more front wing?" |

**Feedback accuracy by experience:**
- Veterans (skill 90+): 85-95% accurate
- Experienced (skill 80-89): 70-85% accurate
- Rookies (skill <75): 50-70% accurate, uses "I think" / "maybe"

---

**PHASE 4: Setup Screen**

Player adjusts car setup based on driver feedback.

**Setup parameters (simplified):**

| Parameter | Range | Effect |
|-----------|-------|--------|
| Front Wing | 0-10° | More = better turn-in, less straight speed |
| Rear Wing | 0-15° | More = better traction, less top speed |
| Brake Bias | 45-65% | Higher = stable braking, less rotation |
| Differential | Open↔Locked | Locked = better traction, less stable |

**Presets:** Low Downforce, High Downforce, Balanced, Qualifying

**Setup impact on lap time:** ±0.3-0.8s per parameter, ±1.5-2.0s total

**UI Layout:**
- Tabbed interface (Driver 1 / Driver 2)
- Current setup vs Recommended changes
- Stat bars showing impact (Speed, Cornering, Traction, Balance)
- Driver feedback shown alongside setup options

---

**PHASE 5: Qualifying (The Main Event)**

**Session Structure (Real F1 Format):**

| Session | Duration | Cars | Eliminated |
|---------|----------|------|------------|
| Q1 | 18 min | 20 | Bottom 5 (P16-P20) |
| Q2 | 15 min | 15 | Bottom 5 (P11-P15) |
| Q3 | 12 min | 10 | None - sets P1-P10 |

**Time compression:** 1 game-second = 3 real-seconds (Q1 ≈ 6 min real time)
**Fast-forward:** 2x/4x available

---

**PHASE 6: Tire Management (6 Sets)**

Player has 6 sets of soft tires for ALL of qualifying (Q1+Q2+Q3).

**Typical allocation:**
- Q1: 2 sets (installation + flying lap)
- Q2: 2 sets
- Q3: 2 sets (final push)

**Strategic decisions:**
- Save tires in Q1 if safe (skip second run)
- Use extra set for "banker lap" mid-session
- Running out forces use of mediums (pace penalty)

**Tire UI:**
```
SOFT TIRES: [🔴] [🔴] [🔴] [🔴] [◯] [◯]
              ↑ current        used  used
```

**Warnings:**
- Orange: "2 tire sets remaining"
- Red flash: "Tire failure risk high"

---

**PHASE 7: Player Controls**

**The core mechanic:** Player decides WHEN to send drivers out.

**Controls:**
- "SEND OUT" button for each driver (when in pits)
- "CALL IN" button (only during out-lap, abort run)
- Both drivers CAN go out simultaneously (enough crew for both)

**Automatic (not player-controlled):**
- Fuel load (always minimal)
- New tires (always fresh set unless player reuses)
- Number of laps per run
- Pit stop execution

---

**PHASE 8: Traffic & Timing**

**What compromises a lap:**
- Dirty air (car within 1.5s ahead): -0.3s penalty
- Blocked (car directly ahead in sector): -0.5s to -1.0s
- Yellow flag on track: lap invalidated

**Player info for timing decisions:**
- Mini-map showing all 20 cars (color-coded by lap type)
- Track status indicator: Clear / Busy / Crowded
- Car status icons: HOT LAP / OUT LAP / IN LAP
- Gap to cars ahead/behind if you send driver out now

**Risk/reward:**
- Early runs: Clean track but less grip (track evolution)
- Late runs: Better grip but traffic risk, weather risk

---

**PHASE 9: Qualifying Timing Tower**

```
Q1 - 12:34 REMAINING              [TRACK: BUSY]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
P1  VER  1:23.456  -         [HOT LAP]  🔴NEW
P2  LEC  1:23.678  +0.222    [IN PIT]   🔴65%
P3  NOR  1:23.890  +0.434    [OUT LAP]  🔴NEW  ← YOU
...
P15 ALO  1:25.123  +1.667    [IN PIT]         ← BUBBLE
P16 OCO  1:25.234  +1.778    [HOT LAP]        ← DANGER
...
```

**Differences from race timing:**
- Sorted by best lap time (not position)
- Shows session time remaining (not laps)
- Status column: OUT LAP / HOT LAP / IN PIT / ELIMINATED
- Bubble positions highlighted (P15/P16 in Q1, P10/P11 in Q2)

---

**PHASE 10: AI Behavior**

| Team Tier | Pattern |
|-----------|---------|
| Top (S/A) | Go out early to set benchmark, final push at end |
| Midfield (B/C) | Wait to see times, mid-session run, desperate final push |
| Backmarkers (D) | Early safe run, hope for improvement |

**AI creates drama via:**
- Sometimes blocking (especially in Q1 chaos)
- Rare spins/crashes → yellow/red flags (5% chance per session)
- Weather gambles (staying out on drys when rain starts)

**AI lap times:**
- First run: 85-90% of potential (banker lap)
- Second run: 95-98% of potential (push lap)
- Occasional mistakes or great laps (variance)

---

**PHASE 11: Weekend State Machine**

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   MENU      │────▶│ TRACK_SELECTION │────▶│   PRACTICE   │
│ (existing)  │     │   (existing)    │     │  (simulated) │
└─────────────┘     └─────────────────┘     └──────┬───────┘
                                                    │
                                                    ▼
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│ PRACTICE    │◀────│   SETUP         │◀────│  PRACTICE    │
│  SUMMARY    │     │   SCREEN        │     │   SUMMARY    │
└──────┬──────┘     └─────────────────┘     └──────────────┘
       │
       ▼
┌──────────────┐     ┌─────────────────┐     ┌──────────────┐
│  QUALIFYING  │────▶│  QUALIFYING     │────▶│     GRID     │
│   (played)   │     │   SUMMARY       │     │  (formation) │
└──────────────┘     └─────────────────┘     └──────┬───────┘
                                                    │
                                                    ▼
                                             ┌──────────────┐
                                             │    RACE      │
                                             │  (existing)  │
                                             └──────────────┘
```

**New game states (add to config.py):**
```python
GAME_STATE_PRACTICE = "practice"
GAME_STATE_PRACTICE_SUMMARY = "practice_summary"
GAME_STATE_SETUP = "setup"
GAME_STATE_QUALIFYING = "qualifying"
GAME_STATE_QUALIFYING_SUMMARY = "qualifying_summary"
GAME_STATE_GRID = "grid"
```

---

**Data That Persists:**

| Data | Where Used |
|------|------------|
| Setup choices | Affects quali & race lap times |
| Tire usage | 6 sets for quali only |
| Grid positions | Race starting order |
| Q2 tire choice | Race starting tire compound (real F1 rule) |

---

**New Files:**

```
race/
├── qualifying_engine.py    # QualifyingEngine class (like RaceEngine but time-based)
├── practice_engine.py      # PracticeEngine class (simulated)
├── car_setup.py            # CarSetup class, setup parameters
├── driver_feedback.py      # Feedback generation based on setup vs optimal

ui/
├── practice_summary.py     # Practice results + feedback display
├── setup_screen.py         # Car setup adjustment UI
├── qualifying_screen.py    # Main qualifying UI (timing tower + controls)
├── grid_screen.py          # Grid formation display

settings/
├── weekend_state.py        # WeekendState class for persistence
```

---

**Acceptance Criteria:**

- [ ] Practice simulates in 5-10 seconds with progress bar
- [ ] Driver feedback reflects car setup issues
- [ ] Feedback style matches driver personality
- [ ] Setup changes affect lap times (±1.5-2.0s range)
- [ ] Q1/Q2/Q3 sessions run with correct durations
- [ ] Bottom 5 eliminated after Q1 and Q2
- [ ] Player can send drivers out at any time
- [ ] Traffic affects lap times realistically
- [ ] 6 tire sets tracked across all sessions
- [ ] Timing tower shows qualifying-specific info
- [ ] Mini-map shows car positions for traffic awareness
- [ ] AI behavior creates realistic qualifying patterns
- [ ] Grid positions carry over to race
- [ ] Weekend state saves/loads correctly
- [ ] Can skip practice (with penalty)
- [ ] Fast-forward works during qualifying

---

**What Makes It Fun:**

1. **Practice → Feedback → Setup** loop gives meaning to practice
2. **Tire scarcity** (6 sets) forces strategic thinking
3. **Timing decisions** (when to send out) = skill-based gameplay
4. **Driver personality** in feedback makes it feel alive
5. **Knockout tension** builds naturally each session
6. **Direct race impact** — your quali result IS your race starting grid

---

**Design Decisions Made:**

- **No crew conflict** — Both drivers can go out simultaneously (enough crew for both)
- **6 soft tire sets** — Creates meaningful resource management without being punishing
- **Simulated practice** — Keeps focus on the interesting parts (feedback, setup, quali)
- **Driver personality in feedback** — Reuses existing driver style data from teams.py
- **Time compression** — 1:3 ratio keeps sessions engaging without dragging
- **Setup simplified to 4 parameters** — Accessible but meaningful

---

#### #10: Dynamic Pit Strategy Manager
**Priority:** HIGH | **Complexity:** MEDIUM | **Est. Sessions:** 2-3

Give players full control over pit stop timing and tire selection:
- **Manual pit calls** - Replace AI automation with player-triggered stops
- **Tire compound selection** - Choose next compound before pit stop
- **Degradation visualization** - Show tire deg graphs to inform decisions
- **Pit window warnings** - Alert when outside optimal window
- **Double stack decisions** - If both cars need stops, choose order

*Implementation:* Replace `should_pit()` AI logic with player command system, add pit strategy UI overlay

---

#### #11: Tire Performance Graph
**Priority:** HIGH | **Complexity:** SMALL | **Est. Sessions:** 1-2

Real-time line graph showing tire degradation curves:
- **Display:** 300x100px below timing tower
- **Shows:** Multiple cars' degradation curves (click to add/remove)
- **Cliff visualization** - Clear indicator of critical degradation point
- **Predicted laps** - Shows laps until cliff based on current rate
- **Compound colors** - Red (soft), yellow (medium), white (hard)

*Implementation:* Car already tracks tire_age and degradation; visualize the calculation

---

#### #12: Race Strategy Timeline
**Priority:** HIGH | **Complexity:** MEDIUM | **Est. Sessions:** 2-3

Horizontal timeline showing full race strategy:
- **Display:** Full width x 100px at bottom of timing screen
- **Shows:** Timeline from lap 1 to total laps with current position
- **Stint bars** - Colored bars showing each car's stint (color = compound)
- **Pit diamonds** - Pit stops marked on timeline
- **Optimal windows** - Highlighted ranges based on tire deg rates

*Implementation:* Aggregate pit_stops and tire history into visual timeline

---

#### #13: Team Radio Commands (Simplified)
**Priority:** MEDIUM | **Complexity:** MEDIUM | **Est. Sessions:** 2-3

Limited but impactful driver commands:
- **Push mode** - +2% pace, +50% tire deg (3 lap maximum)
- **Conserve mode** - -3% pace, -30% tire deg
- **Cooldowns** - Prevent spam, force strategic use
- **Visual feedback** - Mode indicator on timing screen
- **Authentic feel** - Based on real F1 team communications

*Implementation:* Add command queue to Car class, modify pace calculation, add UI buttons

---

#### #14: Pit Window Strategy Overlay
**Priority:** MEDIUM | **Complexity:** SMALL | **Est. Sessions:** 1

Visual indicators for optimal pit windows:
- **Green background** - In optimal window
- **Yellow background** - Possible but not ideal
- **Red background** - Too early/late
- **Updates dynamically** - Based on tire degradation
- **Subtle design** - Doesn't overwhelm timing data

*Implementation:* Calculate optimal windows in race_engine, apply background colors in timing_screen

---

#### #15: Sector Indicators (Refined)
**Priority:** LOW | **Complexity:** SMALL | **Est. Sessions:** 1

Horizontal mini-bars in timing screen:
- **Location:** Between GAP and LAP columns (60x16px)
- **Visual:** 3 segments (S1|S2|S3) with color coding
- **Colors:** Purple (fastest), green (personal best), yellow (current), gray (slower)
- **Animation:** Current sector pulses gently
- **Clean integration** - Fits naturally in timing flow

*Implementation:* Add sector tracking to Car, draw mini-bars in timing_screen

---

#### #16: Race Start Lights (Refined)
**Priority:** LOW | **Complexity:** SMALL | **Est. Sessions:** 1

Authentic F1 5-light start sequence:
- **Position:** Top center of track view
- **Lights:** 5 red circles (60px diameter, 80px spacing)
- **Timing:** 1 light/second, random 0-2s hold, instant out
- **Style:** Clean circles, no effects
- **Text:** "LIGHTS OUT AND AWAY WE GO!" flash

*Implementation:* Add start sequence state to race_engine, draw lights in renderer

---

#### #17: Live Position Mini-Map
**Priority:** LOW | **Complexity:** MEDIUM | **Est. Sessions:** 1-2

Track overview showing all car positions:
- **Display:** 200x200px in top-right of track view
- **Visual:** Simplified track outline
- **Cars:** 4px colored dots using team colors
- **Shows:** Field spread, bunching, gaps
- **Semi-transparent** - Doesn't block main view

*Implementation:* Scale track waypoints to mini size, draw in renderer as overlay

---

## Session History

### 2025-12-22 - Race Simulation Brainstorm
- **Duration:** Extended session
- **Outcome:** Complete 4-phase design saved to backlog
- **Notes:** Very productive session, user engaged with all aspects

### 2025-12-25 - Track Boundary Bug Fix Design
- **Duration:** Short session
- **Outcome:** Smart Track Boundaries (#8) saved to backlog
- **Notes:** User wanted long-term fix for all tracks. Researched Shapely's offset_curve for prior art. Chose arc interpolation over miter/bevel for smoother kerb appearance. User deferred to my recommendation when unsure.

### 2025-12-27 - Qualifying Weekend Mode Design
- **Duration:** Extended session (10+ agents used)
- **Outcome:** Complete qualifying weekend design (#9) saved to backlog
- **Notes:** User requested 10 agents to explore the idea. Covered: practice simulation, driver feedback, setup system, tire allocation, Q1/Q2/Q3 format, traffic mechanics, AI behavior, UI design, state machine. User confirmed: no crew conflict (both drivers can go out), 6 soft tire sets, simulated practice with driver feedback.

### 2025-12-27 - Strategic Features Brainstorm & Refinement
- **Duration:** Extended session (5 evaluation agents + 3 refinement agents)
- **Outcome:** Added 8 refined features (#10-17) to backlog
- **Notes:** User noticed initial brainstorm didn't consider codebase constraints. Re-ran agents with proper context about 2D pygame game. Evaluated 12 features for authenticity, feasibility, and fit. Kept 5, modified 3, removed 4. Final features focus on strategic depth while maintaining "watching races unfold" philosophy.

### 2025-12-27 - Career Mode 23 Phases Deep Dive
- **Duration:** Extended session (23 parallel agents)
- **Outcome:** Explored all 23 phases of Career Mode with detailed ideas
- **Progress:** Completed refining Phases 1-4 (Team Selection, Season Calendar, Driver Management, Contract Negotiations)
- **Key Refinements:** 
  - Phase 1: Removed video pitches and negotiation mini-game, added AI-first design with simple scoring
  - Phase 2: Integrated fatigue with development days, removed regional bonuses
  - Phase 3: Added AI personality types for driver management
  - Phase 4: Added dynamic demands based on performance, "selling the project" system
- **Next Session:** Continue from Phase 5 (Car Development)
- **User Preferences:** Wants AI to be competitive, systems must work for both player and AI, no fake bonuses or penalties

### 2025-12-27 - Career Mode Streamlined to Core Systems
- **Duration:** Extended session (continuation of above)
- **Outcome:** Streamlined 23 phases down to 8 core systems
- **Final Design:** Saved to `.opencode/context/f1-career-mode-design.md`
- **Core Systems:**
  1. Team Selection (already refined)
  2. Season Calendar (already refined)
  3. Driver Management (already refined)
  4. Contract Negotiations (already refined)
  5. Car Development (money-driven upgrades)
  6. Financial System (sponsors + prize money)
  7. Staff & Facilities (2 staff, 2 facilities)
  8. Save/Load System
- **Key Decisions:**
  - Money is the universal resource (no abstract points)
  - Everything interconnects through financial flow
  - Built with expansion hooks for future features
  - AI teams use exact same systems as player
- **Ready for:** Implementation by @f1-director

### 2025-12-28 - Backlog Reality Check & Display Settings
- **Duration:** Short session
- **Outcome:** Updated backlog to reflect actual implementation status from GitHub commits
- **Key Findings:**
  - Phase 1 is fully implemented ✅
  - Main Menu + Settings are fully implemented ✅
  - Track boundaries fixed ✅
  - Career Mode still pending
- **New Feature:** Display Settings & Menu Rename (#18)
  - Rename "Settings" to "Config" for gameplay settings
  - Add new "Settings" for display/video options
  - Fullscreen mode with auto-scaling for 4K displays
- **User Setup:** Has 3840x2160 (4K) display, needs fullscreen support

---

## User Preferences Summary

### What They Like
- Drama and emergent stories
- Simcade feel (deep but accessible)
- Driver skill should matter
- Last lap battles, safety cars, mechanical failures
- Using multiple agents in parallel for complex designs
- AI teams that compete fairly (no fake bonuses)
- Fullscreen gaming experience

### Visual Preferences
- ASCII mockups work well
- Appreciates detailed specifications
- Needs UI scaling for 4K displays

---

## Design Patterns

### What Works
- Start with proposal, refine through conversation
- Ground designs in existing codebase
- Be honest about complexity
- Kick off 10+ agents for complex features
- Check implementation status before assuming
- Quick back-and-forth to clarify intent

---

## Next Steps

### Immediate Priorities:
1. **Display Settings & Menu Rename (#18)** - Quick win for better UX
2. **Career Mode (#7)** - Full design ready, transforms the game
3. **Phase 2: Advanced Tire System (#2)** - Build on existing system

### Future Features:
- Proximity racing (#3)
- Strategic features (#10-17)
- Drama & chaos (#4)