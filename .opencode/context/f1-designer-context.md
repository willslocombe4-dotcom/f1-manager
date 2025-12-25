# F1 Designer Context

**Last Updated:** 2025-12-24

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
| 6 | Main Menu + Settings System | HIGH | HIGH | 2025-12-24 | Pending | — |
| 7 | Career Mode (23 sub-phases) | HIGH | MASSIVE | 2025-12-24 | Pending | **#6** |
| 8 | Smart Track Boundaries (Kerb Fix) | HIGH | MEDIUM | 2025-12-25 | Pending | — |

**Total Ideas:** 8 (1 complete, 7 pending)

---

## Learnings

### User Preferences
<!-- What they like, what they reject, their style -->
- [2025-12-24] **Preference:** User wants agents to learn and improve over time | **Lesson:** Build learning systems into agent workflows

### Conversation Wins
<!-- Approaches that led to good designs -->
- [2025-12-24] **Win:** Ask 1-2 questions per exchange, not 5+ | **Lesson:** Keeps conversation flowing naturally

### Codebase Constraints
<!-- Technical limits that affect design -->
- [2025-12-24] **Constraint:** Settings system uses RuntimeConfig singleton | **Lesson:** New features with config must integrate with it
- [2025-12-24] **Constraint:** UI screens cache values at creation | **Lesson:** Designs must account for cache invalidation

### Design Revisions
<!-- Designs that needed changes, why -->
- [2025-12-24] **Revision:** Track selection initially started race on select | **Lesson:** Confirm UX flow with user before finalizing

---

### ⚠️ Build Order Note
**#6 (Main Menu) MUST be built before #7 (Career Mode)** — Career Mode needs the menu to exist so players can select it.

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

---

**CORE LOOP:**
```
Start at a team → Set season target → Race (10 per season) → 
Manage between races → End season → Prize money/consequences → 
Get offers / Get fired → Next season
```

---

**SEASON STRUCTURE:**
- 10 races per season (configurable)
- Start of season: Set constructor target (e.g., "P5")
- Board holds you to it
- End of season: Prize money based on final position

---

**MANAGEMENT SYSTEMS (All Plates to Spin):**

| System | What You Manage | If Neglected |
|--------|-----------------|--------------|
| **Drivers** | Happiness, contracts, expectations | Complain publicly, leave, sandbag |
| **Board** | Trust, patience, expectations | Pressure, fired |
| **Staff** | Engineers, strategists, morale | Bad upgrades, slow pits, poached |
| **Sponsors** | Demands, exposure, payments | Pull funding, bad press |
| **Finances** | Budget, income, spending | Can't develop, can't sign talent |
| **Car Dev** | Performance, reliability, balance | Slow car, DNFs, angry drivers |
| **Facilities** | Factory, wind tunnel, sim | Slower dev, less accuracy |
| **Media/Rep** | Public perception, fan support | Sponsors leave, hard to attract talent |

**Everything connects:** Bad car → Unhappy drivers → Public complaints → Board angry → Sponsors nervous → Less money → Can't fix car → Spiral

---

**CAR DEVELOPMENT:**
- Sliders for car areas (aero, engine, chassis, etc.)
- Push one area → risk hurting another
- "Safe" slow upgrades vs "Risky" fast ones
- Failed upgrades waste money AND can make things worse

---

**BOARD SYSTEM (Dynamic, not static):**

**Board State = Base Personality + Current Mood + Recent Events**

*Board Types:*
| Type | Cares About | Tolerates |
|------|-------------|-----------|
| Patient Investors | Long-term growth | Bad seasons if trending up |
| Win Now | Immediate results | Nothing |
| Budget Hawks | Financial stability | Slow dev if cheap |
| Legacy Builders | Prestige, reputation | Mediocre results if team looks good |
| Chaotic Owners | Unpredictable | Random mood swings |

*Events that shift board mood:*
- Driver praises/trashes team publicly
- Unexpected results (good or bad)
- Sponsor movements
- Media hype or backlash
- Budget overruns
- New investors / ownership changes

---

**DRIVER PERSONALITIES (Hidden Traits):**
- **Media behavior:** Professional / Honest / Toxic
- **Patience:** Will wait / Demands results now
- **Loyalty:** Sticks with you / Always looking elsewhere

A fast driver who's a media nightmare can tank your board relationship even while scoring points.

---

**AI TEAM PRINCIPALS:**

Real principals with real personalities, playing the same game:

| Team | Principal | Style |
|------|-----------|-------|
| Red Bull | Christian Horner | Political, media savvy, ruthless |
| McLaren | Andrea Stella | Technical, calm, driver-focused |
| Ferrari | Frédéric Vasseur | Steady, handles pressure |
| Mercedes | Toto Wolff | Intense, demanding, hates losing |
| Aston Martin | Mike Krack | Under pressure, Alonso's shadow |
| Alpine | Oliver Oakes | Young, unproven |
| Williams | James Vowles | Strategist, long-term thinker |
| RB | Laurent Mekies | Proving himself |
| Haas | Ayao Komatsu | Engineer first, new to leadership |
| Sauber | Mattia Binotto | Redemption arc, building for Audi |

**They can:**
- Get fired mid-season
- Move teams
- Poach your staff/drivers
- Take jobs you wanted
- You can take their jobs

---

**NEWS/MEDIA TAB:**

Live paddock feed showing AI drama + your own:

```
📰 F1 INSIDER

🔴 BREAKING: Ferrari part ways with Vasseur after P6 finish

💬 Verstappen: "The car is the best it's ever been"

📉 Alpine facing budget crisis - Castrol threatens exit

🔄 RUMOUR: Mercedes eyeing your lead engineer

💰 McLaren announce $50M facility upgrade

😤 Stroll: "We promised podiums. This is P12."

😰 You have been shortlisted for the Mercedes job...
```

Gives intel for poaching + shows consequences of same systems you manage.

---

**JOB MARKET:**
- Perform well → bigger teams come calling
- Perform badly → pressure → sacked
- Get fired → find new job (maybe only backmarkers want you)
- Other teams can approach you mid-career
- Your reputation follows you

---

**IMPLEMENTATION PHASES (Detailed):**

---

### PHASE 7.1: Game State & Career Foundation
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** #6 (Main Menu)

The skeleton that everything else hangs on. Adds game modes and career save structure.

**What Gets Built:**
- **Game Mode Selection** in main menu: "Quick Race" vs "Career Mode"
- **Career save file structure** (`career_save.json`)
  - Current team, season number, race number
  - Player reputation score
  - Historical results
- **New game flow:** Career Start → Pick starting team → Season begins
- **Basic career screen** (placeholder for management, just shows "Race X of 10")

**New Files:**
```
career/
├── __init__.py
├── career_manager.py    # CareerManager class - save/load, state tracking
└── career_state.py      # CareerState dataclass - all career data
```

**Data Structures:**
```python
@dataclass
class CareerState:
    player_name: str
    current_team: str
    season: int
    race_in_season: int          # 1-10
    reputation: int              # 0-100
    career_history: list         # [{season, team, finish_position}]
    
    # Placeholders for later phases:
    budget: int = 0
    board_happiness: int = 50
    driver_happiness: dict = None
    staff: list = None
```

**UI Changes:**
- Main menu gets "Career Mode" button
- New screen: Team Selection (pick from 10 teams to start)
- Career HUD shows: Team name, Season X, Race X/10

**Acceptance Criteria:**
- [ ] Can start new career, pick a team
- [ ] Career state saves to JSON on exit
- [ ] Career state loads on game start
- [ ] Quick Race still works independently
- [ ] Can complete a 10-race "season" (just races, no management yet)

---

### PHASE 7.2: Season Calendar & Race Flow
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.1

Turns the season into a structured calendar with named races and progression.

**What Gets Built:**
- **Race Calendar** - 10 races with names/locations
- **Calendar Screen** - shows upcoming races, results of completed races
- **Pre-race screen** - "Round 5: Monaco Grand Prix" → Start Race
- **Post-race screen** - Results + "Continue to next race" or "Go to Management"
- **Season end detection** - after race 10, trigger end-of-season flow

**Race Calendar (Default):**
```python
SEASON_CALENDAR = [
    {"round": 1, "name": "Bahrain Grand Prix", "track": "bahrain"},
    {"round": 2, "name": "Saudi Arabian Grand Prix", "track": "jeddah"},
    {"round": 3, "name": "Australian Grand Prix", "track": "melbourne"},
    {"round": 4, "name": "Japanese Grand Prix", "track": "suzuka"},
    {"round": 5, "name": "Chinese Grand Prix", "track": "shanghai"},
    {"round": 6, "name": "Miami Grand Prix", "track": "miami"},
    {"round": 7, "name": "Monaco Grand Prix", "track": "monaco"},
    {"round": 8, "name": "Canadian Grand Prix", "track": "montreal"},
    {"round": 9, "name": "British Grand Prix", "track": "silverstone"},
    {"round": 10, "name": "Abu Dhabi Grand Prix", "track": "abudhabi"},
]
```

**New Files:**
```
career/
├── calendar.py          # Season calendar data + logic
ui/
├── calendar_screen.py   # Visual calendar display
├── pre_race_screen.py   # "Round X: [Race Name]" screen
├── post_race_screen.py  # Results + continue options
```

**Flow:**
```
Calendar Screen → Select Race → Pre-Race Screen → Race → 
Post-Race Screen → Calendar Screen (updated) → ... → Season End
```

**Acceptance Criteria:**
- [ ] Calendar shows all 10 races with status (upcoming/completed)
- [ ] Completed races show finishing position
- [ ] Pre-race screen shows race name, round number
- [ ] Post-race screen shows results, points scored
- [ ] After race 10, season marked complete
- [ ] Track selection tied to calendar (uses track from calendar, falls back to default)

---

### PHASE 7.3: Points & Constructor Standings
**Complexity:** SMALL | **Est. Sessions:** 1-2 | **Dependencies:** 7.2

Tracks championship points across the season.

**What Gets Built:**
- **Points system** - F1 points (25-18-15-12-10-8-6-4-2-1)
- **Driver standings** - accumulated points per driver
- **Constructor standings** - accumulated points per team
- **Standings screen** - viewable from calendar, shows both championships
- **Your position tracking** - "You are P4 in constructors"

**Points Table:**
```python
POINTS_SYSTEM = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}
# Positions 11-20 = 0 points
```

**Data Added to CareerState:**
```python
driver_standings: dict    # {"VER": 125, "NOR": 98, ...}
constructor_standings: dict  # {"Red Bull Racing": 200, ...}
```

**New Files:**
```
career/
├── standings.py         # Points calculation, standings logic
ui/
├── standings_screen.py  # Championship tables display
```

**Acceptance Criteria:**
- [ ] Points awarded correctly after each race
- [ ] Driver standings update and sort correctly
- [ ] Constructor standings sum both drivers' points
- [ ] Standings screen accessible from calendar
- [ ] Your team's position highlighted
- [ ] End of season shows final standings

---

### PHASE 7.4: Budget & Prize Money
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.3

Introduces money as a resource. You earn it, you'll spend it later.

**What Gets Built:**
- **Team budget** - starting amount based on team tier
- **Race bonuses** - money for finishing positions
- **Season prize money** - big payout based on final constructor position
- **Budget display** - always visible in career mode
- **Transaction log** - history of income/expenses

**Starting Budgets (by tier):**
```python
STARTING_BUDGETS = {
    "S": 150_000_000,  # $150M - Red Bull, McLaren
    "A": 130_000_000,  # $130M - Ferrari, Mercedes
    "B": 100_000_000,  # $100M - Aston Martin, Williams
    "C": 80_000_000,   # $80M - RB, Alpine, Haas
    "D": 60_000_000,   # $60M - Sauber
}
```

**Race Finish Bonuses:**
```python
RACE_BONUS = {
    1: 2_000_000,   # $2M for a win
    2: 1_500_000,
    3: 1_000_000,
    4: 800_000,
    5: 600_000,
    6: 400_000,
    7: 300_000,
    8: 200_000,
    9: 100_000,
    10: 50_000,
    # 11-20: $0
}
```

**Season Prize Money:**
```python
SEASON_PRIZE = {
    1: 50_000_000,   # $50M for constructor champs
    2: 40_000_000,
    3: 35_000_000,
    4: 30_000_000,
    5: 25_000_000,
    6: 20_000_000,
    7: 15_000_000,
    8: 10_000_000,
    9: 7_000_000,
    10: 5_000_000,
}
```

**Data Added to CareerState:**
```python
budget: int                    # Current money
transactions: list             # [{type, amount, description, race/season}]
```

**UI Changes:**
- Budget shown in career HUD: "$142.5M"
- Post-race shows money earned
- End of season shows prize money breakdown
- Transaction history viewable from management screen

**Acceptance Criteria:**
- [ ] Teams start with tier-appropriate budget
- [ ] Race bonuses awarded based on both drivers' finishes
- [ ] Season prize money awarded at end of season
- [ ] Budget persists across saves
- [ ] Transaction log tracks all income
- [ ] Budget display formatted nicely ($XXM)

---

### PHASE 7.5: Board System - Expectations & Happiness
**Complexity:** LARGE | **Est. Sessions:** 3-4 | **Dependencies:** 7.4

The board watches your performance and judges you.

**What Gets Built:**
- **Season target setting** - at season start, pick your constructor goal (P1-P10)
- **Board happiness meter** - 0-100, starts at 50
- **Board personality types** - each team has a board type
- **Happiness modifiers** - events that raise/lower happiness
- **Pressure warnings** - "The board is losing patience..."
- **Job security status** - Safe / Pressured / Final Warning / Fired

**Board Types (assigned to teams):**
```python
BOARD_TYPES = {
    "Red Bull Racing": "win_now",
    "McLaren": "win_now",
    "Ferrari": "legacy_builders",
    "Mercedes": "win_now",
    "Aston Martin": "patient_investors",
    "Williams": "legacy_builders",
    "RB": "budget_hawks",
    "Alpine": "chaotic_owners",
    "Haas": "budget_hawks",
    "Sauber": "patient_investors",
}
```

**Board Type Behaviors:**
```python
BOARD_BEHAVIORS = {
    "win_now": {
        "target_tolerance": 0,      # Must hit target exactly
        "patience_decay": 10,       # Loses 10 happiness per missed race
        "success_boost": 5,         # Gains 5 per good race
    },
    "patient_investors": {
        "target_tolerance": 2,      # Can miss by 2 positions
        "patience_decay": 3,
        "success_boost": 8,
    },
    "legacy_builders": {
        "target_tolerance": 1,
        "patience_decay": 5,
        "success_boost": 10,        # Love exceeding expectations
    },
    "budget_hawks": {
        "target_tolerance": 1,
        "patience_decay": 5,
        "success_boost": 5,
        "budget_sensitivity": 2.0,  # Extra angry about overspending
    },
    "chaotic_owners": {
        "target_tolerance": "random",  # Changes randomly
        "patience_decay": "random",
        "success_boost": "random",
    },
}
```

**Happiness Events:**
```python
HAPPINESS_EVENTS = {
    # Race results
    "win": +15,
    "podium": +8,
    "points": +3,
    "no_points": -5,
    "double_no_points": -12,
    
    # vs expectations (calculated dynamically)
    "beat_target_position": +10,
    "on_target": +2,
    "below_target_1": -5,
    "below_target_2": -10,
    "below_target_3_plus": -20,
    
    # Other
    "driver_public_praise": +5,
    "driver_public_complaint": -10,
    "sponsor_happy": +3,
    "sponsor_threatens_exit": -15,
    "budget_overrun": -10,
}
```

**Job Security Thresholds:**
```python
JOB_SECURITY = {
    "safe": (60, 100),          # 60-100 happiness
    "pressured": (35, 59),      # 35-59 happiness
    "final_warning": (15, 34),  # 15-34 happiness
    "fired": (0, 14),           # Below 15 = fired
}
```

**Data Added to CareerState:**
```python
season_target: int              # Constructor position target (1-10)
board_happiness: int            # 0-100
board_type: str                 # Personality type
job_security: str               # safe/pressured/final_warning
warnings_received: int          # Count of formal warnings
```

**UI Changes:**
- Season start: Target selection screen
- Career HUD: Board happiness bar + job security indicator
- Post-race: Board reaction message
- Warning popups when happiness drops to new threshold
- Fired screen if happiness hits 0

**Acceptance Criteria:**
- [ ] Can set season target at start
- [ ] Board happiness changes based on results vs target
- [ ] Different board types behave differently
- [ ] Job security status updates correctly
- [ ] Warnings shown when entering new threshold
- [ ] Getting fired ends career at that team (for now, game over)

---

### PHASE 7.6: Management Hub Screen
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.5

Central screen for all between-race management. Placeholder buttons for future systems.

**What Gets Built:**
- **Management Hub** - main between-race screen
- **Navigation** to sub-screens (some placeholder for now)
- **Quick stats panel** - budget, standings, board happiness, next race
- **Time progression** - "Advance to next race" button

**Hub Layout:**
```
┌─────────────────────────────────────────────────────────────┐
│  TEAM MANAGEMENT - [Team Name]           Season 1, Race 5   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   DRIVERS    │  │    STAFF     │  │  DEVELOPMENT │      │
│  │   [2/2]      │  │   [TODO]     │  │    [TODO]    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  FACILITIES  │  │   SPONSORS   │  │    NEWS      │      │
│  │   [TODO]     │  │   [TODO]     │  │   [TODO]     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │  STANDINGS   │  │   CALENDAR   │                        │
│  │   [VIEW]     │  │   [VIEW]     │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Budget: $142.5M  │  Constructors: P4  │  Board: ████░ 72% │
├─────────────────────────────────────────────────────────────┤
│              [ ADVANCE TO NEXT RACE ]                       │
└─────────────────────────────────────────────────────────────┘
```

**New Files:**
```
ui/
├── management_hub.py    # Main hub screen
├── hub_button.py        # Reusable button component for hub
```

**Navigation:**
- DRIVERS → Drivers screen (built in 7.7)
- STAFF → Placeholder "Coming Soon"
- DEVELOPMENT → Placeholder "Coming Soon"
- FACILITIES → Placeholder "Coming Soon"
- SPONSORS → Placeholder "Coming Soon"
- NEWS → Placeholder "Coming Soon"
- STANDINGS → Standings screen (already built)
- CALENDAR → Calendar screen (already built)
- ADVANCE → Goes to pre-race screen for next race

**Acceptance Criteria:**
- [ ] Hub screen displays after each race (via post-race "Continue")
- [ ] All buttons clickable, placeholders show "Coming Soon"
- [ ] Stats panel shows current state accurately
- [ ] Can navigate to standings and calendar
- [ ] "Advance to Next Race" works correctly
- [ ] Hub accessible from calendar screen too

---

### PHASE 7.7: Driver Management - Contracts & Happiness
**Complexity:** LARGE | **Est. Sessions:** 3-4 | **Dependencies:** 7.6

Your drivers have feelings. Keep them happy or face consequences.

**What Gets Built:**
- **Driver contracts** - length, salary, release clause
- **Driver happiness** - 0-100 per driver
- **Driver personality traits** - media behavior, patience, loyalty
- **Happiness modifiers** - car performance, results, promises
- **Driver demands** - occasionally ask for things
- **Contract negotiations** - renew, release, or let expire
- **Driver market** - free agents available to sign

**Driver Personality Traits:**
```python
DRIVER_TRAITS = {
    "VER": {"media": "honest", "patience": 2, "loyalty": 3, "ego": 5},
    "NOR": {"media": "professional", "patience": 4, "loyalty": 4, "ego": 3},
    "HAM": {"media": "professional", "patience": 3, "loyalty": 3, "ego": 4},
    "LEC": {"media": "honest", "patience": 2, "loyalty": 4, "ego": 4},
    # ... etc for all drivers
}

# Media behavior affects public statements
# Patience: how long they wait for car improvements (1=impatient, 5=patient)
# Loyalty: how likely to stay vs seek other options (1=mercenary, 5=loyal)
# Ego: how much they expect to be #1 driver (1=team player, 5=diva)
```

**Contract Structure:**
```python
@dataclass
class DriverContract:
    driver_short: str
    team: str
    salary: int              # Per season
    length: int              # Seasons remaining
    release_clause: int      # Buyout cost
    is_first_driver: bool    # #1 or #2 status
```

**Happiness Events:**
```python
DRIVER_HAPPINESS_EVENTS = {
    "win": +15,
    "podium": +8,
    "points": +3,
    "no_points": -3,
    "mechanical_dnf": -10,
    "teammate_beats_consistently": -5,  # Per race where teammate ahead
    "car_upgrade_success": +5,
    "car_upgrade_fail": -8,
    "promise_kept": +10,
    "promise_broken": -20,
    "contract_renewed": +15,
    "lowball_offer": -10,
}
```

**Consequences of Low Happiness:**
```python
DRIVER_UNHAPPINESS_EFFECTS = {
    (70, 100): None,                    # Happy, no issues
    (50, 69): "occasional_grumbles",    # Minor complaints
    (30, 49): "public_complaints",      # Affects board happiness
    (10, 29): "seeking_exit",           # Actively looking elsewhere
    (0, 9): "refuses_to_race",          # Won't race until resolved
}
```

**New Files:**
```
career/
├── drivers.py           # Driver contracts, happiness, traits
├── driver_market.py     # Free agents, transfers
ui/
├── drivers_screen.py    # View/manage your drivers
├── contract_screen.py   # Negotiate contracts
├── driver_market_screen.py  # Browse available drivers
```

**UI - Drivers Screen:**
```
┌─────────────────────────────────────────────────────────────┐
│  YOUR DRIVERS                                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ #1 MAX VERSTAPPEN                      Happiness: 85 │   │
│  │ Contract: 2 years @ $25M/yr                    ████▓ │   │
│  │ Status: Happy                                        │   │
│  │ [NEGOTIATE]  [RELEASE]                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ #2 LIAM LAWSON                         Happiness: 62 │   │
│  │ Contract: 1 year @ $5M/yr                      ███░░ │   │
│  │ Status: Wants more race wins                         │   │
│  │ [NEGOTIATE]  [RELEASE]                               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [ BROWSE DRIVER MARKET ]                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Acceptance Criteria:**
- [ ] Each driver has contract with salary, length, status
- [ ] Driver happiness tracked and changes based on events
- [ ] Unhappy drivers complain (affects board)
- [ ] Very unhappy drivers seek exit
- [ ] Can negotiate new contracts
- [ ] Can release drivers (pay release clause)
- [ ] Can browse and sign free agents
- [ ] 2 driver per team limit enforced

---

### PHASE 7.8: Car Development System
**Complexity:** LARGE | **Est. Sessions:** 4-5 | **Dependencies:** 7.7

The core of between-race gameplay. Improve your car, but it's risky.

**What Gets Built:**
- **Development areas** - Aero, Engine, Chassis, Reliability
- **Development sliders** - allocate resources to each area
- **Upgrade attempts** - spend money + time, might fail
- **Risk vs reward** - safe upgrades are slow, risky ones can backfire
- **Car performance tracking** - see how your car compares to others
- **Development team quality** - affects success rate (placeholder for staff system)

**Development Areas:**
```python
CAR_DEVELOPMENT_AREAS = {
    "aero": {
        "affects": ["cornering", "top_speed"],
        "base_cost": 5_000_000,
        "base_time": 2,  # races to complete
    },
    "engine": {
        "affects": ["top_speed", "reliability"],
        "base_cost": 8_000_000,
        "base_time": 3,
    },
    "chassis": {
        "affects": ["balance", "traction"],
        "base_cost": 4_000_000,
        "base_time": 2,
    },
    "reliability": {
        "affects": ["reliability"],
        "base_cost": 3_000_000,
        "base_time": 1,
    },
}
```

**Upgrade Types:**
```python
UPGRADE_TYPES = {
    "safe": {
        "success_rate": 0.90,      # 90% success
        "gain_range": (0.5, 1.0),  # +0.5% to +1.0% improvement
        "cost_multiplier": 1.0,
        "time_multiplier": 1.5,    # Takes 50% longer
    },
    "normal": {
        "success_rate": 0.70,
        "gain_range": (1.0, 2.0),
        "cost_multiplier": 1.0,
        "time_multiplier": 1.0,
    },
    "aggressive": {
        "success_rate": 0.50,
        "gain_range": (2.0, 4.0),
        "cost_multiplier": 1.5,    # 50% more expensive
        "time_multiplier": 0.7,    # 30% faster
        "fail_penalty": (-1.0, 0), # Can make car WORSE on failure
    },
}
```

**Development Queue:**
```python
@dataclass
class DevelopmentProject:
    area: str                # aero/engine/chassis/reliability
    upgrade_type: str        # safe/normal/aggressive
    cost: int
    races_remaining: int     # Countdown to completion
    success_chance: float
    potential_gain: float
    potential_loss: float    # If aggressive and fails
```

**Car Performance Model:**
```python
@dataclass
class CarPerformance:
    aero: float              # 0-100, affects cornering
    engine: float            # 0-100, affects top speed
    chassis: float           # 0-100, affects balance/traction
    reliability: float       # 0-100, affects DNF chance
    
    # Derived stats (calculated from above)
    overall_pace: float      # Weighted average
    dnf_chance_per_race: float
```

**New Files:**
```
career/
├── development.py       # Development logic, projects, completion
├── car_performance.py   # Car stats model
ui/
├── development_screen.py  # Development UI with sliders
├── car_stats_screen.py    # View car performance vs field
```

**UI - Development Screen:**
```
┌─────────────────────────────────────────────────────────────┐
│  CAR DEVELOPMENT                          Budget: $142.5M   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  CURRENT PROJECTS:                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [AERO] Normal Upgrade - 1 race remaining            │   │
│  │ Cost: $5M | Success: 70% | Potential: +1.5%         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  START NEW PROJECT:                                         │
│                                                             │
│  Area:    [AERO ▼]  [ENGINE]  [CHASSIS]  [RELIABILITY]     │
│                                                             │
│  Type:    ○ Safe (90%, +0.5-1%, slow)                      │
│           ● Normal (70%, +1-2%)                             │
│           ○ Aggressive (50%, +2-4%, can backfire)          │
│                                                             │
│  Cost: $5,000,000    Time: 2 races                         │
│                                                             │
│  [ START DEVELOPMENT ]                                      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  CAR PERFORMANCE:  Aero: 72  Engine: 68  Chassis: 75       │
│  Overall: 71.7 (P4 in field)   Reliability: 85%            │
└─────────────────────────────────────────────────────────────┘
```

**Integration with Race:**
- Car performance stats feed into existing tier/characteristics system
- Higher aero → better cornering modifier
- Higher engine → better top speed modifier
- Lower reliability → chance of random DNF during race

**Acceptance Criteria:**
- [ ] Can view current car performance stats
- [ ] Can start development projects in any area
- [ ] Projects cost money and take time (races)
- [ ] Projects complete between races with success/fail
- [ ] Failed aggressive upgrades can hurt performance
- [ ] Car stats affect race performance
- [ ] Reliability affects DNF chance
- [ ] Can only run limited projects at once (e.g., 2)

---

### PHASE 7.9: Staff System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.8

Your team behind the scenes. They affect development and pit stops.

**What Gets Built:**
- **Staff roles** - Technical Director, Chief Engineer, Pit Crew Chief
- **Staff stats** - skill level affects their domain
- **Staff happiness** - unhappy staff can leave
- **Staff market** - hire better staff (costs money)
- **Poaching risk** - other teams can steal your staff

**Staff Roles:**
```python
STAFF_ROLES = {
    "technical_director": {
        "affects": ["development_success_rate", "development_speed"],
        "salary_range": (2_000_000, 10_000_000),
    },
    "chief_engineer": {
        "affects": ["development_success_rate", "car_setup"],
        "salary_range": (1_000_000, 5_000_000),
    },
    "pit_crew_chief": {
        "affects": ["pit_stop_time", "pit_stop_variance"],
        "salary_range": (500_000, 2_000_000),
    },
}
```

**Staff Member:**
```python
@dataclass
class StaffMember:
    name: str
    role: str
    skill: int               # 1-100
    salary: int
    contract_length: int     # Seasons
    happiness: int           # 0-100
    loyalty: int             # 1-5, affects poaching resistance
```

**Effects:**
```python
# Technical Director skill affects:
dev_success_modifier = 0.8 + (td_skill / 100) * 0.4  # 0.8x to 1.2x

# Pit Crew Chief skill affects:
pit_time_modifier = 1.2 - (pcc_skill / 100) * 0.4    # 1.2x to 0.8x
```

**New Files:**
```
career/
├── staff.py             # Staff logic, effects
├── staff_market.py      # Available staff to hire
ui/
├── staff_screen.py      # View/manage staff
├── staff_market_screen.py  # Browse and hire
```

**Acceptance Criteria:**
- [ ] Each team has 3 staff roles filled
- [ ] Staff skill affects relevant systems
- [ ] Staff have salaries that cost budget
- [ ] Can hire new staff from market
- [ ] Staff can be poached by other teams (news event)
- [ ] Staff happiness affects performance and retention

---

### PHASE 7.10: Sponsors System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.9

Money comes with strings attached.

**What Gets Built:**
- **Sponsor contracts** - money per season with requirements
- **Sponsor demands** - finish position, exposure, etc.
- **Sponsor happiness** - meet demands or they leave
- **Sponsor market** - attract new sponsors based on performance
- **Title sponsor** - one big sponsor, lots of money, high demands

**Sponsor Types:**
```python
SPONSOR_TIERS = {
    "title": {
        "payment_range": (20_000_000, 50_000_000),
        "demands": "strict",      # Must meet all demands
        "slots": 1,
    },
    "major": {
        "payment_range": (5_000_000, 15_000_000),
        "demands": "moderate",
        "slots": 2,
    },
    "minor": {
        "payment_range": (1_000_000, 4_000_000),
        "demands": "lenient",
        "slots": 3,
    },
}
```

**Sponsor Demands:**
```python
SPONSOR_DEMANDS = {
    "finish_top_5": {"type": "constructor_position", "target": 5},
    "podium_per_season": {"type": "podiums", "target": 1},
    "no_scandals": {"type": "reputation", "min": 50},
    "media_exposure": {"type": "races_shown", "target": 5},  # Placeholder
}
```

**Sponsor Contract:**
```python
@dataclass
class SponsorContract:
    name: str
    tier: str                # title/major/minor
    payment: int             # Per season
    demands: list            # List of demand types
    satisfaction: int        # 0-100
    years_remaining: int
```

**New Files:**
```
career/
├── sponsors.py          # Sponsor logic
├── sponsor_market.py    # Available sponsors
ui/
├── sponsors_screen.py   # View/manage sponsors
```

**Acceptance Criteria:**
- [ ] Teams start with appropriate sponsors for tier
- [ ] Sponsors pay at season start
- [ ] Sponsor satisfaction tracked based on demands
- [ ] Unhappy sponsors can leave (lose income)
- [ ] Can attract new sponsors based on performance
- [ ] Title sponsor is high-risk high-reward

---

### PHASE 7.11: Facilities System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.10

Long-term investments that compound over time.

**What Gets Built:**
- **Facility types** - Factory, Wind Tunnel, Simulator, HQ
- **Facility levels** - 1-5, higher = better bonuses
- **Upgrade costs** - expensive but permanent
- **Facility effects** - boost development, reduce costs, etc.

**Facilities:**
```python
FACILITIES = {
    "factory": {
        "max_level": 5,
        "upgrade_costs": [10_000_000, 20_000_000, 35_000_000, 50_000_000, 75_000_000],
        "effects_per_level": {
            "development_speed": +5,      # % faster per level
            "max_concurrent_projects": 1,  # +1 project slot per 2 levels
        },
    },
    "wind_tunnel": {
        "max_level": 5,
        "upgrade_costs": [8_000_000, 15_000_000, 25_000_000, 40_000_000, 60_000_000],
        "effects_per_level": {
            "aero_development_success": +3,  # % per level
        },
    },
    "simulator": {
        "max_level": 5,
        "upgrade_costs": [5_000_000, 10_000_000, 18_000_000, 30_000_000, 45_000_000],
        "effects_per_level": {
            "driver_consistency_boost": +1,  # Per level
            "setup_accuracy": +5,            # % per level
        },
    },
    "hq": {
        "max_level": 5,
        "upgrade_costs": [15_000_000, 30_000_000, 50_000_000, 80_000_000, 120_000_000],
        "effects_per_level": {
            "staff_happiness": +3,           # Per level
            "sponsor_attraction": +5,        # % per level
        },
    },
}
```

**Team Starting Facilities:**
```python
STARTING_FACILITIES = {
    "Red Bull Racing": {"factory": 5, "wind_tunnel": 5, "simulator": 5, "hq": 4},
    "McLaren": {"factory": 5, "wind_tunnel": 4, "simulator": 5, "hq": 5},
    "Ferrari": {"factory": 5, "wind_tunnel": 5, "simulator": 4, "hq": 5},
    "Mercedes": {"factory": 5, "wind_tunnel": 5, "simulator": 5, "hq": 5},
    "Aston Martin": {"factory": 4, "wind_tunnel": 3, "simulator": 4, "hq": 4},
    "Williams": {"factory": 3, "wind_tunnel": 3, "simulator": 3, "hq": 3},
    "RB": {"factory": 3, "wind_tunnel": 2, "simulator": 3, "hq": 2},
    "Alpine": {"factory": 4, "wind_tunnel": 3, "simulator": 3, "hq": 3},
    "Haas": {"factory": 2, "wind_tunnel": 1, "simulator": 2, "hq": 2},
    "Sauber": {"factory": 3, "wind_tunnel": 2, "simulator": 2, "hq": 3},
}
```

**New Files:**
```
career/
├── facilities.py        # Facility logic, upgrades, effects
ui/
├── facilities_screen.py # View/upgrade facilities
```

**Acceptance Criteria:**
- [ ] Each team has 4 facilities with starting levels
- [ ] Facility levels affect relevant systems
- [ ] Can upgrade facilities (costs money, instant)
- [ ] Upgrades persist across seasons
- [ ] UI shows current levels and upgrade costs

---

### PHASE 7.12: Events System & News Feed
**Complexity:** LARGE | **Est. Sessions:** 3-4 | **Dependencies:** 7.11

The world reacts to what happens. Drama unfolds.

**What Gets Built:**
- **Event types** - race results, driver statements, rumors, transfers, etc.
- **Event triggers** - conditions that spawn events
- **Event effects** - how events affect game state
- **News feed** - scrollable list of recent events
- **Event history** - searchable log of all events

**Event Categories:**
```python
EVENT_CATEGORIES = {
    "race_result": "Results and standings changes",
    "driver_statement": "Driver public comments",
    "transfer_rumor": "Driver/staff movement speculation",
    "transfer_confirmed": "Confirmed moves",
    "sponsor_news": "Sponsor announcements",
    "development": "Car upgrade news",
    "team_internal": "Internal team news",
    "principal_news": "Team principal changes",
    "regulation": "Rule changes (future feature)",
}
```

**Event Templates:**
```python
EVENT_TEMPLATES = {
    "driver_praises_team": {
        "category": "driver_statement",
        "template": "{driver}: \"{team} has given me a fantastic car. We're heading in the right direction.\"",
        "effects": {"board_happiness": +5, "driver_happiness": +3},
        "triggers": ["driver_happiness > 75", "recent_podium"],
    },
    "driver_criticizes_car": {
        "category": "driver_statement",
        "template": "{driver}: \"We need to find more pace. The car isn't where it needs to be.\"",
        "effects": {"board_happiness": -8},
        "triggers": ["driver_happiness < 50", "recent_no_points"],
    },
    "principal_fired": {
        "category": "principal_news",
        "template": "BREAKING: {team} part ways with Team Principal {principal}",
        "effects": {"opens_job": True},
        "triggers": ["ai_principal_happiness < 15"],
    },
    "staff_poached": {
        "category": "transfer_confirmed",
        "template": "{staff_name} leaves {old_team} to join {new_team} as {role}",
        "effects": {"lose_staff": True},
        "triggers": ["staff_happiness < 40", "better_offer_exists"],
    },
    # ... many more
}
```

**News Feed UI:**
```
┌─────────────────────────────────────────────────────────────┐
│  📰 F1 INSIDER                              [Filter ▼]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔴 BREAKING: Ferrari part ways with Frédéric Vasseur      │
│     "Results not matching expectations" - Chairman          │
│     [2 hours ago]                                           │
│                                                             │
│  💬 Max Verstappen: "The car is the best it's ever been"   │
│     [Yesterday]                                             │
│                                                             │
│  📉 Alpine facing budget crisis - Castrol threatens exit   │
│     [Yesterday]                                             │
│                                                             │
│  🔄 RUMOUR: Mercedes eyeing Williams' lead engineer        │
│     [2 days ago]                                            │
│                                                             │
│  💰 McLaren announce $50M factory upgrade                  │
│     [3 days ago]                                            │
│                                                             │
│  😤 Lance Stroll: "We promised podiums. This is P12."      │
│     [3 days ago]                                            │
│                                                             │
│  [Load More...]                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**New Files:**
```
career/
├── events.py            # Event generation, triggers, effects
├── event_templates.py   # All event templates
├── news_feed.py         # News feed management
ui/
├── news_screen.py       # News feed display
```

**Acceptance Criteria:**
- [ ] Events generate based on game state triggers
- [ ] Events have visible effects on game systems
- [ ] News feed shows recent events with timestamps
- [ ] Can filter news by category
- [ ] Events persist in save file
- [ ] AI teams generate events too (not just player)

---

### PHASE 7.13: AI Team Principals
**Complexity:** LARGE | **Est. Sessions:** 4-5 | **Dependencies:** 7.12

The AI plays the same game you do. They can win, fail, and get fired.

**What Gets Built:**
- **AI Principal profiles** - real names, personalities, management styles
- **AI decision making** - development choices, driver management, etc.
- **AI performance tracking** - their board happiness, job security
- **AI job market** - fired principals seek new jobs
- **Principal movement** - AI can change teams, you can take AI jobs

**AI Principal Profiles:**
```python
AI_PRINCIPALS = {
    "christian_horner": {
        "name": "Christian Horner",
        "style": "political",
        "strengths": ["media_handling", "driver_management"],
        "weaknesses": ["budget_control"],
        "aggression": 4,          # 1-5, affects risk-taking
        "loyalty": 3,             # 1-5, how likely to stay
        "current_team": "Red Bull Racing",
    },
    "toto_wolff": {
        "name": "Toto Wolff",
        "style": "intense",
        "strengths": ["development", "staff_retention"],
        "weaknesses": ["patience"],
        "aggression": 5,
        "loyalty": 4,
        "current_team": "Mercedes",
    },
    # ... all 10 principals
}
```

**AI Decision Making:**
```python
class AIPrincipal:
    def decide_development(self):
        # Based on style and car needs
        if self.style == "aggressive":
            return "aggressive_upgrade"
        elif self.car_performance < field_average:
            return "normal_upgrade"
        else:
            return "safe_upgrade"
    
    def handle_unhappy_driver(self, driver):
        if self.style == "driver_focused":
            return "negotiate_better_contract"
        elif driver.skill > 85:
            return "try_to_retain"
        else:
            return "let_them_leave"
```

**AI Board Happiness:**
- AI principals have their own board happiness
- Tracked the same way as player
- When AI happiness < 15, they get fired
- Fired AI principals enter job market

**Job Market:**
```python
@dataclass
class JobOpening:
    team: str
    board_type: str
    budget: int
    car_performance: int
    available_since: int      # Race number
    
@dataclass
class PrincipalInMarket:
    name: str
    reputation: int           # Based on past performance
    asking_salary: int
    preferred_team_tier: str  # Won't take jobs below this
```

**Player Job Offers:**
- If player performing well, other teams approach
- If player gets fired, must find new job
- Can only take jobs where team wants you (reputation check)

**New Files:**
```
career/
├── ai_principals.py     # AI principal logic
├── ai_decisions.py      # AI decision-making
├── job_market.py        # Job openings, applications
ui/
├── job_offers_screen.py # View and respond to offers
├── job_market_screen.py # Browse available positions
```

**Acceptance Criteria:**
- [ ] All 10 teams have AI principals with profiles
- [ ] AI makes development/management decisions
- [ ] AI board happiness tracked, can get fired
- [ ] Fired AI enters job market
- [ ] Player can receive job offers from other teams
- [ ] Fired player must find new job or game over
- [ ] News feed shows AI principal changes

---

### PHASE 7.14: Career Progression & Reputation
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.13

Your legacy builds over time.

**What Gets Built:**
- **Player reputation** - 0-100, affects job offers and negotiations
- **Career history** - all teams managed, results achieved
- **Achievements** - milestones that boost reputation
- **Career stats** - wins, podiums, championships
- **Reputation decay** - out of work = reputation drops

**Reputation Factors:**
```python
REPUTATION_EVENTS = {
    "win_race": +2,
    "win_championship": +15,
    "podium": +1,
    "beat_target": +5,
    "miss_target": -3,
    "get_fired": -20,
    "resign_gracefully": -5,
    "poached_by_bigger_team": +10,
    "turn_around_backmarker": +25,  # Special achievement
}
```

**Achievements:**
```python
ACHIEVEMENTS = {
    "first_win": {"name": "Race Winner", "reputation": +10},
    "first_championship": {"name": "Champion", "reputation": +20},
    "underdog_victory": {"name": "Giant Killer", "reputation": +15},
    "dynasty": {"name": "Dynasty Builder", "reputation": +30},  # 3+ titles
    "rebuilder": {"name": "The Rebuilder", "reputation": +20},  # D-tier to podium
    "survivor": {"name": "Survivor", "reputation": +10},  # 5+ seasons
}
```

**Career Summary Screen:**
```
┌─────────────────────────────────────────────────────────────┐
│  CAREER SUMMARY                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [Your Name]                          Reputation: 72 ████▓░ │
│                                                             │
│  CAREER STATS:                                              │
│  Seasons: 5  │  Wins: 12  │  Podiums: 34  │  Championships: 1│
│                                                             │
│  HISTORY:                                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Season 5: McLaren - P1 (CHAMPION)                   │   │
│  │ Season 4: McLaren - P2                              │   │
│  │ Season 3: McLaren - P3                              │   │
│  │ Season 2: Williams - P5 (Promoted to McLaren)       │   │
│  │ Season 1: Williams - P7                             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ACHIEVEMENTS:                                              │
│  🏆 Champion  │  🥇 Race Winner  │  📈 The Rebuilder       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**New Files:**
```
career/
├── reputation.py        # Reputation tracking
├── achievements.py      # Achievement definitions and tracking
├── career_history.py    # Historical record
ui/
├── career_summary_screen.py  # Career overview
```

**Acceptance Criteria:**
- [ ] Reputation tracked and changes based on events
- [ ] Career history records all seasons
- [ ] Achievements unlock and persist
- [ ] Reputation affects job offers (high rep = better teams interested)
- [ ] Career summary viewable from hub
- [ ] Reputation shown in relevant UIs

---

### PHASE 7.15: Save System & Polish
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.14

Make it all persistent and polished.

**What Gets Built:**
- **Full save system** - all career state to JSON
- **Multiple save slots** - 3 career slots
- **Auto-save** - after each race
- **Save validation** - detect corrupted saves
- **Career deletion** - with confirmation
- **Polish pass** - UI consistency, transitions, feedback

**Save File Structure:**
```python
SAVE_FILE_STRUCTURE = {
    "version": "1.0",
    "timestamp": "2025-12-24T15:30:00",
    "player": {
        "name": str,
        "reputation": int,
        "achievements": list,
        "career_history": list,
    },
    "current_season": {
        "number": int,
        "team": str,
        "race_number": int,
        "target": int,
        "standings": dict,
        "calendar_results": list,
    },
    "team_state": {
        "budget": int,
        "board_happiness": int,
        "drivers": list,
        "staff": list,
        "sponsors": list,
        "facilities": dict,
        "car_performance": dict,
        "development_projects": list,
    },
    "world_state": {
        "all_teams": dict,          # AI team states
        "all_principals": dict,     # AI principal states
        "job_market": list,
        "driver_market": list,
        "news_history": list,
    },
}
```

**Save Slots UI:**
```
┌─────────────────────────────────────────────────────────────┐
│  CAREER MODE                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SLOT 1: [Your Name] @ McLaren                       │   │
│  │ Season 5, Race 7  │  Reputation: 72  │  P2 in WCC   │   │
│  │ Last saved: Dec 24, 2025 3:30 PM                    │   │
│  │ [CONTINUE]  [DELETE]                                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SLOT 2: Empty                                       │   │
│  │ [NEW CAREER]                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SLOT 3: Empty                                       │   │
│  │ [NEW CAREER]                                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [BACK TO MAIN MENU]                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Polish Items:**
- Consistent button styles across all career screens
- Smooth transitions between screens
- Loading indicators for save/load
- Confirmation dialogs for destructive actions
- Keyboard navigation support
- Sound effects (if audio system exists)

**New Files:**
```
career/
├── save_manager.py      # Save/load logic
├── save_validation.py   # Corruption detection
ui/
├── save_slots_screen.py # Save slot selection
├── confirmation_dialog.py  # Reusable confirmation popup
```

**Acceptance Criteria:**
- [ ] Full career state saves to JSON
- [ ] 3 save slots available
- [ ] Auto-save after each race
- [ ] Can load saved career correctly
- [ ] Corrupted saves detected and handled gracefully
- [ ] Can delete career with confirmation
- [ ] UI polish pass complete

---

### PHASE 7.16: Balance & Tuning
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.15

Make it fun, not frustrating.

**What Gets Built:**
- **Difficulty settings** - Easy/Normal/Hard affects AI and economy
- **Economy balance** - ensure money flow feels right
- **AI balance** - AI teams shouldn't dominate or collapse
- **Progression curve** - backmarker to champion should feel achievable
- **Playtesting feedback integration**

**Difficulty Modifiers:**
```python
DIFFICULTY_SETTINGS = {
    "easy": {
        "ai_development_speed": 0.7,
        "budget_multiplier": 1.3,
        "board_patience": 1.5,
        "sponsor_generosity": 1.3,
    },
    "normal": {
        "ai_development_speed": 1.0,
        "budget_multiplier": 1.0,
        "board_patience": 1.0,
        "sponsor_generosity": 1.0,
    },
    "hard": {
        "ai_development_speed": 1.3,
        "budget_multiplier": 0.8,
        "board_patience": 0.7,
        "sponsor_generosity": 0.8,
    },
}
```

**Balance Targets:**
- Backmarker → midfield: 2-3 seasons
- Midfield → podiums: 2-3 seasons
- Podiums → championship: 1-2 seasons
- Total "rags to riches" journey: 5-8 seasons

**Tuning Knobs (in Settings):**
```python
CAREER_SETTINGS = {
    "season_length": [5, 10, 15, 20],      # Races per season
    "budget_difficulty": ["generous", "normal", "tight"],
    "board_patience": ["lenient", "normal", "demanding"],
    "ai_aggression": ["passive", "normal", "aggressive"],
    "random_events": ["few", "normal", "many"],
}
```

**Acceptance Criteria:**
- [ ] Difficulty settings affect gameplay noticeably
- [ ] Economy feels balanced (not too easy/hard to make money)
- [ ] AI teams have realistic performance variance
- [ ] Progression from backmarker to champion is achievable
- [ ] Career settings exposed in Settings menu (#6)
- [ ] Playtest feedback addressed

---

### PHASE 7.17: Engine Supplier Relationships
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.8

Not every team builds their own engine. Customer teams depend on manufacturers.

**What Gets Built:**
- **Engine manufacturers** - Mercedes, Ferrari, Honda/Red Bull, Renault
- **Supplier relationships** - customer teams linked to manufacturers
- **Engine performance** - affects top speed, reliability
- **Supplier priority** - works teams get upgrades first
- **Switching suppliers** - expensive, takes a season to implement

**Engine Manufacturers:**
```python
ENGINE_MANUFACTURERS = {
    "mercedes": {
        "performance": 95,
        "reliability": 92,
        "works_team": "Mercedes",
        "customers": ["McLaren", "Williams", "Aston Martin"],
        "customer_cost": 15_000_000,  # Per season
        "upgrade_delay": 2,           # Races behind works team
    },
    "ferrari": {
        "performance": 93,
        "reliability": 88,
        "works_team": "Ferrari",
        "customers": ["Haas", "Sauber"],
        "customer_cost": 12_000_000,
        "upgrade_delay": 3,
    },
    "honda_rbpt": {
        "performance": 96,
        "reliability": 90,
        "works_team": "Red Bull Racing",
        "customers": ["RB"],
        "customer_cost": 10_000_000,
        "upgrade_delay": 2,
    },
    "renault": {
        "performance": 88,
        "reliability": 85,
        "works_team": "Alpine",
        "customers": [],
        "customer_cost": 8_000_000,
        "upgrade_delay": 0,
    },
}
```

**Supplier Relationship:**
```python
@dataclass
class EngineSupplierRelationship:
    manufacturer: str
    is_works_team: bool
    contract_years: int
    annual_cost: int
    relationship_level: int    # 0-100, affects priority
    upgrade_delay: int         # Races behind works team
```

**Relationship Events:**
```python
ENGINE_RELATIONSHIP_EVENTS = {
    "works_team_priority": "Mercedes give works team new spec engine first",
    "customer_delayed": "Williams receive engine upgrade 2 races late",
    "relationship_improved": "Strong results improve standing with {manufacturer}",
    "supplier_unhappy": "{manufacturer} frustrated with {team}'s poor results",
    "contract_negotiation": "{team} in talks to switch to {new_manufacturer}",
}
```

**Switching Suppliers:**
- Announce switch at end of season
- Takes effect next season
- Costs money (early termination fee)
- New supplier relationship starts at 50
- Car development partially reset (engine-related stats)

**New Files:**
```
career/
├── engines.py           # Engine supplier logic
├── engine_market.py     # Available suppliers, negotiations
ui/
├── engine_screen.py     # View engine stats, relationship
```

**Acceptance Criteria:**
- [ ] Each team has an engine supplier
- [ ] Engine performance affects car top speed
- [ ] Works teams get upgrades before customers
- [ ] Relationship level affects upgrade priority
- [ ] Can negotiate to switch suppliers
- [ ] Switching takes a season and costs money
- [ ] News events for engine-related drama

---

### PHASE 7.18: Driver Academy & Junior Program
**Complexity:** MEDIUM | **Est. Sessions:** 3-4 | **Dependencies:** 7.7

Grow your own talent instead of always buying from the market.

**What Gets Built:**
- **Academy investment** - annual funding level
- **Junior drivers** - prospects developing over 2-3 seasons
- **Junior stats** - potential rating, current skill, development rate
- **Promotion decisions** - when to bring juniors to F1
- **Academy reputation** - attracts better prospects

**Academy System:**
```python
ACADEMY_TIERS = {
    "none": {
        "cost": 0,
        "prospect_quality": 0,
        "development_speed": 0,
    },
    "basic": {
        "cost": 2_000_000,
        "prospect_quality": (60, 75),   # Potential range
        "development_speed": 1.0,
        "slots": 2,
    },
    "established": {
        "cost": 5_000_000,
        "prospect_quality": (70, 85),
        "development_speed": 1.2,
        "slots": 3,
    },
    "elite": {
        "cost": 10_000_000,
        "prospect_quality": (80, 95),
        "development_speed": 1.5,
        "slots": 4,
    },
}
```

**Junior Driver:**
```python
@dataclass
class JuniorDriver:
    name: str
    age: int                    # 16-21 typically
    potential: int              # Hidden, 60-99
    current_skill: int          # Visible, starts low
    development_rate: float     # How fast they improve
    seasons_in_academy: int
    ready_for_f1: bool          # Calculated from skill threshold
    
    # Personality (affects F1 career)
    media_behavior: str
    patience: int
    loyalty: int
```

**Development Mechanics:**
```python
# Each season, junior skill increases
skill_gain = base_gain * academy_tier_speed * random(0.8, 1.2)

# Junior is "ready" when skill >= 70
# But you can promote early (risky) or wait (they might leave)

# Juniors who wait too long get impatient
if seasons_in_academy >= 3 and not promoted:
    loyalty -= 20
    # May leave for rival academy
```

**Promotion Path:**
```
Academy (2-3 years) → Reserve Driver (optional) → Race Seat
```

**Academy Events:**
```python
ACADEMY_EVENTS = {
    "hot_prospect": "{junior} wins F2 championship - ready for F1?",
    "slow_developer": "{junior} struggling to improve - cut losses?",
    "poached": "Ferrari academy approaches {junior} with offer",
    "breakthrough": "{junior} shows sudden improvement in testing",
    "injury": "{junior} sidelined for 6 months after crash",
}
```

**New Files:**
```
career/
├── academy.py           # Academy management
├── junior_drivers.py    # Junior driver logic
ui/
├── academy_screen.py    # View/manage academy
├── junior_detail_screen.py  # Individual junior stats
```

**Acceptance Criteria:**
- [ ] Can invest in academy at different tiers
- [ ] Academy generates junior prospects
- [ ] Juniors develop over multiple seasons
- [ ] Can promote juniors to F1 seat
- [ ] Juniors have hidden potential revealed over time
- [ ] Rival teams can poach promising juniors
- [ ] Academy reputation affects prospect quality

---

### PHASE 7.19: Driver Form & Confidence System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.7

Drivers aren't robots. They have good weekends and bad weekends.

**What Gets Built:**
- **Form rating** - temporary modifier that fluctuates
- **Confidence level** - builds or crashes based on results
- **Hot streaks** - sustained good form
- **Cold spells** - sustained poor form
- **Form visualization** - show form on driver cards

**Form System:**
```python
@dataclass
class DriverForm:
    current_form: float         # 0.9 to 1.1 multiplier
    confidence: int             # 0-100
    streak_type: str            # "hot", "cold", "neutral"
    streak_length: int          # Races in current streak
    
    # Recent results affect form
    last_5_results: list        # [position, position, ...]
```

**Form Calculation:**
```python
def calculate_form(driver):
    # Base form from recent results
    avg_recent = average(driver.last_5_results)
    expected = driver.expected_position  # Based on car + skill
    
    if avg_recent < expected - 2:
        # Overperforming
        form_boost = 0.02 * (expected - avg_recent)
    elif avg_recent > expected + 2:
        # Underperforming
        form_penalty = 0.02 * (avg_recent - expected)
    
    # Confidence affects variance
    if confidence > 80:
        # High confidence = more consistent
        variance_reduction = 0.5
    elif confidence < 30:
        # Low confidence = more mistakes
        mistake_chance += 0.1
    
    return base_form + form_boost - form_penalty
```

**Confidence Events:**
```python
CONFIDENCE_EVENTS = {
    # Positive
    "win": +15,
    "podium": +8,
    "beat_teammate": +3,
    "quali_front_row": +5,
    "overtake_rival": +2,
    
    # Negative
    "crash_own_fault": -20,
    "spun": -10,
    "beaten_by_teammate": -5,
    "quali_disaster": -8,
    "mechanical_dnf": -3,  # Not their fault, small hit
    
    # Streaks
    "hot_streak_3": +10,   # Bonus for 3+ good races
    "cold_streak_3": -15,  # Penalty for 3+ bad races
}
```

**Hot/Cold Streak Effects:**
```python
STREAK_EFFECTS = {
    "hot": {
        "form_bonus": 0.03,           # +3% pace
        "confidence_floor": 60,       # Can't drop below 60
        "media": "positive",          # Good press
        "contract_leverage": +10,     # Wants more money
    },
    "cold": {
        "form_penalty": 0.03,         # -3% pace
        "confidence_ceiling": 50,     # Can't rise above 50
        "media": "negative",          # Bad press
        "seat_pressure": True,        # Other drivers circling
    },
}
```

**Form Visualization:**
```
DRIVER FORM
┌─────────────────────────────────────────┐
│ Max Verstappen          Form: ▲ HOT     │
│ Confidence: 92 ████████████░            │
│ Last 5: 1st, 1st, 2nd, 1st, 3rd         │
│ Streak: 5 races (hot)                   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Lance Stroll            Form: ▼ COLD    │
│ Confidence: 28 ███░░░░░░░░░             │
│ Last 5: 14th, 16th, DNF, 15th, 13th     │
│ Streak: 4 races (cold)                  │
└─────────────────────────────────────────┘
```

**New Files:**
```
career/
├── driver_form.py       # Form and confidence logic
ui/
├── driver_form_widget.py  # Form display component
```

**Acceptance Criteria:**
- [ ] Each driver has form rating that fluctuates
- [ ] Confidence builds/drops based on results
- [ ] Hot streaks provide performance bonus
- [ ] Cold spells cause performance penalty
- [ ] Form affects race simulation
- [ ] Form visible on driver management screens
- [ ] News events reference driver form

---

### PHASE 7.20: Media Pressure & Spotlight System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.12

Big teams live under a microscope. Small teams fly under the radar.

**What Gets Built:**
- **Media attention level** - based on team prestige
- **Spotlight pressure** - affects driver/staff stress
- **Media events** - more frequent for big teams
- **Scrutiny effects** - mistakes amplified, wins expected
- **Underdog bonus** - small teams get praise for overperformance

**Media Attention Levels:**
```python
MEDIA_ATTENTION = {
    "Red Bull Racing": 100,    # Maximum scrutiny
    "Ferrari": 100,
    "Mercedes": 95,
    "McLaren": 85,
    "Aston Martin": 70,
    "Williams": 50,            # Historic name, some attention
    "Alpine": 45,
    "RB": 30,
    "Haas": 25,
    "Sauber": 20,              # Minimal attention
}
```

**Spotlight Effects:**
```python
SPOTLIGHT_EFFECTS = {
    "high_attention": {        # 80-100
        "win_reaction": "expected",       # No bonus praise
        "loss_reaction": "disaster",      # Heavy criticism
        "mistake_amplification": 2.0,     # Mistakes 2x impact
        "sponsor_expectations": "high",
        "driver_stress": +10,
        "staff_stress": +5,
    },
    "medium_attention": {      # 40-79
        "win_reaction": "celebrated",
        "loss_reaction": "disappointing",
        "mistake_amplification": 1.0,
        "sponsor_expectations": "normal",
        "driver_stress": 0,
        "staff_stress": 0,
    },
    "low_attention": {         # 0-39
        "win_reaction": "heroic",         # Underdog story!
        "loss_reaction": "understandable",
        "mistake_amplification": 0.5,     # Mistakes less noticed
        "sponsor_expectations": "low",
        "driver_stress": -5,              # Less pressure
        "staff_stress": -5,
    },
}
```

**Media Event Frequency:**
```python
# High attention teams get more events (good and bad)
events_per_race = base_events * (1 + media_attention / 100)

# Types of media events scale with attention
MEDIA_EVENT_TYPES = {
    "press_conference_drama": {"min_attention": 60},
    "social_media_storm": {"min_attention": 50},
    "tabloid_speculation": {"min_attention": 70},
    "underdog_story": {"max_attention": 40},
    "feel_good_piece": {"max_attention": 50},
}
```

**Underdog Mechanics:**
```python
UNDERDOG_BONUSES = {
    "unexpected_podium": {
        "reputation": +15,        # Big rep boost
        "sponsor_interest": +20,  # Sponsors notice
        "media_attention": +10,   # Temporarily more attention
        "driver_confidence": +20,
        "board_happiness": +15,
    },
    "giant_killing_win": {
        "reputation": +25,
        "sponsor_interest": +40,
        "media_attention": +20,
        "achievement_unlock": "giant_killer",
    },
}
```

**Stress Effects:**
```python
# High stress increases mistake chance
mistake_modifier = 1.0 + (stress / 200)  # Up to 1.5x at max stress

# Stress recovery
stress_recovery_per_race = 5 - (media_attention / 25)
# High attention teams recover slower
```

**New Files:**
```
career/
├── media_pressure.py    # Media attention, spotlight logic
├── stress.py            # Stress tracking for drivers/staff
ui/
├── media_attention_widget.py  # Show attention level
```

**Acceptance Criteria:**
- [ ] Each team has media attention level
- [ ] High attention = more scrutiny, less forgiveness
- [ ] Low attention = underdog bonuses for success
- [ ] Stress affects performance
- [ ] Media events scale with attention
- [ ] News feed reflects spotlight dynamics
- [ ] Underdog victories get special recognition

---

### PHASE 7.21: Regulation Changes & Rule Shakeups
**Complexity:** LARGE | **Est. Sessions:** 3-4 | **Dependencies:** 7.8

Every few seasons, new rules reset the competitive order.

**What Gets Built:**
- **Regulation cycles** - major changes every 3-4 seasons
- **Advance warning** - announced 1-2 seasons early
- **Preparation investment** - split resources between current and future
- **Reset effects** - car performance partially reset
- **Winners and losers** - some teams nail new regs, others don't

**Regulation Types:**
```python
REGULATION_TYPES = {
    "aero_overhaul": {
        "description": "Major aerodynamic rule changes",
        "affects": ["aero"],
        "reset_amount": 0.7,          # 70% of aero progress reset
        "preparation_bonus": 0.3,     # Max 30% head start for prep
        "cost_to_prepare": 30_000_000,
    },
    "engine_formula": {
        "description": "New power unit regulations",
        "affects": ["engine"],
        "reset_amount": 0.8,
        "preparation_bonus": 0.4,
        "cost_to_prepare": 50_000_000,
        "manufacturer_impact": True,  # Engine suppliers affected
    },
    "cost_cap_change": {
        "description": "Budget cap adjustments",
        "affects": ["budget"],
        "budget_change": -10_000_000,  # Or positive
        "preparation_bonus": 0,        # Can't prepare for this
    },
    "ground_effect": {
        "description": "Return of ground effect aerodynamics",
        "affects": ["aero", "chassis"],
        "reset_amount": 0.6,
        "preparation_bonus": 0.35,
        "cost_to_prepare": 40_000_000,
    },
}
```

**Regulation Timeline:**
```python
@dataclass
class UpcomingRegulation:
    type: str
    announcement_season: int    # When announced
    implementation_season: int  # When it takes effect
    preparation_started: bool
    preparation_investment: int
    estimated_readiness: float  # 0-1, how prepared you are
```

**Preparation System:**
```python
# Each race, you can allocate development resources
DEVELOPMENT_ALLOCATION = {
    "current_car": 0.0 to 1.0,    # Focus on this season
    "future_regs": 0.0 to 1.0,    # Focus on upcoming regs
    # Must sum to 1.0
}

# Preparation progress
prep_progress += investment * facility_bonus * staff_skill

# When regs hit, your starting position is:
new_car_base = (old_car * (1 - reset_amount)) + (prep_progress * preparation_bonus)
```

**Regulation Lottery:**
```python
# Some teams "get it right", others don't
# Based on preparation + luck + facilities
def calculate_reg_change_outcome(team):
    base = team.preparation_progress
    
    # Facility bonus (wind tunnel, simulator help understand new regs)
    facility_bonus = (team.wind_tunnel + team.simulator) / 10 * 0.1
    
    # Luck factor (can't fully predict new regs)
    luck = random.gauss(0, 0.15)  # ±15% variance
    
    # Staff quality
    staff_bonus = team.technical_director.skill / 100 * 0.1
    
    return base + facility_bonus + luck + staff_bonus
```

**Historical Examples (for flavor):**
```python
REGULATION_STORIES = {
    "brawn_2009": "Small team nails new regs, wins championship",
    "mercedes_2014": "Manufacturer dominance from engine change",
    "red_bull_2022": "Prepared team capitalizes on ground effect",
    "ferrari_2005": "Failed to adapt, lost competitiveness",
}
```

**UI - Regulation Preparation:**
```
┌─────────────────────────────────────────────────────────────┐
│  UPCOMING REGULATIONS                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ⚠️ MAJOR AERO CHANGES - Season 8 (2 seasons away)         │
│                                                             │
│  Your Preparation: ████████░░░░░░░░░░░░ 42%                │
│  Investment to date: $18M                                   │
│  Estimated starting position: P6 → P4 (if current pace)    │
│                                                             │
│  RESOURCE ALLOCATION:                                       │
│  Current Car: [====60%====]                                 │
│  Future Regs: [===40%===]                                   │
│                                                             │
│  [ INCREASE FUTURE FOCUS ]  [ DECREASE FUTURE FOCUS ]       │
│                                                             │
│  Field Preparation Estimates:                               │
│  Red Bull: ████████████████ 85% (heavy investment)         │
│  Ferrari:  ████████████░░░░ 65%                            │
│  Mercedes: ██████████░░░░░░ 55%                            │
│  You:      ████████░░░░░░░░ 42%                            │
│  ...                                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**News Events:**
```python
REGULATION_NEWS = {
    "announcement": "FIA announces major {type} changes for Season {season}",
    "team_investment": "{team} commits $50M to future regulations program",
    "concern": "{team} principal: 'We're worried about the new rules'",
    "confidence": "{team} confident they've cracked new regulations",
    "post_change_winner": "{team} emerges as early favorite under new rules",
    "post_change_loser": "{team} struggling to adapt - 'We got it wrong'",
}
```

**New Files:**
```
career/
├── regulations.py       # Regulation change logic
├── reg_preparation.py   # Preparation tracking
ui/
├── regulations_screen.py  # View upcoming regs, allocate resources
```

**Acceptance Criteria:**
- [ ] Regulation changes announced 1-2 seasons early
- [ ] Can allocate resources between current car and future regs
- [ ] When regs hit, car performance partially resets
- [ ] Preparation level affects starting position under new regs
- [ ] Some randomness in who "gets it right"
- [ ] AI teams also prepare (or don't)
- [ ] News covers regulation changes and team responses
- [ ] Creates opportunity for underdogs to leap forward

---

### PHASE 7.22: Team Rivalries System
**Complexity:** MEDIUM | **Est. Sessions:** 2-3 | **Dependencies:** 7.12, 7.7

History matters. Some teams and drivers have beef.

**What Gets Built:**
- **Team rivalries** - historic and emergent
- **Driver rivalries** - personal vendettas
- **Rivalry effects** - affects on-track behavior, media drama
- **Rivalry events** - incidents that create/intensify rivalries
- **Rivalry decay** - old rivalries fade over time

**Historic Rivalries:**
```python
HISTORIC_TEAM_RIVALRIES = {
    ("Ferrari", "McLaren"): {
        "intensity": 70,
        "origin": "1990s championship battles",
        "type": "historic",
    },
    ("Red Bull Racing", "Mercedes"): {
        "intensity": 85,
        "origin": "2021 championship battle",
        "type": "recent",
    },
    ("Ferrari", "Red Bull Racing"): {
        "intensity": 60,
        "origin": "2022-2024 battles",
        "type": "recent",
    },
}

HISTORIC_DRIVER_RIVALRIES = {
    ("VER", "HAM"): {
        "intensity": 90,
        "origin": "2021 championship",
        "type": "fierce",
    },
    ("LEC", "VER"): {
        "intensity": 65,
        "origin": "Karting days, 2022 battles",
        "type": "respectful",
    },
    ("ALO", "HAM"): {
        "intensity": 50,
        "origin": "2007 McLaren",
        "type": "cold",
    },
}
```

**Rivalry Intensity Effects:**
```python
RIVALRY_EFFECTS = {
    # On-track behavior
    "racing_aggression": intensity * 0.01,      # More aggressive moves
    "late_braking": intensity * 0.005,          # Brake later against rival
    "defending_intensity": intensity * 0.01,    # Harder defending
    
    # Off-track
    "media_drama_chance": intensity * 0.02,     # More likely to make comments
    "fan_interest": intensity * 0.5,            # More exciting for fans
    "sponsor_interest": intensity * 0.3,        # Sponsors love drama
}
```

**Rivalry Creation Events:**
```python
RIVALRY_TRIGGERS = {
    "on_track_collision": {
        "intensity_gain": 20,
        "news": "{driver1} and {driver2} collide! Tempers flare.",
    },
    "controversial_move": {
        "intensity_gain": 15,
        "news": "{driver1} forces {driver2} off track - stewards investigating",
    },
    "championship_decider": {
        "intensity_gain": 25,
        "news": "Championship battle creates lasting rivalry",
    },
    "public_criticism": {
        "intensity_gain": 10,
        "news": "{driver1} questions {driver2}'s driving standards",
    },
    "poaching_staff": {
        "intensity_gain": 15,
        "team_rivalry": True,
        "news": "{team1} poaches key engineer from {team2}",
    },
    "poaching_driver": {
        "intensity_gain": 20,
        "team_rivalry": True,
        "news": "{team1} signs {driver} from rivals {team2}",
    },
}
```

**Rivalry Decay:**
```python
# Rivalries fade if nothing happens
decay_per_season = 5

# But some never fully die
minimum_intensity = {
    "historic": 20,
    "fierce": 30,
    "respectful": 10,
    "cold": 15,
}
```

**Rivalry Types:**
```python
RIVALRY_TYPES = {
    "fierce": {
        "description": "Intense, personal animosity",
        "media_behavior": "hostile",
        "on_track": "no quarter given",
    },
    "respectful": {
        "description": "Competitive but professional",
        "media_behavior": "complimentary but competitive",
        "on_track": "hard but fair",
    },
    "cold": {
        "description": "Distant, avoid each other",
        "media_behavior": "dismissive",
        "on_track": "minimal interaction",
    },
    "historic": {
        "description": "Institutional rivalry",
        "media_behavior": "references past battles",
        "on_track": "extra motivation",
    },
}
```

**UI - Rivalry View:**
```
┌─────────────────────────────────────────────────────────────┐
│  RIVALRIES                                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TEAM RIVALRIES:                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🔥 Red Bull vs Mercedes         Intensity: 85/100   │   │
│  │    Type: Recent | Origin: 2021 Championship         │   │
│  │    "The wounds from 2021 haven't healed"            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  DRIVER RIVALRIES:                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⚔️ Verstappen vs Hamilton       Intensity: 90/100   │   │
│  │    Type: Fierce | Origin: 2021 Championship         │   │
│  │    Recent: Collision at Turn 1, British GP          │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🤝 Leclerc vs Verstappen        Intensity: 65/100   │   │
│  │    Type: Respectful | Origin: Karting days          │   │
│  │    "Old friends, fierce competitors"                │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**New Files:**
```
career/
├── rivalries.py         # Rivalry tracking, effects
├── rivalry_events.py    # Events that create/affect rivalries
ui/
├── rivalries_screen.py  # View all rivalries
```

**Acceptance Criteria:**
- [ ] Historic rivalries loaded at career start
- [ ] New rivalries can form from incidents
- [ ] Rivalry intensity affects on-track behavior
- [ ] Rivalries generate media drama
- [ ] Rivalries decay over time without incidents
- [ ] Team rivalries and driver rivalries tracked separately
- [ ] News feed covers rivalry moments

---

### PHASE 7.23: Historic Moments & Milestones
**Complexity:** SMALL | **Est. Sessions:** 1-2 | **Dependencies:** 7.12, 7.14

Track when cool things happen and celebrate them.

**What Gets Built:**
- **Milestone tracking** - wins, podiums, championships for all
- **Historic moment detection** - recognize special achievements
- **Celebration events** - special news/visuals for milestones
- **Record tracking** - all-time records in your save
- **Legacy stats** - driver/team career totals

**Milestone Types:**
```python
MILESTONES = {
    # Driver milestones
    "first_win": {"threshold": 1, "type": "wins"},
    "10_wins": {"threshold": 10, "type": "wins"},
    "25_wins": {"threshold": 25, "type": "wins"},
    "50_wins": {"threshold": 50, "type": "wins"},
    "100_wins": {"threshold": 100, "type": "wins"},
    "first_championship": {"threshold": 1, "type": "championships"},
    "multiple_champion": {"threshold": 2, "type": "championships"},
    "legend_status": {"threshold": 5, "type": "championships"},
    "100_podiums": {"threshold": 100, "type": "podiums"},
    "200_races": {"threshold": 200, "type": "race_starts"},
    
    # Team milestones
    "team_first_win": {"threshold": 1, "type": "team_wins"},
    "team_100_wins": {"threshold": 100, "type": "team_wins"},
    "team_first_title": {"threshold": 1, "type": "team_championships"},
    "constructor_dynasty": {"threshold": 3, "type": "consecutive_titles"},
}
```

**Historic Moments:**
```python
HISTORIC_MOMENTS = {
    "rookie_wins": {
        "condition": "driver.rookie and race_position == 1",
        "rarity": "legendary",
        "news": "HISTORIC: {driver} wins on debut! First rookie winner since...",
    },
    "backmarker_podium": {
        "condition": "team.tier == 'D' and race_position <= 3",
        "rarity": "epic",
        "news": "INCREDIBLE: {team} scores shock podium!",
    },
    "last_lap_overtake_for_win": {
        "condition": "won_on_last_lap and was_p2_before",
        "rarity": "epic",
        "news": "DRAMA: {driver} steals victory on final lap!",
    },
    "championship_decider": {
        "condition": "final_race and championship_decided_this_race",
        "rarity": "epic",
        "news": "{driver} clinches championship in dramatic finale!",
    },
    "team_turnaround": {
        "condition": "team.last_season_position >= 8 and current_position <= 3",
        "rarity": "rare",
        "news": "{team} completes remarkable turnaround!",
    },
    "home_hero": {
        "condition": "driver.nationality == race.country and position == 1",
        "rarity": "uncommon",
        "news": "{driver} wins in front of home crowd!",
    },
}
```

**Record Tracking:**
```python
@dataclass
class CareerRecords:
    # Driver records
    most_wins_driver: tuple          # (name, count)
    most_championships_driver: tuple
    most_podiums_driver: tuple
    longest_win_streak: tuple        # (name, count)
    
    # Team records
    most_wins_team: tuple
    most_championships_team: tuple
    most_consecutive_titles: tuple
    
    # Your records
    your_best_season_finish: int
    your_total_wins: int
    your_total_championships: int
```

**Celebration Events:**
```python
CELEBRATION_NEWS = {
    "milestone": {
        "template": "🏆 MILESTONE: {subject} reaches {milestone}!",
        "duration": "headline",  # Stays at top of news
    },
    "historic_moment": {
        "template": "📜 HISTORIC: {description}",
        "duration": "headline",
        "special_graphic": True,
    },
    "record_broken": {
        "template": "📊 RECORD: {subject} breaks {record}!",
        "duration": "headline",
    },
}
```

**UI - Records Screen:**
```
┌─────────────────────────────────────────────────────────────┐
│  RECORDS & MILESTONES                                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ALL-TIME RECORDS (This Save):                              │
│  Most Wins (Driver):        Max Verstappen - 67             │
│  Most Championships:        Max Verstappen - 5              │
│  Most Wins (Team):          Red Bull Racing - 142           │
│  Longest Win Streak:        Max Verstappen - 10 races       │
│                                                             │
│  RECENT MILESTONES:                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 🏆 Lewis Hamilton - 200th Race Start (Season 6)     │   │
│  │ 🏆 Ferrari - 250th Win (Season 5)                   │   │
│  │ 🏆 You - First Championship! (Season 5)             │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  HISTORIC MOMENTS:                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 📜 Season 4: Sauber scores shock podium at Monaco   │   │
│  │ 📜 Season 3: Rookie Antonelli wins on debut!        │   │
│  │ 📜 Season 2: Championship decided on last lap       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**New Files:**
```
career/
├── milestones.py        # Milestone tracking
├── historic_moments.py  # Special moment detection
├── records.py           # Record tracking
ui/
├── records_screen.py    # View records and milestones
```

**Acceptance Criteria:**
- [ ] Driver/team milestones tracked and celebrated
- [ ] Historic moments detected and highlighted
- [ ] Records tracked across career save
- [ ] Special news events for milestones
- [ ] Records screen viewable from hub
- [ ] AI drivers/teams also hit milestones

---

## IMPLEMENTATION GUIDE FOR @f1-director

### ⚠️ CRITICAL RULES

1. **ONE SUB-PHASE AT A TIME** — Never combine phases. Each phase is a complete unit that must be built, tested, and working before starting the next.

2. **FOLLOW SPRINT ORDER** — Sprints must be completed in order (1 → 2 → 3 → 4 → 5). Within a sprint, phases can be done in any order UNLESS they have dependencies.

3. **CHECK DEPENDENCIES** — Before starting any phase, verify its dependencies are complete.

4. **TEST BEFORE NEXT** — User must confirm phase works before moving on.

---

## SPRINT STRUCTURE

### 🏁 SPRINT 1: Core Skeleton (MUST BE FIRST)
*Playable career loop with no management — just racing through a season*

| Order | Phase | Name | Sessions | Depends On |
|-------|-------|------|----------|------------|
| 1 | 7.1 | Game State & Career Foundation | 2-3 | #6 (Menu) |
| 2 | 7.2 | Season Calendar & Race Flow | 2-3 | 7.1 |
| 3 | 7.3 | Points & Constructor Standings | 1-2 | 7.2 |
| 4 | 7.4 | Budget & Prize Money | 2-3 | 7.3 |
| 5 | 7.5 | Board System | 3-4 | 7.4 |
| 6 | 7.6 | Management Hub Screen | 2-3 | 7.5 |

**Sprint 1 Total: ~14-17 sessions**
**Milestone:** Can start career, race 10-race season, earn money, get judged by board

---

### 🏁 SPRINT 2: Management Systems (Parallel OK)
*All the things you manage between races*

| Phase | Name | Sessions | Depends On | Can Parallel With |
|-------|------|----------|------------|-------------------|
| 7.7 | Driver Management | 3-4 | 7.6 | — |
| 7.8 | Car Development System | 4-5 | 7.7 | — |
| 7.9 | Staff System | 2-3 | 7.8 | 7.10, 7.11 |
| 7.10 | Sponsors System | 2-3 | 7.9 | 7.9, 7.11 |
| 7.11 | Facilities System | 2-3 | 7.10 | 7.9, 7.10 |

**Sprint 2 Total: ~14-18 sessions**
**Milestone:** Full between-race management loop

---

### 🏁 SPRINT 3: Living World (Parallel OK)
*Events, news, and AI principals*

| Phase | Name | Sessions | Depends On | Can Parallel With |
|-------|------|----------|------------|-------------------|
| 7.12 | Events System & News Feed | 3-4 | 7.11 | — |
| 7.13 | AI Team Principals | 4-5 | 7.12 | 7.20, 7.22, 7.23 |

**Sprint 3 Total: ~7-9 sessions**
**Milestone:** World feels alive, AI teams have drama too

---

### 🏁 SPRINT 4: Depth & Flavor (Parallel OK)
*All the systems that add richness — can be built in any order*

| Phase | Name | Sessions | Depends On |
|-------|------|----------|------------|
| 7.17 | Engine Supplier Relationships | 2-3 | 7.8 |
| 7.18 | Driver Academy & Junior Program | 3-4 | 7.7 |
| 7.19 | Driver Form & Confidence | 2-3 | 7.7 |
| 7.20 | Media Pressure & Spotlight | 2-3 | 7.12 |
| 7.21 | Regulation Changes | 3-4 | 7.8 |
| 7.22 | Team Rivalries | 2-3 | 7.12 + 7.7 |
| 7.23 | Historic Moments & Milestones | 1-2 | 7.12 + 7.14 |

**Sprint 4 Total: ~16-22 sessions**
**Milestone:** Deep, rich career experience

---

### 🏁 SPRINT 5: Polish & Balance (MUST BE LAST)
*Finishing touches*

| Order | Phase | Name | Sessions | Depends On |
|-------|-------|------|----------|------------|
| 1 | 7.14 | Career Progression & Reputation | 2-3 | 7.13 |
| 2 | 7.15 | Save System & Polish | 2-3 | 7.14 |
| 3 | 7.16 | Balance & Tuning | 2-3 | 7.15 |

**Sprint 5 Total: ~6-9 sessions**
**Milestone:** Complete, polished career mode

---

## DEPENDENCY GRAPH

```
#6 Main Menu (REQUIRED FIRST)
 │
 ▼
7.1 Foundation
 │
 ▼
7.2 Calendar
 │
 ▼
7.3 Points
 │
 ▼
7.4 Budget
 │
 ▼
7.5 Board
 │
 ▼
7.6 Hub ────────────────────────────────────────────────┐
 │                                                       │
 ▼                                                       │
7.7 Drivers ──────┬──────────────────────────────────────┤
 │                │                                      │
 │                ├─► 7.18 Academy                       │
 │                ├─► 7.19 Form                          │
 │                └─► 7.22 Rivalries ◄───────────────────┤
 ▼                                                       │
7.8 Car Dev ──────┬─► 7.17 Engines                       │
 │                └─► 7.21 Regulations                   │
 ▼                                                       │
7.9 Staff                                                │
 │                                                       │
 ▼                                                       │
7.10 Sponsors                                            │
 │                                                       │
 ▼                                                       │
7.11 Facilities                                          │
 │                                                       │
 ▼                                                       │
7.12 Events ──────┬─► 7.20 Media Pressure                │
 │                ├─► 7.22 Rivalries ◄───────────────────┘
 │                └─► 7.23 Milestones ◄──┐
 ▼                                       │
7.13 AI Principals                       │
 │                                       │
 ▼                                       │
7.14 Reputation ─────────────────────────┘
 │
 ▼
7.15 Save/Polish
 │
 ▼
7.16 Balance
```

---

## FULL PHASE TABLE

| Sprint | Phase | Name | Complexity | Sessions | Dependencies |
|--------|-------|------|------------|----------|--------------|
| 1 | 7.1 | Game State & Career Foundation | MEDIUM | 2-3 | #6 |
| 1 | 7.2 | Season Calendar & Race Flow | MEDIUM | 2-3 | 7.1 |
| 1 | 7.3 | Points & Constructor Standings | SMALL | 1-2 | 7.2 |
| 1 | 7.4 | Budget & Prize Money | MEDIUM | 2-3 | 7.3 |
| 1 | 7.5 | Board System | LARGE | 3-4 | 7.4 |
| 1 | 7.6 | Management Hub Screen | MEDIUM | 2-3 | 7.5 |
| 2 | 7.7 | Driver Management | LARGE | 3-4 | 7.6 |
| 2 | 7.8 | Car Development System | LARGE | 4-5 | 7.7 |
| 2 | 7.9 | Staff System | MEDIUM | 2-3 | 7.8 |
| 2 | 7.10 | Sponsors System | MEDIUM | 2-3 | 7.9 |
| 2 | 7.11 | Facilities System | MEDIUM | 2-3 | 7.10 |
| 3 | 7.12 | Events System & News Feed | LARGE | 3-4 | 7.11 |
| 3 | 7.13 | AI Team Principals | LARGE | 4-5 | 7.12 |
| 4 | 7.17 | Engine Supplier Relationships | MEDIUM | 2-3 | 7.8 |
| 4 | 7.18 | Driver Academy & Junior Program | MEDIUM | 3-4 | 7.7 |
| 4 | 7.19 | Driver Form & Confidence | MEDIUM | 2-3 | 7.7 |
| 4 | 7.20 | Media Pressure & Spotlight | MEDIUM | 2-3 | 7.12 |
| 4 | 7.21 | Regulation Changes | LARGE | 3-4 | 7.8 |
| 4 | 7.22 | Team Rivalries | MEDIUM | 2-3 | 7.12 + 7.7 |
| 4 | 7.23 | Historic Moments & Milestones | SMALL | 1-2 | 7.12 + 7.14 |
| 5 | 7.14 | Career Progression & Reputation | MEDIUM | 2-3 | 7.13 |
| 5 | 7.15 | Save System & Polish | MEDIUM | 2-3 | 7.14 |
| 5 | 7.16 | Balance & Tuning | MEDIUM | 2-3 | 7.15 |

**TOTAL: 23 sub-phases across 5 sprints, ~55-75 sessions**

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

**How It Works:**

```python
def get_track_boundaries(self, track_width=35, corner_resolution=3):
    """
    Calculate outer and inner track boundaries with smart corner handling.
    
    At sharp corners (angle change > threshold):
    - Outer boundary: miter with limit (extend lines to meet, cap if too long)
    - Inner boundary: arc interpolation (insert corner_resolution points along arc)
    
    Returns: (outer_points, inner_points)
    Note: inner_points may have MORE points than waypoints at sharp corners
    """
    outer_points = []
    inner_points = []
    
    angle_threshold = math.radians(45)  # Corners sharper than 45° get special handling
    
    for i, (x, y) in enumerate(self.waypoints):
        prev_i = (i - 1) % len(self.waypoints)
        next_i = (i + 1) % len(self.waypoints)
        
        # Calculate angle change at this waypoint
        angle_in = math.atan2(y - self.waypoints[prev_i][1], 
                              x - self.waypoints[prev_i][0])
        angle_out = math.atan2(self.waypoints[next_i][1] - y,
                               self.waypoints[next_i][0] - x)
        angle_change = normalize_angle(angle_out - angle_in)
        
        # Determine turn direction (positive = left turn, negative = right turn)
        is_left_turn = angle_change > 0
        
        # Calculate perpendicular directions
        perp_in = angle_in + math.pi/2
        perp_out = angle_out + math.pi/2
        
        if abs(angle_change) < angle_threshold:
            # Mild corner: standard perpendicular offset (current behavior)
            # Average the two perpendicular directions for smoother result
            avg_perp = (perp_in + perp_out) / 2
            outer_points.append((x + math.cos(avg_perp) * track_width,
                                y + math.sin(avg_perp) * track_width))
            inner_points.append((x - math.cos(avg_perp) * track_width,
                                y - math.sin(avg_perp) * track_width))
        else:
            # Sharp corner: special handling
            
            # OUTER BOUNDARY: Miter join (extend lines until they meet)
            # Calculate intersection of offset lines
            outer_point = calculate_miter_point(...)  # With limit to prevent spikes
            outer_points.append(outer_point)
            
            # INNER BOUNDARY: Arc interpolation
            # Insert multiple points along an arc from perp_in to perp_out
            arc_center = (x, y)  # Corner apex
            arc_radius = track_width
            
            # Generate arc points
            for j in range(corner_resolution + 1):
                t = j / corner_resolution
                arc_angle = lerp_angle(perp_in + math.pi, perp_out + math.pi, t)
                arc_x = x + math.cos(arc_angle) * arc_radius
                arc_y = y + math.sin(arc_angle) * arc_radius
                inner_points.append((arc_x, arc_y))
    
    return outer_points, inner_points
```

**Visual Explanation:**

```
BEFORE (current - folds over):

    Racing Line
        │
   ─────●─────  Waypoint at hairpin
       /│\
      / │ \     Perpendicular offsets
     /  │  \    cross each other
    X───┼───X   ← Inner points CROSSED
        │
    Outer points (fine)


AFTER (arc interpolation):

    Racing Line
        │
   ─────●─────  Waypoint at hairpin
       /│\
      / │ \     
     /  │  \    
    ●   │   ●   ← Outer points (miter join)
        │
      ╭─●─╮     ← Inner points follow ARC
     ╱     ╲       (multiple points inserted)
    ●       ●
```

**Files Changed:**

| File | Change |
|------|--------|
| `race/track.py` | Rewrite `get_track_boundaries()` with corner-aware logic |
| `ui/renderer.py` | Remove hacky cross-product skip in `_draw_kerbs()` — boundaries will be correct |

**Helper Functions Needed:**

```python
def normalize_angle(angle):
    """Normalize angle to [-pi, pi] range"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def lerp_angle(a, b, t):
    """Linearly interpolate between two angles, handling wraparound"""
    diff = normalize_angle(b - a)
    return a + diff * t

def calculate_miter_point(p1, angle1, p2, angle2, max_miter_length):
    """
    Calculate where two offset lines intersect.
    If intersection is too far (> max_miter_length), return bevel point instead.
    """
    # Line intersection math...
    # If miter_length > max_miter_length: return midpoint (bevel)
    pass
```

**Acceptance Criteria:**
- [ ] Kerbs render correctly at all hairpin corners (no crossing racing line)
- [ ] Gravel traps render without self-intersecting polygons
- [ ] Track surface has no visual glitches at sharp corners
- [ ] Works for any track geometry (imported, hand-drawn, procedural)
- [ ] Performance: boundary calculation still fast (< 1ms for 100 waypoints)
- [ ] Existing tracks look the same or better (no regression on mild corners)

**Testing Strategy:**
1. Test with current default track (has several hairpins)
2. Test with a synthetic "stress test" track with 180° hairpins
3. Test with imported tracks from track editor
4. Visual inspection: kerbs should follow corner curves naturally

**Why This Matters:**
This is a foundational fix. Every track created for the game will benefit. Without it, track creators have to avoid tight corners or accept visual glitches. With it, any track geometry "just works."

---

## User Preferences

### What They Like
- Drama and emergent stories
- Simcade feel (deep but accessible)
- Driver skill should matter
- Last lap battles, safety cars, mechanical failures

### Visual Preferences
- ASCII mockups work well
- Appreciates detailed specifications

---

## Design Patterns

### What Works
- Start with proposal, refine through conversation
- Ground designs in existing codebase
- Be honest about complexity

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

---

## Learnings

### Gotchas (Things That Caused Problems)
<!-- Add entries when you encounter non-obvious issues -->
<!-- Format: - [YYYY-MM-DD] **Issue:** Description | **Solution:** How to fix/avoid -->

### Patterns That Work
<!-- Add entries when you find successful approaches -->
<!-- Format: - [YYYY-MM-DD] **Pattern:** Description | **When to use:** Context -->

### Codebase Knowledge
<!-- Add entries when you discover important things about the code -->
<!-- Format: - [YYYY-MM-DD] **Discovery:** What was learned -->
- [2025-12-25] **Discovery:** `get_track_boundaries()` uses naive perpendicular offsets that fail at sharp corners. Inner boundary points cross over when angle change > ~45°. Fix requires arc interpolation on inner boundary at corners.
- [2025-12-25] **Discovery:** `_draw_kerbs()` has a hacky cross-product check to skip kerbs that crossed over — this is a symptom, not a fix. Proper boundary calculation eliminates need for this check.
- [2025-12-25] **Discovery:** Shapely library has `offset_curve()` with join_style options (round/miter/bevel) — same problem, same solutions. We can implement similar logic without the dependency.

### Time Sinks (Avoid These)
<!-- Add entries when something took too long and had a simple fix -->
<!-- Format: - [YYYY-MM-DD] **Problem:** What happened | **Prevention:** How to avoid -->
