"""
F1 Team Colors - 2024 Season
"""

# Team color definitions (Primary, Secondary)
TEAM_COLORS = {
    "Red Bull Racing": {
        "primary": (30, 65, 170),  # Dark Blue
        "secondary": (255, 200, 0),  # Yellow
        "name_short": "RBR"
    },
    "Ferrari": {
        "primary": (220, 0, 0),  # Red
        "secondary": (255, 255, 255),  # White
        "name_short": "FER"
    },
    "Mercedes": {
        "primary": (0, 210, 190),  # Teal
        "secondary": (0, 0, 0),  # Black
        "name_short": "MER"
    },
    "McLaren": {
        "primary": (255, 135, 0),  # Papaya Orange
        "secondary": (0, 0, 0),  # Black
        "name_short": "MCL"
    },
    "Aston Martin": {
        "primary": (0, 111, 98),  # British Racing Green
        "secondary": (0, 230, 180),  # Lime
        "name_short": "AST"
    },
    "Alpine": {
        "primary": (255, 135, 180),  # Pink
        "secondary": (0, 144, 255),  # Blue
        "name_short": "ALP"
    },
    "Williams": {
        "primary": (0, 82, 255),  # Blue
        "secondary": (255, 255, 255),  # White
        "name_short": "WIL"
    },
    "Alfa Romeo": {
        "primary": (155, 0, 40),  # Burgundy
        "secondary": (255, 255, 255),  # White
        "name_short": "ALF"
    },
    "Haas": {
        "primary": (180, 180, 180),  # Silver
        "secondary": (220, 0, 30),  # Red
        "name_short": "HAA"
    },
    "AlphaTauri": {
        "primary": (43, 69, 98),  # Navy Blue
        "secondary": (255, 255, 255),  # White
        "name_short": "AT"
    }
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
