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
