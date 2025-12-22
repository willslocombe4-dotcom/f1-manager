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
