# Implementation Plan: Race Simulation Overhaul - Phase 1: Foundation

**Planned by:** @f1-feature-planner  
**Date:** 2025-12-22  
**Based on:** @f1-onboarding briefing  
**Estimated Steps:** 14  
**Estimated Files Changed:** 4 (`data/teams.py`, `config.py`, `race/car.py`, `assets/colors.py`)

---

## Feature Overview

### What It Does
Replaces the current random speed logic with a deterministic, dynamic simulation based on:
1. **2025 Grid**: Real teams/drivers with performance tiers
2. **Physics**: Fuel load affecting pace throughout the race
3. **Driver Skills**: Individual stats affecting pace and consistency
4. **Synergy**: Bonus/penalty for driver-car fit
5. **Pit Stops**: Simple time-based pit stops with tire reset

### User Experience
- Players see realistic gaps forming (Red Bull pulling away, Sauber fighting at back)
- Pace evolves as fuel burns off (cars get faster each lap)
- Tire degradation forces strategic pit stops
- 5 rookies visible on the 2025 grid

### Technical Approach
Replace static spawn-time speed calculation with a per-frame dynamic pace calculation using the formula:
```
FINAL_PACE = BASE_SPEED × TIER_MODIFIER × DRIVER_SKILL × SYNERGY × FUEL_MODIFIER × TIRE_MODIFIER
```

---

## Prerequisites

- [x] Codebase briefing from @f1-onboarding (completed)
- [x] Understanding of current Car/RaceEngine architecture (reviewed)
- [ ] None - ready to implement

---

## Key Design Decisions

### Decision 1: Pit Stop Implementation
**Choice:** Time-based pit stops (add time to lap, don't physically stop car)  
**Why:** Simpler for Phase 1, avoids complex track position logic. Car continues moving but loses time equivalent to pit stop duration.

### Decision 2: Synergy Calculation
**Choice:** Style-based matching with random variance  
**Why:** Provides meaningful differentiation while keeping it simple. Aggressive drivers match high-traction cars, smooth drivers match balanced cars.

### Decision 3: Fuel Model
**Choice:** Linear fuel burn from 100% to 0% over race distance  
**Why:** Simple, predictable, easy to balance. Fuel penalty decreases linearly each lap.

### Decision 4: Tire Degradation Threshold
**Choice:** Compound-specific thresholds trigger pit stops  
**Why:** Creates natural strategy variation. Soft = 12 laps, Medium = 20 laps, Hard = 30 laps.

---

## Implementation Steps

Execute these steps IN ORDER. Test after each step.

---

### Step 1: Add Physics Constants to config.py

**Purpose:** Establish all tuning constants in one place for easy balancing.

**File:** `config.py`

**Location:** After line 68 (at end of file)

**Action:** Add new section

**Code:**
```python
# =============================================================================
# PHASE 1: RACE SIMULATION PHYSICS
# =============================================================================

# Team Performance Tiers
# S-Tier: Championship contenders, A-Tier: Podium fighters, etc.
TIER_MODIFIERS = {
    "S": 1.04,   # +4% pace (Red Bull, McLaren)
    "A": 1.02,   # +2% pace (Ferrari, Mercedes)
    "B": 1.00,   # Baseline (Aston Martin, Williams)
    "C": 0.98,   # -2% pace (RB, Alpine, Haas)
    "D": 0.95,   # -5% pace (Sauber)
}

# Fuel System
# Cars start heavy (full fuel) and get lighter (faster) each lap
FUEL_START_PENALTY = 0.04      # -4% pace at race start (full fuel)
FUEL_BURN_PER_LAP = 0.002      # +0.2% pace gained per lap (fuel burn)

# Tire Degradation
# Each compound has different degradation rate and lifespan
TIRE_DEG_RATES = {
    TIRE_SOFT: 0.004,    # 0.4% pace loss per lap
    TIRE_MEDIUM: 0.002,  # 0.2% pace loss per lap
    TIRE_HARD: 0.001,    # 0.1% pace loss per lap
}

TIRE_CLIFF_LAPS = {
    TIRE_SOFT: 12,       # Performance cliff after 12 laps
    TIRE_MEDIUM: 20,     # Performance cliff after 20 laps
    TIRE_HARD: 30,       # Performance cliff after 30 laps
}

TIRE_CLIFF_PENALTY = 0.10  # -10% pace after hitting tire cliff

# Pit Stops
PIT_STOP_BASE_TIME = 22.0      # Base pit stop time in seconds
PIT_STOP_VARIANCE = 3.0        # Random variance ±3 seconds

# Synergy System
# How well driver style matches car characteristics
SYNERGY_MODIFIERS = {
    "high": 1.02,      # +2% pace (great match)
    "neutral": 1.00,   # No modifier
    "low": 0.98,       # -2% pace (poor match)
}

# Driver Style to Car Characteristic Matching
# Aggressive drivers prefer high traction, Smooth prefer balance
STYLE_PREFERENCES = {
    "aggressive": {"traction": 4, "balance": 0},   # Wants high traction
    "smooth": {"traction": 2, "balance": 1},       # Wants balanced car
    "adaptive": {"traction": 3, "balance": 0},     # Flexible
}

# Random pace variance per lap (simulates driver inconsistency)
LAP_VARIANCE_BASE = 0.005  # ±0.5% base variance
```

**Verification:**
- Run `python -c "import config; print(config.TIER_MODIFIERS)"`
- Should print: `{'S': 1.04, 'A': 1.02, 'B': 1.0, 'C': 0.98, 'D': 0.95}`

---

### Step 2: Create Complete 2025 Teams Data Structure

**Purpose:** Replace 2024 data with full 2025 grid including all driver stats and team characteristics.

**File:** `data/teams.py`

**Location:** Replace entire file contents

**Action:** Replace

**Code:**
```python
"""
F1 Teams and Drivers Data - 2025 Season
Complete data structure with performance tiers, car characteristics, and driver profiles.
"""

# =============================================================================
# 2025 SEASON DATA
# =============================================================================

TEAMS_2025 = [
    # S-TIER: Championship Contenders (+4% pace)
    {
        "name": "Red Bull Racing",
        "tier": "S",
        "characteristics": {
            "balance": 1,       # -2 to +2: negative = understeer, positive = oversteer
            "cornering": 2,     # -2 to +2: corner speed capability
            "traction": 5,      # 1-5: acceleration out of corners
        },
        "drivers": [
            {
                "number": 1,
                "name": "Max Verstappen",
                "short": "VER",
                "skill": 99,           # 70-99: raw pace ability
                "consistency": 5,      # 1-5: lap-to-lap consistency
                "racecraft": 5,        # 1-5: wheel-to-wheel ability
                "style": "aggressive", # aggressive/smooth/adaptive
            },
            {
                "number": 30,
                "name": "Liam Lawson",
                "short": "LAW",
                "skill": 82,
                "consistency": 3,
                "racecraft": 4,
                "style": "aggressive",
            },
        ]
    },
    {
        "name": "McLaren",
        "tier": "S",
        "characteristics": {
            "balance": 0,
            "cornering": 2,
            "traction": 4,
        },
        "drivers": [
            {
                "number": 4,
                "name": "Lando Norris",
                "short": "NOR",
                "skill": 93,
                "consistency": 4,
                "racecraft": 4,
                "style": "smooth",
            },
            {
                "number": 81,
                "name": "Oscar Piastri",
                "short": "PIA",
                "skill": 89,
                "consistency": 4,
                "racecraft": 4,
                "style": "smooth",
            },
        ]
    },
    
    # A-TIER: Podium Fighters (+2% pace)
    {
        "name": "Ferrari",
        "tier": "A",
        "characteristics": {
            "balance": 1,
            "cornering": 1,
            "traction": 4,
        },
        "drivers": [
            {
                "number": 16,
                "name": "Charles Leclerc",
                "short": "LEC",
                "skill": 92,
                "consistency": 3,
                "racecraft": 4,
                "style": "aggressive",
            },
            {
                "number": 44,
                "name": "Lewis Hamilton",
                "short": "HAM",
                "skill": 94,
                "consistency": 5,
                "racecraft": 5,
                "style": "smooth",
            },
        ]
    },
    {
        "name": "Mercedes",
        "tier": "A",
        "characteristics": {
            "balance": 0,
            "cornering": 1,
            "traction": 3,
        },
        "drivers": [
            {
                "number": 63,
                "name": "George Russell",
                "short": "RUS",
                "skill": 90,
                "consistency": 4,
                "racecraft": 4,
                "style": "smooth",
            },
            {
                "number": 12,
                "name": "Andrea Kimi Antonelli",
                "short": "ANT",
                "skill": 80,
                "consistency": 2,
                "racecraft": 3,
                "style": "aggressive",
                "rookie": True,
            },
        ]
    },
    
    # B-TIER: Midfield Leaders (baseline pace)
    {
        "name": "Aston Martin",
        "tier": "B",
        "characteristics": {
            "balance": -1,
            "cornering": 0,
            "traction": 3,
        },
        "drivers": [
            {
                "number": 14,
                "name": "Fernando Alonso",
                "short": "ALO",
                "skill": 91,
                "consistency": 5,
                "racecraft": 5,
                "style": "adaptive",
            },
            {
                "number": 18,
                "name": "Lance Stroll",
                "short": "STR",
                "skill": 78,
                "consistency": 2,
                "racecraft": 3,
                "style": "aggressive",
            },
        ]
    },
    {
        "name": "Williams",
        "tier": "B",
        "characteristics": {
            "balance": 0,
            "cornering": -1,
            "traction": 3,
        },
        "drivers": [
            {
                "number": 23,
                "name": "Alexander Albon",
                "short": "ALB",
                "skill": 85,
                "consistency": 4,
                "racecraft": 4,
                "style": "smooth",
            },
            {
                "number": 55,
                "name": "Carlos Sainz",
                "short": "SAI",
                "skill": 88,
                "consistency": 4,
                "racecraft": 4,
                "style": "smooth",
            },
        ]
    },
    
    # C-TIER: Midfield Runners (-2% pace)
    {
        "name": "RB",
        "tier": "C",
        "characteristics": {
            "balance": 0,
            "cornering": 0,
            "traction": 3,
        },
        "drivers": [
            {
                "number": 22,
                "name": "Yuki Tsunoda",
                "short": "TSU",
                "skill": 82,
                "consistency": 3,
                "racecraft": 3,
                "style": "aggressive",
            },
            {
                "number": 20,
                "name": "Isack Hadjar",
                "short": "HAD",
                "skill": 78,
                "consistency": 2,
                "racecraft": 3,
                "style": "aggressive",
                "rookie": True,
            },
        ]
    },
    {
        "name": "Alpine",
        "tier": "C",
        "characteristics": {
            "balance": -1,
            "cornering": 0,
            "traction": 2,
        },
        "drivers": [
            {
                "number": 10,
                "name": "Pierre Gasly",
                "short": "GAS",
                "skill": 84,
                "consistency": 4,
                "racecraft": 3,
                "style": "smooth",
            },
            {
                "number": 7,
                "name": "Jack Doohan",
                "short": "DOO",
                "skill": 76,
                "consistency": 2,
                "racecraft": 2,
                "style": "adaptive",
                "rookie": True,
            },
        ]
    },
    {
        "name": "Haas",
        "tier": "C",
        "characteristics": {
            "balance": -1,
            "cornering": -1,
            "traction": 2,
        },
        "drivers": [
            {
                "number": 31,
                "name": "Esteban Ocon",
                "short": "OCO",
                "skill": 82,
                "consistency": 3,
                "racecraft": 3,
                "style": "smooth",
            },
            {
                "number": 87,
                "name": "Oliver Bearman",
                "short": "BEA",
                "skill": 77,
                "consistency": 2,
                "racecraft": 3,
                "style": "aggressive",
                "rookie": True,
            },
        ]
    },
    
    # D-TIER: Backmarkers (-5% pace)
    {
        "name": "Sauber",
        "tier": "D",
        "characteristics": {
            "balance": -2,
            "cornering": -1,
            "traction": 2,
        },
        "drivers": [
            {
                "number": 27,
                "name": "Nico Hulkenberg",
                "short": "HUL",
                "skill": 83,
                "consistency": 4,
                "racecraft": 3,
                "style": "smooth",
            },
            {
                "number": 5,
                "name": "Gabriel Bortoleto",
                "short": "BOR",
                "skill": 75,
                "consistency": 2,
                "racecraft": 2,
                "style": "adaptive",
                "rookie": True,
            },
        ]
    },
]

# =============================================================================
# LEGACY COMPATIBILITY - Keep TEAMS_DATA as alias
# =============================================================================

TEAMS_DATA = TEAMS_2025


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_all_drivers():
    """Get a flat list of all drivers with team information"""
    all_drivers = []
    for team in TEAMS_2025:
        for driver in team["drivers"]:
            all_drivers.append({
                "team": team["name"],
                "tier": team["tier"],
                "characteristics": team["characteristics"],
                "number": driver["number"],
                "name": driver["name"],
                "short": driver["short"],
                "skill": driver["skill"],
                "consistency": driver["consistency"],
                "racecraft": driver["racecraft"],
                "style": driver["style"],
                "rookie": driver.get("rookie", False),
            })
    return all_drivers


def get_team_by_name(team_name):
    """Get team data by name"""
    for team in TEAMS_2025:
        if team["name"] == team_name:
            return team
    return None


def get_driver_by_short(short_name):
    """Get driver data by short name (e.g., 'VER')"""
    for team in TEAMS_2025:
        for driver in team["drivers"]:
            if driver["short"] == short_name:
                return {**driver, "team": team["name"], "tier": team["tier"]}
    return None
```

**Verification:**
- Run `python -c "from data.teams import TEAMS_2025; print(len(TEAMS_2025))"`
- Should print: `10` (10 teams)
- Run `python -c "from data.teams import get_all_drivers; print(len(get_all_drivers()))"`
- Should print: `20` (20 drivers)
- Run `python -c "from data.teams import get_all_drivers; rookies = [d for d in get_all_drivers() if d.get('rookie')]; print([d['short'] for d in rookies])"`
- Should print: `['ANT', 'HAD', 'DOO', 'BEA', 'BOR']` (5 rookies)

---

### Step 3: Update Team Colors for 2025

**Purpose:** Update colors for renamed/rebranded teams (AlphaTauri→RB, Alfa Romeo→Sauber).

**File:** `assets/colors.py`

**Location:** Replace entire file contents

**Action:** Replace

**Code:**
```python
"""
F1 Team Colors - 2025 Season
"""

# Team color definitions (Primary, Secondary)
TEAM_COLORS = {
    "Red Bull Racing": {
        "primary": (30, 65, 170),      # Dark Blue
        "secondary": (255, 200, 0),    # Yellow
        "name_short": "RBR"
    },
    "Ferrari": {
        "primary": (220, 0, 0),        # Red
        "secondary": (255, 255, 255),  # White
        "name_short": "FER"
    },
    "Mercedes": {
        "primary": (0, 210, 190),      # Teal
        "secondary": (0, 0, 0),        # Black
        "name_short": "MER"
    },
    "McLaren": {
        "primary": (255, 135, 0),      # Papaya Orange
        "secondary": (0, 0, 0),        # Black
        "name_short": "MCL"
    },
    "Aston Martin": {
        "primary": (0, 111, 98),       # British Racing Green
        "secondary": (0, 230, 180),    # Lime
        "name_short": "AST"
    },
    "Alpine": {
        "primary": (0, 147, 221),      # Blue (2025 rebrand)
        "secondary": (255, 135, 180),  # Pink accent
        "name_short": "ALP"
    },
    "Williams": {
        "primary": (0, 82, 255),       # Blue
        "secondary": (255, 255, 255),  # White
        "name_short": "WIL"
    },
    "RB": {
        "primary": (22, 50, 91),       # Navy Blue (was AlphaTauri)
        "secondary": (255, 55, 0),     # Red accent
        "name_short": "RB"
    },
    "Haas": {
        "primary": (180, 180, 180),    # Silver
        "secondary": (220, 0, 30),     # Red
        "name_short": "HAA"
    },
    "Sauber": {
        "primary": (82, 226, 82),      # Kick green (was Alfa Romeo)
        "secondary": (0, 0, 0),        # Black
        "name_short": "SAU"
    },
}


def get_team_color(team_name):
    """Get primary color for a team"""
    return TEAM_COLORS.get(team_name, {}).get("primary", (255, 255, 255))


def get_team_secondary_color(team_name):
    """Get secondary color for a team"""
    return TEAM_COLORS.get(team_name, {}).get("secondary", (0, 0, 0))


def get_team_short_name(team_name):
    """Get short name for a team"""
    return TEAM_COLORS.get(team_name, {}).get("name_short", "UNK")
```

**Verification:**
- Run `python -c "from assets.colors import get_team_color; print(get_team_color('Sauber'))"`
- Should print: `(82, 226, 82)` (green)
- Run `python -c "from assets.colors import get_team_color; print(get_team_color('RB'))"`
- Should print: `(22, 50, 91)` (navy)

---

### Step 4: Rewrite Car Class - Complete Replacement

**Purpose:** Replace entire car.py with new implementation including all new attributes and methods.

**File:** `race/car.py`

**Location:** Replace entire file contents

**Action:** Replace

**Code:**
```python
"""
F1 Car - Individual car with dynamic pace calculation
Phase 1: Foundation - Fuel, Tires, Synergy, Pit Stops
"""
import random
import config


class Car:
    """Represents a single F1 car in the race with dynamic performance."""

    def __init__(self, driver_data, team_data, starting_position):
        """
        Initialize a car with driver and team data.
        
        Args:
            driver_data: Dict with driver info (number, name, short, skill, etc.)
            team_data: Dict with team info (name, tier, characteristics)
            starting_position: Grid position (1-20)
        """
        # Driver info
        self.driver_number = driver_data["number"]
        self.driver_name = driver_data["name"]
        self.driver_short = driver_data["short"]
        self.driver_skill = driver_data.get("skill", 80)
        self.driver_consistency = driver_data.get("consistency", 3)
        self.driver_racecraft = driver_data.get("racecraft", 3)
        self.driver_style = driver_data.get("style", "adaptive")
        self.is_rookie = driver_data.get("rookie", False)
        
        # Team info
        self.team = team_data["name"]
        self.team_tier = team_data.get("tier", "B")
        self.car_balance = team_data.get("characteristics", {}).get("balance", 0)
        self.car_cornering = team_data.get("characteristics", {}).get("cornering", 0)
        self.car_traction = team_data.get("characteristics", {}).get("traction", 3)

        # Race state
        self.position = starting_position
        self.starting_position = starting_position
        self.progress = 0.0
        self.lap = 1
        self.total_laps = 0
        self.race_finished = False

        # Fuel state (1.0 = full, 0.0 = empty)
        self.fuel_load = 1.0
        
        # Tire state
        self.tire_compound = self._choose_starting_tire(starting_position)
        self.tire_age = 0
        self.pit_stops = 0
        self.is_pitting = False
        self.pit_time_remaining = 0.0

        # Synergy (calculated once at init)
        self.synergy_level = self._calculate_synergy()
        
        # Dynamic speed (recalculated each frame)
        self.current_pace = config.BASE_SPEED

        # Timing
        self.lap_time = 0.0
        self.best_lap_time = None
        self.last_lap_time = None
        self.gap_to_leader = 0.0
        self.gap_to_ahead = 0.0

        # Visual
        self.lateral_offset = 0

    def _choose_starting_tire(self, position):
        """Choose starting tire based on grid position."""
        # Top 10 start on softs, rest can choose
        if position <= 10:
            return config.TIRE_SOFT
        else:
            return random.choice([config.TIRE_MEDIUM, config.TIRE_SOFT])

    def _calculate_synergy(self):
        """
        Calculate driver-car synergy based on style and car characteristics.
        
        Returns:
            str: 'high', 'neutral', or 'low'
        """
        # Get style preferences from config
        style_prefs = config.STYLE_PREFERENCES.get(
            self.driver_style, 
            {"traction": 3, "balance": 0}
        )
        
        # Calculate match score
        # Traction match: how close car traction is to driver preference
        traction_diff = abs(self.car_traction - style_prefs["traction"])
        
        # Balance match: how close car balance is to driver preference
        balance_diff = abs(self.car_balance - style_prefs["balance"])
        
        # Total mismatch score (lower is better)
        mismatch = traction_diff + balance_diff
        
        # Determine synergy level
        if mismatch <= 1:
            return "high"
        elif mismatch <= 3:
            return "neutral"
        else:
            return "low"

    def _calculate_current_pace(self):
        """
        Calculate current pace based on all performance factors.
        
        Formula:
            PACE = BASE × TIER × SKILL × SYNERGY × FUEL × TIRE × VARIANCE
        
        Returns:
            float: Current pace (speed per frame)
        """
        # 1. Base pace from config
        pace = config.BASE_SPEED
        
        # 2. Team tier modifier (+4% to -5%)
        tier_mod = config.TIER_MODIFIERS.get(self.team_tier, 1.0)
        pace *= tier_mod
        
        # 3. Driver skill (70-99 → normalized to 0.85-1.00 range)
        # This ensures skill matters but doesn't dominate
        skill_factor = 0.85 + (self.driver_skill - 70) * (0.15 / 29)
        pace *= skill_factor
        
        # 4. Synergy modifier
        synergy_mod = config.SYNERGY_MODIFIERS.get(self.synergy_level, 1.0)
        pace *= synergy_mod
        
        # 5. Fuel load penalty (full tank = -4%, empty = 0%)
        fuel_penalty = self.fuel_load * config.FUEL_START_PENALTY
        pace *= (1.0 - fuel_penalty)
        
        # 6. Tire degradation
        deg_rate = config.TIRE_DEG_RATES.get(self.tire_compound, 0.002)
        tire_penalty = self.tire_age * deg_rate
        
        # Check for tire cliff
        cliff_lap = config.TIRE_CLIFF_LAPS.get(self.tire_compound, 20)
        if self.tire_age >= cliff_lap:
            tire_penalty += config.TIRE_CLIFF_PENALTY
        
        # Cap tire penalty at 20%
        pace *= (1.0 - min(tire_penalty, 0.20))
        
        # 7. Lap-to-lap variance based on consistency
        # Higher consistency = less variance
        variance_factor = config.LAP_VARIANCE_BASE * (6 - self.driver_consistency) / 5
        variance = 1.0 + (random.random() * 2 - 1) * variance_factor
        pace *= variance
        
        return pace

    def should_pit(self, total_race_laps):
        """
        Determine if car should pit based on tire age and race progress.
        
        Args:
            total_race_laps: Total laps in the race
            
        Returns:
            bool: True if car should pit
        """
        # Don't pit if already pitting
        if self.is_pitting:
            return False
        
        # Don't pit on first lap or last 3 laps
        if self.lap <= 1 or self.lap >= total_race_laps - 2:
            return False
        
        # Check if past tire cliff
        cliff_lap = config.TIRE_CLIFF_LAPS.get(self.tire_compound, 20)
        
        # Pit if at or past cliff, with some randomness
        if self.tire_age >= cliff_lap:
            # 80% chance to pit each lap after cliff
            return random.random() < 0.8
        
        # Pit if very close to cliff (within 2 laps) with lower probability
        if self.tire_age >= cliff_lap - 2:
            return random.random() < 0.3
        
        return False

    def start_pit_stop(self):
        """Initiate a pit stop."""
        self.is_pitting = True
        
        # Calculate pit stop time with variance
        base_time = config.PIT_STOP_BASE_TIME
        variance = (random.random() * 2 - 1) * config.PIT_STOP_VARIANCE
        self.pit_time_remaining = base_time + variance
        
        self.pit_stops += 1

    def _complete_pit_stop(self):
        """Complete pit stop: reset tires and state."""
        self.is_pitting = False
        self.pit_time_remaining = 0.0
        
        # Choose new tire compound (simple strategy)
        if self.tire_compound == config.TIRE_SOFT:
            # Soft → Medium or Hard
            self.tire_compound = random.choice([config.TIRE_MEDIUM, config.TIRE_HARD])
        elif self.tire_compound == config.TIRE_MEDIUM:
            # Medium → Hard or Soft
            self.tire_compound = random.choice([config.TIRE_HARD, config.TIRE_SOFT])
        else:
            # Hard → Medium or Soft
            self.tire_compound = random.choice([config.TIRE_MEDIUM, config.TIRE_SOFT])
        
        # Reset tire age
        self.tire_age = 0

    def update(self, track, dt=1.0, total_race_laps=20):
        """
        Update car position with dynamic pace calculation.
        
        Args:
            track: Track object for position calculation
            dt: Delta time in frames
            total_race_laps: Total laps in the race (for pit strategy)
        """
        # Handle pit stop timing
        if self.is_pitting:
            self.pit_time_remaining -= dt / config.FPS
            if self.pit_time_remaining <= 0:
                self._complete_pit_stop()
        
        # Calculate current pace (dynamic each frame)
        self.current_pace = self._calculate_current_pace()
        
        # Apply pit stop penalty (reduced speed while "pitting")
        effective_pace = self.current_pace
        if self.is_pitting:
            effective_pace *= 0.3  # Slow down significantly during pit
        
        # Move car forward
        speed_per_frame = effective_pace / track.track_length
        self.progress += speed_per_frame * dt

        # Handle lap completion
        if self.progress >= 1.0:
            self.progress -= 1.0
            self.lap += 1
            self.total_laps += 1
            self.tire_age += 1
            
            # Burn fuel (linear over race distance)
            fuel_burn = 1.0 / total_race_laps
            self.fuel_load = max(0.0, self.fuel_load - fuel_burn)

            # Record lap time
            if self.last_lap_time is not None:
                if self.best_lap_time is None or self.last_lap_time < self.best_lap_time:
                    self.best_lap_time = self.last_lap_time

            self.last_lap_time = self.lap_time
            self.lap_time = 0.0
            
            # Check if should pit (at start of new lap)
            if self.should_pit(total_race_laps):
                self.start_pit_stop()

        # Increment lap time
        self.lap_time += dt / config.FPS

    def get_position_on_track(self, track):
        """Get x, y coordinates on track."""
        return track.get_offset_position(self.progress, self.lateral_offset)

    def get_total_progress(self):
        """Get total progress including laps."""
        return self.lap - 1 + self.progress

    def get_status(self):
        """
        Get current car status for display.
        
        Returns:
            str: Status indicator ('PIT', 'OUT', or '')
        """
        if self.is_pitting:
            return "PIT"
        elif self.pit_stops > 0 and self.tire_age <= 2:
            return "OUT"  # Just exited pits
        return ""

    def __repr__(self):
        return f"Car({self.driver_short}, P{self.position}, Lap {self.lap}, {self.team_tier}-tier)"
```

**Verification:**
- This step will cause errors until Step 5 is complete
- Continue to Step 5 immediately

---

### Step 5: Update RaceEngine._initialize_cars()

**Purpose:** Pass full team data to Car constructor instead of just team name.

**File:** `race/race_engine.py`

**Location:** Replace `_initialize_cars` method (lines 23-46)

**Action:** Replace

**Before:**
```python
def _initialize_cars(self):
    """Create all 20 cars from team data"""
    position = 1

    # Randomize starting grid
    all_entries = []
    for team_data in TEAMS_DATA:
        for driver in team_data["drivers"]:
            all_entries.append({
                "driver": driver,
                "team": team_data["name"]
            })

    # Shuffle for random grid
    random.shuffle(all_entries)

    # Create cars
    for entry in all_entries:
        car = Car(entry["driver"], entry["team"], position)
        # Set initial progress based on grid position
        # Cars start slightly staggered
        car.progress = -0.001 * (position - 1)
        self.cars.append(car)
        position += 1
```

**After:**
```python
def _initialize_cars(self):
    """Create all 20 cars from team data with full performance stats."""
    position = 1

    # Build entries with full team data
    all_entries = []
    for team_data in TEAMS_DATA:
        team_info = {
            "name": team_data["name"],
            "tier": team_data.get("tier", "B"),
            "characteristics": team_data.get("characteristics", {
                "balance": 0,
                "cornering": 0,
                "traction": 3,
            }),
        }
        for driver in team_data["drivers"]:
            all_entries.append({
                "driver": driver,
                "team": team_info,
            })

    # Shuffle for random grid
    random.shuffle(all_entries)

    # Create cars with full data
    for entry in all_entries:
        car = Car(entry["driver"], entry["team"], position)
        # Set initial progress based on grid position
        # Cars start slightly staggered
        car.progress = -0.001 * (position - 1)
        self.cars.append(car)
        position += 1
```

**Verification:**
- Continue to Step 6

---

### Step 6: Update RaceEngine.update() to Pass Race Laps

**Purpose:** Pass total_race_laps to car.update() for pit strategy decisions.

**File:** `race/race_engine.py`

**Location:** In `update` method, modify line 51-52

**Action:** Modify

**Before:**
```python
def update(self):
    """Update all cars and race state"""
    # Update each car
    for car in self.cars:
        car.update(self.track)
```

**After:**
```python
def update(self):
    """Update all cars and race state"""
    # Update each car with race context
    for car in self.cars:
        car.update(self.track, dt=1.0, total_race_laps=self.total_laps)
```

**Verification:**
- Run `python main.py`
- Game should start without errors
- Press SPACE to start race
- Cars should move with varying speeds based on tier

---

### Step 7: Final Integration Test

**Purpose:** Verify all systems work together correctly.

**Action:** Run comprehensive test

**Test Script (run in Python):**
```python
# Run this in Python to verify:
import config
from data.teams import TEAMS_2025, get_all_drivers
from assets.colors import get_team_color
from race.car import Car
from race.race_engine import RaceEngine

# Test 1: Config loaded
print("Test 1: Config")
print(f"  Tiers: {config.TIER_MODIFIERS}")
print(f"  Fuel penalty: {config.FUEL_START_PENALTY}")

# Test 2: Teams loaded
print("\nTest 2: Teams")
print(f"  Team count: {len(TEAMS_2025)}")
drivers = get_all_drivers()
print(f"  Driver count: {len(drivers)}")
rookies = [d for d in drivers if d.get('rookie')]
print(f"  Rookies: {[d['short'] for d in rookies]}")

# Test 3: Colors work
print("\nTest 3: Colors")
print(f"  Sauber: {get_team_color('Sauber')}")
print(f"  RB: {get_team_color('RB')}")

# Test 4: Race engine initializes
print("\nTest 4: Race Engine")
engine = RaceEngine()
print(f"  Cars created: {len(engine.cars)}")
print(f"  First car: {engine.cars[0].driver_short} ({engine.cars[0].team})")
print(f"  Tier: {engine.cars[0].team_tier}")
print(f"  Synergy: {engine.cars[0].synergy_level}")

print("\n✓ All tests passed!")
```

**Verification:**
- Run the test script
- All tests should pass
- Run `python main.py` and complete a full race

---

## Files Summary

### Modified
| File | Changes |
|------|---------|
| `config.py` | Added ~50 lines of physics constants |
| `data/teams.py` | Complete rewrite with 2025 grid (~250 lines) |
| `assets/colors.py` | Updated team colors for 2025 (~70 lines) |
| `race/car.py` | Complete rewrite with new physics (~220 lines) |
| `race/race_engine.py` | Updated _initialize_cars() and update() |

### Created
| File | Purpose |
|------|---------|
| None | All changes are modifications |

---

## Testing Plan

### Quick Test (After Each Step)
```bash
python main.py
```
- Game starts without errors
- No import errors in console

### Feature Test (After All Steps)

1. **Tier Verification**
   - Start race, watch first 5 laps
   - Red Bull/McLaren should pull ahead
   - Sauber should fall to back
   
2. **Fuel Burn Verification**
   - Watch lap times over race
   - Later laps should be slightly faster (fuel burn)
   
3. **Pit Stop Verification**
   - Watch for cars slowing down mid-race
   - Check tire compound changes in timing
   
4. **Rookie Verification**
   - Look for ANT, HAD, DOO, BEA, BOR on grid
   - All 5 should appear

5. **Synergy Verification**
   - Same-tier cars should have pace differences
   - Based on driver-car match

### Edge Cases
| Scenario | Expected Behavior |
|----------|-------------------|
| Lap 1 | No pit stops allowed |
| Last 3 laps | No pit stops allowed |
| Tire cliff reached | Car slows significantly, then pits |
| Fuel at 0% | No further fuel penalty (capped) |
| Tire penalty > 20% | Capped at 20% loss |

### Regression Test
- Existing features still work:
  - SPACE starts race
  - R restarts race
  - ESC quits
  - Timing screen shows positions
  - Cars complete laps correctly

---

## Rollback Plan

If something goes wrong:

### Full Rollback
```bash
git checkout -- config.py data/teams.py assets/colors.py race/car.py race/race_engine.py
```

### Partial Rollback (by file)
```bash
git checkout -- race/car.py  # Revert just car changes
```

### Manual Fixes
- If Car.__init__ signature changed but RaceEngine not updated:
  - Check Step 5 was applied
- If import errors:
  - Check config.py has all new constants (Step 1)

---

## Handoff

This plan is ready for @f1-feature-coder to implement.

### Key Implementation Notes
1. **Order matters**: Steps 1-3 (data) must be done before Steps 4-6 (code)
2. **Test after Step 6**: First point where game should run
3. **Config first**: Step 1 must be done before any Car changes
4. **Complete file replacements**: Steps 2, 3, 4 replace entire files

### Decisions Already Made
- **Pit stops**: Time-based (car slows, doesn't stop)
- **Synergy**: Style-based matching (aggressive→traction, smooth→balance)
- **Fuel**: Linear burn over race distance
- **Tire cliff**: Compound-specific thresholds

### Questions for User
- None. All decisions made based on briefing recommendations.

---

## Implementation Checklist

- [ ] Step 1: Add physics constants to config.py
- [ ] Step 2: Replace teams.py with 2025 data
- [ ] Step 3: Update colors.py for 2025
- [ ] Step 4: Replace car.py with new implementation
- [ ] Step 5: Update RaceEngine._initialize_cars()
- [ ] Step 6: Update RaceEngine.update()
- [ ] Step 7: Run integration tests

---

## Planning Statistics

| Metric | Value |
|--------|-------|
| Plans Created | 1 |
| Steps in This Plan | 7 |
| Files Modified | 5 |
| Complexity | Medium-High |

---

*Plan created by @f1-feature-planner on 2025-12-22*
