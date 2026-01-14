"""
F1 Manager - Game Configuration
"""

VERSION = "0.1.0"

# Screen settings
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

# Display settings
BASE_WIDTH = 1600
BASE_HEIGHT = 900
FULLSCREEN = True
SCALE_FACTOR = 1.0  # Will be calculated at runtime

# Supported resolutions
SUPPORTED_RESOLUTIONS = [
    (1280, 720),    # HD
    (1600, 900),    # HD+
    (1920, 1080),   # Full HD
    (2560, 1440),   # QHD
    (3840, 2160),   # 4K UHD
]

# Layout (base values - will be scaled at runtime)
TRACK_VIEW_WIDTH = 1000
TIMING_VIEW_WIDTH = 600
TIMING_VIEW_X = TRACK_VIEW_WIDTH

def get_scaled(value):
    """Get a value scaled by the current scale factor."""
    return int(value * SCALE_FACTOR)

# Track settings
TRACK_CENTER_X = TRACK_VIEW_WIDTH // 2
TRACK_CENTER_Y = SCREEN_HEIGHT // 2
TRACK_OUTER_RADIUS = 350
TRACK_INNER_RADIUS = 250
TRACK_WIDTH = TRACK_OUTER_RADIUS - TRACK_INNER_RADIUS

# Car settings
CAR_SIZE = 12
CAR_SPACING = 25  # Minimum distance between cars on same position
BASE_SPEED = 0.014  # Base speed - ~80 second lap times (realistic F1)
SPEED_VARIANCE = 0.3  # Speed variation between cars
CAR_SMOOTHING = 0.15  # Lerp factor for smooth car movement (0.1 = smooth, 0.3 = responsive)

# Simulation Speed Control
SIMULATION_SPEED_DEFAULT = 1.0  # 1x = real-time (~80 second laps)
SIMULATION_SPEED_OPTIONS = [1, 2, 5, 10, 20]  # Available speed multipliers

# Race settings
NUM_CARS = 20
NUM_TEAMS = 10
DRIVERS_PER_TEAM = 2

# Colors (UI)
BG_COLOR = (15, 15, 15)  # Dark background
TRACK_BG_COLOR = (20, 20, 20)
TIMING_BG_COLOR = (18, 18, 18)
TRACK_COLOR = (40, 40, 40)
TRACK_LINE_COLOR = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)
TEXT_GRAY = (150, 150, 150)
POSITION_GAIN_COLOR = (0, 255, 100)
POSITION_LOSS_COLOR = (255, 50, 50)

# Fonts
FONT_SIZE_LARGE = 32
FONT_SIZE_MEDIUM = 20
FONT_SIZE_SMALL = 16

# Game States
GAME_STATE_MENU = "menu"
GAME_STATE_TRACK_SELECTION = "track_selection"
GAME_STATE_RACING = "racing"
GAME_STATE_RESULTS = "results"
GAME_STATE_SETTINGS = "settings"  # Now for display settings
GAME_STATE_CONFIG = "config"      # Renamed from settings (gameplay config)

# Track Loading
TRACKS_DIRECTORY = "tools/tracks"
DEFAULT_TRACK_NAME = "default"

# Tire compounds
TIRE_SOFT = "SOFT"
TIRE_MEDIUM = "MEDIUM"
TIRE_HARD = "HARD"

TIRE_COLORS = {
    TIRE_SOFT: (255, 50, 50),
    TIRE_MEDIUM: (255, 215, 0),
    TIRE_HARD: (240, 240, 240)
}

# Track visual elements
GRASS_BASE_COLOR = (30, 80, 30)
GRASS_LIGHT_COLOR = (40, 100, 40)
GRASS_COLOR = (34, 139, 34)  # Forest green for explicit grass decorations
GRAVEL_COLOR = (194, 178, 128)
GRAVEL_BORDER_COLOR = (170, 155, 110)
KERB_RED = (200, 0, 0)
KERB_WHITE = (255, 255, 255)
KERB_WIDTH = 8  # Width of kerb stripes
KERB_MIN_CORNER_ANGLE = 30  # Degrees - minimum corner angle to draw kerbs at all

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
PIT_STOP_BASE_TIME = 4.0       # Base pit stop time in seconds (proportional to new lap time)
PIT_STOP_VARIANCE = 1.0        # Random variance ±1 second

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

# Driver Skill Normalization
# Maps skill range (70-99) to a multiplier range (0.85-1.00)
SKILL_MIN = 70              # Minimum possible skill value
SKILL_MAX = 99              # Maximum possible skill value
SKILL_MIN_FACTOR = 0.85     # Multiplier for minimum skill
SKILL_FACTOR_RANGE = 0.15   # Range of skill multiplier (1.00 - 0.85)

# Tire Penalty Cap
MAX_TIRE_PENALTY = 0.20     # Maximum tire degradation penalty (20%)

# Pit Stop Strategy
PIT_WINDOW_LAPS = 2         # Laps before cliff where early pit is possible
PIT_CHANCE_AFTER_CLIFF = 0.8  # 80% chance to pit each lap after cliff
PIT_CHANCE_NEAR_CLIFF = 0.3   # 30% chance to pit when near cliff
PIT_SPEED_PENALTY = 0.3       # Speed multiplier during pit (30% of normal)
LAST_LAPS_NO_PIT = 3          # Don't pit in last N laps

# DRS (Drag Reduction System)
DRS_DETECTION_TIME = 1.0      # Gap required to car ahead (in seconds)
DRS_SPEED_BOOST = 0.08        # +8% speed boost when DRS is active
DRS_ENABLED_FROM_LAP = 2      # DRS becomes available from this lap onwards

# Track Characteristics
DEFAULT_TIRE_DEG_MULTIPLIER = 1.0  # Default tire degradation multiplier for custom tracks



