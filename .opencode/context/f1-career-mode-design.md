# F1 Manager Career Mode - Core Systems Design

## Status: PENDING IMPLEMENTATION
**This is the design document only. Career Mode is not yet implemented in the game.**

## Overview
8 streamlined phases creating a complete career loop. Each system is simple but built for expansion.

**Priority:** HIGH | **Complexity:** LARGE | **Est. Sessions:** 15-20

**Design Philosophy:**
- AI teams use exact same systems as player (no fake bonuses)
- Money is the universal resource connecting all systems
- Simple core systems with expansion hooks for future features
- Every decision has trade-offs

---

## Phase 1: Team Selection
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

## Phase 2: Season Calendar
- 23 races following real F1 calendar
- Each track has characteristics affecting car performance
- Weather probability per track (Monaco 20% rain, Spa 60% rain)
- Development days between races for upgrades/decisions

---

## Phase 3: Driver Management
Drivers have 5 attributes + morale:
- **Skill** (70-99): Raw pace
- **Consistency** (60-95): Lap time variance  
- **Racecraft** (65-95): Overtaking/defending
- **Style**: Aggressive/Smooth/Adaptive
- **Experience** (0-100): Grows over time
- **Morale** (0-100): Affects all performance (-10% when unhappy)

Chemistry with teammate impacts both drivers' morale.

---

## Phase 4: Contract Negotiations
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

## Phase 5: Car Development
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

## Phase 6: Financial System
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

## Phase 7: Staff & Facilities
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

## Phase 8: Save/Load System
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

## Money Flow Diagram
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

## AI Team Behaviors
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

## Implementation Notes
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

## Key Design Principles
1. **AI uses same systems** - No fake AI bonuses, they follow same rules
2. **Money drives everything** - Single resource to manage
3. **Every decision has trade-offs** - Spend on drivers or development?
4. **Expansion-friendly** - Core systems can grow without rewrites
5. **Clear feedback** - Player always knows why they succeeded/failed

---

## Acceptance Criteria
- [ ] Player can select team and start career
- [ ] Money flows correctly: sponsors → budget → expenses
- [ ] Car upgrades take time and improve performance
- [ ] Staff affects development speed and strategy
- [ ] AI teams develop and compete using same systems
- [ ] Cost cap penalties apply correctly
- [ ] Season ends with prize money distribution
- [ ] Career saves and loads correctly
- [ ] Full 23-race season is playable
- [ ] Clear UI shows all financial/development status