"""
RuntimeConfig - Modifiable settings layer (singleton)
Provides runtime-adjustable game settings that override config.py defaults.
"""
import config


class RuntimeConfig:
    """
    Singleton class for runtime-modifiable game settings.
    
    All values default to config.py constants but can be modified at runtime.
    Changes persist through SettingsPersistence.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        # Initialize all settings to defaults from config.py
        self.reset_to_defaults()
    
    def reset_to_defaults(self):
        """Reset all settings to config.py defaults."""
        # Display settings
        self.display_width = 1280  # Default windowed width (smaller for 4K screens)
        self.display_height = 720  # Default windowed height
        self.fullscreen = False    # Start in windowed mode
        
        # Race settings
        self.race_laps = 20  # Default sprint race
        self.simulation_speed = config.SIMULATION_SPEED_DEFAULT
        
        # Tire settings
        self.tire_deg_rates = {
            config.TIRE_SOFT: config.TIRE_DEG_RATES[config.TIRE_SOFT],
            config.TIRE_MEDIUM: config.TIRE_DEG_RATES[config.TIRE_MEDIUM],
            config.TIRE_HARD: config.TIRE_DEG_RATES[config.TIRE_HARD],
        }
        self.tire_cliff_laps = {
            config.TIRE_SOFT: config.TIRE_CLIFF_LAPS[config.TIRE_SOFT],
            config.TIRE_MEDIUM: config.TIRE_CLIFF_LAPS[config.TIRE_MEDIUM],
            config.TIRE_HARD: config.TIRE_CLIFF_LAPS[config.TIRE_HARD],
        }
        self.tire_cliff_penalty = config.TIRE_CLIFF_PENALTY
        self.max_tire_penalty = config.MAX_TIRE_PENALTY
        
        # Fuel settings
        self.fuel_start_penalty = config.FUEL_START_PENALTY
        self.fuel_burn_per_lap = config.FUEL_BURN_PER_LAP
        
        # Pit stop settings
        self.pit_stop_base_time = config.PIT_STOP_BASE_TIME
        self.pit_stop_variance = config.PIT_STOP_VARIANCE
        self.pit_speed_penalty = config.PIT_SPEED_PENALTY
        self.pit_window_laps = config.PIT_WINDOW_LAPS
        self.pit_chance_after_cliff = config.PIT_CHANCE_AFTER_CLIFF
        self.pit_chance_near_cliff = config.PIT_CHANCE_NEAR_CLIFF
        self.last_laps_no_pit = config.LAST_LAPS_NO_PIT
        
        # Performance settings
        self.tier_modifiers = {
            "S": config.TIER_MODIFIERS["S"],
            "A": config.TIER_MODIFIERS["A"],
            "B": config.TIER_MODIFIERS["B"],
            "C": config.TIER_MODIFIERS["C"],
            "D": config.TIER_MODIFIERS["D"],
        }
        self.synergy_modifiers = {
            "high": config.SYNERGY_MODIFIERS["high"],
            "neutral": config.SYNERGY_MODIFIERS["neutral"],
            "low": config.SYNERGY_MODIFIERS["low"],
        }
        self.lap_variance_base = config.LAP_VARIANCE_BASE
    
    def to_dict(self):
        """Convert settings to dictionary for persistence."""
        return {
            "display_width": self.display_width,
            "display_height": self.display_height,
            "fullscreen": self.fullscreen,
            "race_laps": self.race_laps,
            "simulation_speed": self.simulation_speed,
            "tire_deg_rates": self.tire_deg_rates,
            "tire_cliff_laps": self.tire_cliff_laps,
            "tire_cliff_penalty": self.tire_cliff_penalty,
            "max_tire_penalty": self.max_tire_penalty,
            "fuel_start_penalty": self.fuel_start_penalty,
            "fuel_burn_per_lap": self.fuel_burn_per_lap,
            "pit_stop_base_time": self.pit_stop_base_time,
            "pit_stop_variance": self.pit_stop_variance,
            "pit_speed_penalty": self.pit_speed_penalty,
            "pit_window_laps": self.pit_window_laps,
            "pit_chance_after_cliff": self.pit_chance_after_cliff,
            "pit_chance_near_cliff": self.pit_chance_near_cliff,
            "last_laps_no_pit": self.last_laps_no_pit,
            "tier_modifiers": self.tier_modifiers,
            "synergy_modifiers": self.synergy_modifiers,
            "lap_variance_base": self.lap_variance_base,
        }
    
    def from_dict(self, data):
        """Load settings from dictionary."""
        if not data:
            return
        
        # Display settings
        if "display_width" in data:
            self.display_width = data["display_width"]
        if "display_height" in data:
            self.display_height = data["display_height"]
        if "fullscreen" in data:
            self.fullscreen = data["fullscreen"]
        
        # Race settings
        if "race_laps" in data:
            self.race_laps = data["race_laps"]
        if "simulation_speed" in data:
            self.simulation_speed = data["simulation_speed"]
        
        # Tire settings
        if "tire_deg_rates" in data:
            self.tire_deg_rates.update(data["tire_deg_rates"])
        if "tire_cliff_laps" in data:
            self.tire_cliff_laps.update(data["tire_cliff_laps"])
        if "tire_cliff_penalty" in data:
            self.tire_cliff_penalty = data["tire_cliff_penalty"]
        if "max_tire_penalty" in data:
            self.max_tire_penalty = data["max_tire_penalty"]
        
        # Fuel settings
        if "fuel_start_penalty" in data:
            self.fuel_start_penalty = data["fuel_start_penalty"]
        if "fuel_burn_per_lap" in data:
            self.fuel_burn_per_lap = data["fuel_burn_per_lap"]
        
        # Pit stop settings
        if "pit_stop_base_time" in data:
            self.pit_stop_base_time = data["pit_stop_base_time"]
        if "pit_stop_variance" in data:
            self.pit_stop_variance = data["pit_stop_variance"]
        if "pit_speed_penalty" in data:
            self.pit_speed_penalty = data["pit_speed_penalty"]
        if "pit_window_laps" in data:
            self.pit_window_laps = data["pit_window_laps"]
        if "pit_chance_after_cliff" in data:
            self.pit_chance_after_cliff = data["pit_chance_after_cliff"]
        if "pit_chance_near_cliff" in data:
            self.pit_chance_near_cliff = data["pit_chance_near_cliff"]
        if "last_laps_no_pit" in data:
            self.last_laps_no_pit = data["last_laps_no_pit"]
        
        # Performance settings
        if "tier_modifiers" in data:
            self.tier_modifiers.update(data["tier_modifiers"])
        if "synergy_modifiers" in data:
            self.synergy_modifiers.update(data["synergy_modifiers"])
        if "lap_variance_base" in data:
            self.lap_variance_base = data["lap_variance_base"]


# Global singleton instance
runtime_config = RuntimeConfig()
