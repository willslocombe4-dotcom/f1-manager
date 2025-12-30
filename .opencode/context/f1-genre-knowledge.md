# F1 Manager Genre Knowledge Base

> Reference material for agents designing, planning, building, and reviewing F1 Manager features.
> Sources: F1 Manager 2024, Motorsport Manager, Grand Prix Manager 1 & 2, iGP Manager, GPRO

---

## Core Gameplay Loops

### The Universal Pattern
```
PRE-RACE (Setup/Prep) -> RACE EXECUTION (Live Decisions) -> POST-RACE (Analysis/Progression)
```

### By Game Type

| Game | Loop | Session Length | Depth |
|------|------|----------------|-------|
| **F1 Manager 2024** | R&D -> Staff -> Practice/Quali/Race -> Season | 2-4 hours/weekend | Maximum |
| **Motorsport Manager** | Design HQ -> Car Dev -> Strategy -> Watch Race -> Upgrade | 20-40 min/race | High |
| **Grand Prix Manager** | Personnel -> Finances -> Testing -> Race -> Analysis | 30-60 min/race | Very High |
| **iGP Manager** | Design HQ -> Dev Car -> Strategy -> Live Race -> Upgrade | 5-15 min/race | Medium |

### What Makes These Loops Satisfying

1. **Short-term**: Race day tension (pit calls, weather, tire strategy)
2. **Medium-term**: Development payoff (upgrades show results after 2-4 races)
3. **Long-term**: Team building (backmarker to champion over multiple seasons)

The "slow burn" of watching investments pay off is the core addictive element.

---

## Standard Features (Table Stakes)

These features are **expected** by players. Missing them feels incomplete.

### Race Day (MUST HAVE)
| Feature | Description | Complexity |
|---------|-------------|------------|
| **Live Timing Tower** | Position, gaps, tire info, lap count | Medium |
| **Tire Strategy** | Compound selection, degradation, pit stops | Medium |
| **Pit Stop Management** | Call drivers in, change tires | Low |
| **Race Simulation** | Cars move based on performance | Medium |
| **Weather Effects** | Dry/Wet conditions affecting grip | High |
| **Safety Car/VSC** | Race neutralization periods | High |

### Driver Management (MUST HAVE)
| Feature | Description | Complexity |
|---------|-------------|------------|
| **Driver Stats** | Pace, consistency, racecraft, wet skill | Low |
| **Contract System** | Sign/release drivers, salary negotiation | Medium |
| **Driver Development** | Stats improve over time | Medium |

### Car Development (EXPECTED)
| Feature | Description | Complexity |
|---------|-------------|------------|
| **Performance Tiers** | Teams have different car capabilities | Low |
| **Car Setup** | Adjust settings for different tracks | Medium |
| **Part Development** | Improve car components over time | High |
| **R&D System** | Research new parts, trade-offs | High |

### Season Structure (EXPECTED)
| Feature | Description | Complexity |
|---------|-------------|------------|
| **Race Calendar** | Multiple races in sequence | Low |
| **Championship Points** | Track standings across season | Low |
| **Multi-Season Career** | Progress over multiple years | Medium |

---

## Advanced Features (Differentiators)

These features make games **stand out** from competitors.

### F1 Manager 2024 Innovations
| Feature | What It Does | Player Reception |
|---------|--------------|------------------|
| **Create-A-Team** | Build custom team from scratch | Highly praised |
| **Mentality System** | Staff/driver happiness affects performance | Mixed (can be punishing) |
| **Affiliate Drivers** | Recruit F2/F3 drivers, develop over years | Very positive |
| **Mechanical Failures** | Parts can fail based on usage | Adds realism |
| **ATR Periods** | Regulated development hours | Strategic depth |

### Motorsport Manager Innovations
| Feature | What It Does | Player Reception |
|---------|--------------|------------------|
| **Personality-Driven Drama** | Driver egos, conflicts, preferences | Highly praised |
| **Multi-Tier Championships** | Start in lower series, promote up | Great progression |
| **Dynamic Weather** | Changes mid-race, core strategic element | Essential |
| **Moddable Everything** | Steam Workshop support | Extended lifespan 9+ years |

### Grand Prix Manager Innovations
| Feature | What It Does | Player Reception |
|---------|--------------|------------------|
| **Espionage** | Steal parts/setups from rivals | Fun but gamey |
| **Team Bankruptcy** | AI teams can go bankrupt | Dramatic but disruptive |
| **40-Season Careers** | Extremely long-term progression | Niche appeal |
| **Supplier Contracts** | Negotiate engine/tire deals | Strategic depth |

---

## UI Patterns

### Timing Tower (Universal Standard)

```
+----+-----+------+------+------+--------+
| P# | DRV | TEAM |  GAP |  INT | TIRE   |
+----+-----+------+------+------+--------+
|  1 | VER | RBR  |  --- |  --- | S  12  | <- Leader (no gap)
|  2 | NOR | MCL  | +2.3 | +2.3 | M   8  | <- Gap + Interval
|  3 | LEC | FER  | +5.1 | +2.8 | S  12  |
|  4 | HAM | MER  | +12.4| +7.3 | H   3  | <- Fresh tires
+----+-----+------+------+------+--------+

Elements:
- P#: Race position
- DRV: 3-letter driver code
- TEAM: Team abbreviation
- GAP: Time behind leader
- INT: Interval to car ahead
- TIRE: Compound + Age (laps)
```

**Color Coding Standards**:
- Position changes: Green (gain), Red (loss), White (none)
- Tire compounds: Red (Soft), Yellow (Medium), White (Hard)
- Status indicators: Purple (fastest lap), Yellow (caution), Green (DRS)

### Strategy Screen Patterns

**Pre-Race Setup**:
- Visual stint planner (tire compound per stint)
- Fuel load slider
- Expected pit windows
- Weather forecast display

**In-Race Adjustments**:
- Quick-access pit call button
- Tire compound selection dropdown
- Push/conserve mode toggle
- Driver instructions (attack/defend)

### Car Development UI

**Component View**:
```
+----------------+
|    [AERO]      |  <- Front Wing
|   +------+     |
|   | CAR  |     |  <- Chassis
|   +------+     |
|    [AERO]      |  <- Rear Wing
+----------------+
  [ENGINE] [SUSP]   <- Powertrain components
```

**Development Screen**:
- Part performance bars (current vs. potential)
- Development time progress
- Resource allocation (engineers, budget)
- Performance impact preview

### Team Management Screens

**Staff Overview**:
- Org chart visualization
- Skill ratings per staff member
- Salary/contract info
- Morale indicators

**Financial Dashboard**:
- Budget breakdown (pie chart)
- Income sources (sponsors, prize money)
- Expenditure categories
- Cost cap tracking (if applicable)

---

## Data Structures (Common Patterns)

### Driver Stats

```python
# Industry Standard Structure
driver = {
    # Core Performance (Always Present)
    "pace": 70-99,           # Raw speed
    "consistency": 1-5,      # Lap-to-lap variance
    "racecraft": 1-5,        # Overtaking/defending
    "experience": 1-10,      # Career progression
    
    # Specialized Skills (Common)
    "wet_weather": 1-5,      # Rain performance
    "tire_management": 1-5,  # Degradation control
    "qualifying": 1-5,       # One-lap pace
    
    # Mental/Physical (Simulation-focused)
    "aggression": 1-5,       # Risk-taking
    "concentration": 1-5,    # Late-race focus
    "adaptability": 1-5,     # Setup flexibility
}
```

### Car Performance

```python
# Simplified Model (Mobile/Casual)
car_simple = {
    "overall_rating": 1-100,
    "top_speed": 1-10,
    "acceleration": 1-10,
    "handling": 1-10,
    "reliability": 1-10,
}

# Component Model (PC/Hardcore)
car_detailed = {
    "engine": {
        "power": 1-10,
        "reliability": 1-10,
        "fuel_efficiency": 1-10
    },
    "aerodynamics": {
        "downforce": 1-10,
        "drag": 1-10,
        "balance": -2 to +2  # Front/rear bias
    },
    "chassis": {
        "weight": 1-10,
        "rigidity": 1-10
    },
    "suspension": {
        "ride_height": 1-10,
        "stiffness": 1-10
    }
}
```

### Team Tiers

```python
# Standard Tier System
tiers = {
    "S": {"teams": ["Red Bull", "Ferrari"], "performance_range": 95-100},
    "A": {"teams": ["Mercedes", "McLaren"], "performance_range": 88-94},
    "B": {"teams": ["Aston Martin", "Alpine"], "performance_range": 80-87},
    "C": {"teams": ["Williams", "RB"], "performance_range": 72-79},
    "D": {"teams": ["Haas", "Sauber"], "performance_range": 65-71},
}
```

---

## Player Expectations

### What Players Love

| Category | Praised Features | Why It Works |
|----------|------------------|--------------|
| **Progression** | Building team over seasons | "Slow burn satisfaction" |
| **Strategy** | Meaningful pit/tire decisions | Feeling clever when it works |
| **Authenticity** | Real teams, accurate details | Immersion in F1 world |
| **Customization** | Create-A-Team, livery editors | Personal investment |
| **Drama** | Close races, championship fights | Emotional engagement |

### What Players Hate

| Category | Common Complaints | How to Avoid |
|----------|-------------------|--------------|
| **Bugs** | Soft-locks, save corruption | Rigorous testing |
| **Tedium** | Races take too long | Speed controls, skip options |
| **Unfairness** | Random failures punishing good play | Telegraphed risks |
| **Complexity** | Overwhelming without tutorials | Progressive disclosure |
| **Shallow AI** | Predictable computer opponents | Varied AI strategies |

### Accessibility Spectrum

| Level | Features | Example Games |
|-------|----------|---------------|
| **Casual** | Auto-strategies, quick races, tutorials | iGP Manager |
| **Standard** | Manual pit calls, setup guidance | Motorsport Manager |
| **Simulation** | Full control, no assists | F1 Manager 2024 |
| **Hardcore** | Financial survival, permadeath | Grand Prix Manager |

**Best Practice**: Offer difficulty/assist sliders so players can choose their depth.

---

## Complexity Reference

### Feature Implementation Estimates

| Feature | Complexity | Dev Time | Dependencies |
|---------|------------|----------|--------------|
| **Timing Tower** | Medium | 2-4 hours | Race state, rendering |
| **Tire Degradation** | Medium | 3-5 hours | Car state, lap tracking |
| **Pit Stops** | Medium | 4-6 hours | Strategy system, animations |
| **Weather System** | High | 8-16 hours | Track state, car physics |
| **Safety Car** | High | 10-20 hours | Race control, car bunching |
| **DRS Zones** | Medium | 4-8 hours | Track data, gap detection |
| **R&D System** | Very High | 20-40 hours | UI, persistence, balance |
| **Contract Negotiation** | High | 15-25 hours | AI, economy, UI |
| **Create-A-Team** | Very High | 40-80 hours | Full customization system |

### Phase Recommendations

**Phase 1 - Foundation** (Your current state):
- Simplified car tiers
- Basic driver stats
- Core race loop
- Timing tower

**Phase 2 - Strategic Depth**:
- Weather (wet/dry)
- Qualifying sessions
- DRS zones
- Expanded driver stats

**Phase 3 - Management Layer**:
- Component-based car development
- Staff management
- Multi-season career
- Financial system

**Phase 4 - Polish & Engagement**:
- Multiplayer leagues
- Livery customization
- Achievement system
- Mod support

---

## Quick Reference Tables

### Tire Compound Characteristics

| Compound | Color | Grip | Durability | Use Case |
|----------|-------|------|------------|----------|
| Soft | Red | High | Low (~15 laps) | Qualifying, short stints |
| Medium | Yellow | Medium | Medium (~25 laps) | Balanced strategy |
| Hard | White | Low | High (~40 laps) | Long stints, hot conditions |
| Intermediate | Green | Rain | Medium | Light rain, drying track |
| Wet | Blue | Rain | High | Heavy rain |

### Typical Pit Stop Times

| Component | Time (seconds) | Notes |
|-----------|----------------|-------|
| Pit entry | 3-5s | Speed limit in pit lane |
| Stationary | 2-4s | Tire change only |
| Pit exit | 3-5s | Back to track |
| **Total** | **8-14s** | Varies by team quality |

### Points Systems

| Position | F1 Points | F1 Sprint | Motorsport Manager |
|----------|-----------|-----------|-------------------|
| 1st | 25 | 8 | 25 |
| 2nd | 18 | 7 | 18 |
| 3rd | 15 | 6 | 15 |
| 4th | 12 | 5 | 12 |
| 5th | 10 | 4 | 10 |
| 6th-10th | 8,6,4,2,1 | 3,2,1,0,0 | 8,6,4,2,1 |
| Fastest Lap | +1 (if P10+) | - | - |

---

## Lessons from Genre History

### What Worked

1. **Multi-year progression** - Building a team from scratch to champion
2. **Meaningful trade-offs** - Short-term vs long-term development
3. **Race day tension** - Real-time decisions with consequences
4. **Moddability** - Community content extends lifespan
5. **Visual feedback** - Seeing decisions play out on track

### What Failed

1. **Excessive complexity** - GPM's cryptic interface drove away players
2. **Punishing randomness** - Unfair failures frustrate more than engage
3. **Tedious management** - Between-race tasks must feel purposeful
4. **Unbalanced economy** - Too easy or too hard to manage finances
5. **Shallow AI** - Predictable opponents reduce replayability

### Golden Rule

> "Realism must serve fun, not replace it."

Strategic realism (engine dominance, budget constraints) works.
Punishing realism (random bankruptcies, injuries) frustrates.

---

## Sources

- **F1 Manager 2024**: Frontier Developments, Steam Reviews (79th percentile), Reddit r/F1Manager
- **Motorsport Manager**: Playsport Games, Steam (90% positive, 5033 reviews), Metacritic (81/100)
- **Grand Prix Manager 1 & 2**: MicroProse (1995-1996), Retrospective reviews, GPM2World modding community
- **iGP Manager**: Browser game, community forums
- **GPRO**: Online racing manager, player documentation
