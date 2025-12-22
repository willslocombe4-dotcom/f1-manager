"""
F1 Teams and Drivers Data - 2024 Season
"""

TEAMS_DATA = [
    {
        "name": "Red Bull Racing",
        "drivers": [
            {"number": 1, "name": "Max Verstappen", "short": "VER"},
            {"number": 11, "name": "Sergio Perez", "short": "PER"}
        ]
    },
    {
        "name": "Ferrari",
        "drivers": [
            {"number": 16, "name": "Charles Leclerc", "short": "LEC"},
            {"number": 55, "name": "Carlos Sainz", "short": "SAI"}
        ]
    },
    {
        "name": "Mercedes",
        "drivers": [
            {"number": 44, "name": "Lewis Hamilton", "short": "HAM"},
            {"number": 63, "name": "George Russell", "short": "RUS"}
        ]
    },
    {
        "name": "McLaren",
        "drivers": [
            {"number": 4, "name": "Lando Norris", "short": "NOR"},
            {"number": 81, "name": "Oscar Piastri", "short": "PIA"}
        ]
    },
    {
        "name": "Aston Martin",
        "drivers": [
            {"number": 14, "name": "Fernando Alonso", "short": "ALO"},
            {"number": 18, "name": "Lance Stroll", "short": "STR"}
        ]
    },
    {
        "name": "Alpine",
        "drivers": [
            {"number": 10, "name": "Pierre Gasly", "short": "GAS"},
            {"number": 31, "name": "Esteban Ocon", "short": "OCO"}
        ]
    },
    {
        "name": "Williams",
        "drivers": [
            {"number": 23, "name": "Alexander Albon", "short": "ALB"},
            {"number": 2, "name": "Logan Sargeant", "short": "SAR"}
        ]
    },
    {
        "name": "Alfa Romeo",
        "drivers": [
            {"number": 77, "name": "Valtteri Bottas", "short": "BOT"},
            {"number": 24, "name": "Zhou Guanyu", "short": "ZHO"}
        ]
    },
    {
        "name": "Haas",
        "drivers": [
            {"number": 27, "name": "Nico Hulkenberg", "short": "HUL"},
            {"number": 20, "name": "Kevin Magnussen", "short": "MAG"}
        ]
    },
    {
        "name": "AlphaTauri",
        "drivers": [
            {"number": 22, "name": "Yuki Tsunoda", "short": "TSU"},
            {"number": 21, "name": "Daniel Ricciardo", "short": "RIC"}
        ]
    }
]

def get_all_drivers():
    """Get a flat list of all drivers with team information"""
    all_drivers = []
    for team in TEAMS_DATA:
        for driver in team["drivers"]:
            all_drivers.append({
                "team": team["name"],
                "number": driver["number"],
                "name": driver["name"],
                "short": driver["short"]
            })
    return all_drivers
