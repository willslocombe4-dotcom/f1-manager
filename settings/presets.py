"""
PresetManager - Built-in and custom presets for game settings
"""
import json
import os
import config


# Built-in presets
PRESET_REALISTIC = {
    "name": "Realistic",
    "description": "Default simulation values - authentic F1 experience",
    "settings": {
        "race_laps": 20,
        "simulation_speed": 1.0,
        "tire_deg_rates": {
            config.TIRE_SOFT: 0.004,
            config.TIRE_MEDIUM: 0.002,
            config.TIRE_HARD: 0.001,
        },
        "tire_cliff_laps": {
            config.TIRE_SOFT: 12,
            config.TIRE_MEDIUM: 20,
            config.TIRE_HARD: 30,
        },
        "tire_cliff_penalty": 0.10,
        "max_tire_penalty": 0.20,
        "fuel_start_penalty": 0.04,
        "fuel_burn_per_lap": 0.002,
        "pit_stop_base_time": 4.0,
        "pit_stop_variance": 1.0,
        "pit_speed_penalty": 0.3,
        "pit_window_laps": 2,
        "pit_chance_after_cliff": 0.8,
        "pit_chance_near_cliff": 0.3,
        "last_laps_no_pit": 3,
        "tier_modifiers": {
            "S": 1.04,
            "A": 1.02,
            "B": 1.00,
            "C": 0.98,
            "D": 0.95,
        },
        "synergy_modifiers": {
            "high": 1.02,
            "neutral": 1.00,
            "low": 0.98,
        },
        "lap_variance_base": 0.005,
    }
}

PRESET_BALANCED = {
    "name": "Balanced",
    "description": "Tighter field - closer racing with reduced tier gaps",
    "settings": {
        "race_laps": 20,
        "simulation_speed": 1.0,
        "tire_deg_rates": {
            config.TIRE_SOFT: 0.003,
            config.TIRE_MEDIUM: 0.0015,
            config.TIRE_HARD: 0.001,
        },
        "tire_cliff_laps": {
            config.TIRE_SOFT: 15,
            config.TIRE_MEDIUM: 25,
            config.TIRE_HARD: 35,
        },
        "tire_cliff_penalty": 0.08,
        "max_tire_penalty": 0.15,
        "fuel_start_penalty": 0.03,
        "fuel_burn_per_lap": 0.002,
        "pit_stop_base_time": 3.5,
        "pit_stop_variance": 0.5,
        "pit_speed_penalty": 0.3,
        "pit_window_laps": 3,
        "pit_chance_after_cliff": 0.7,
        "pit_chance_near_cliff": 0.25,
        "last_laps_no_pit": 3,
        "tier_modifiers": {
            "S": 1.02,  # Reduced from +4% to +2%
            "A": 1.01,  # Reduced from +2% to +1%
            "B": 1.00,
            "C": 0.99,  # Reduced from -2% to -1%
            "D": 0.98,  # Reduced from -5% to -2%
        },
        "synergy_modifiers": {
            "high": 1.01,
            "neutral": 1.00,
            "low": 0.99,
        },
        "lap_variance_base": 0.004,
    }
}

PRESET_CHAOS = {
    "name": "Chaos",
    "description": "Fast tire deg, high variance, unpredictable races",
    "settings": {
        "race_laps": 15,  # Shorter races
        "simulation_speed": 1.0,
        "tire_deg_rates": {
            config.TIRE_SOFT: 0.008,  # Double degradation
            config.TIRE_MEDIUM: 0.005,
            config.TIRE_HARD: 0.003,
        },
        "tire_cliff_laps": {
            config.TIRE_SOFT: 6,  # Half the cliff laps
            config.TIRE_MEDIUM: 10,
            config.TIRE_HARD: 15,
        },
        "tire_cliff_penalty": 0.15,  # Harsher cliff
        "max_tire_penalty": 0.30,
        "fuel_start_penalty": 0.06,
        "fuel_burn_per_lap": 0.003,
        "pit_stop_base_time": 3.0,
        "pit_stop_variance": 2.0,  # High variance
        "pit_speed_penalty": 0.3,
        "pit_window_laps": 1,
        "pit_chance_after_cliff": 0.9,
        "pit_chance_near_cliff": 0.5,
        "last_laps_no_pit": 2,
        "tier_modifiers": {
            "S": 1.03,
            "A": 1.01,
            "B": 1.00,
            "C": 0.99,
            "D": 0.97,
        },
        "synergy_modifiers": {
            "high": 1.03,
            "neutral": 1.00,
            "low": 0.97,
        },
        "lap_variance_base": 0.010,  # Double variance
    }
}

# All built-in presets
BUILTIN_PRESETS = [PRESET_REALISTIC, PRESET_BALANCED, PRESET_CHAOS]


class PresetManager:
    """Manages built-in and custom presets."""
    
    CUSTOM_PRESETS_FILE = "custom_presets.json"
    
    def __init__(self):
        self.custom_presets = []
        self._load_custom_presets()
    
    def get_builtin_presets(self):
        """Get list of built-in presets."""
        return BUILTIN_PRESETS
    
    def get_custom_presets(self):
        """Get list of custom presets."""
        return self.custom_presets
    
    def get_all_presets(self):
        """Get all presets (built-in + custom)."""
        return BUILTIN_PRESETS + self.custom_presets
    
    def get_preset_by_name(self, name):
        """Get a preset by name."""
        for preset in self.get_all_presets():
            if preset["name"] == name:
                return preset
        return None
    
    def save_custom_preset(self, name, description, settings_dict):
        """
        Save a custom preset.
        
        Args:
            name: Preset name
            description: Preset description
            settings_dict: Settings dictionary from RuntimeConfig.to_dict()
        """
        # Check if preset with this name already exists
        for i, preset in enumerate(self.custom_presets):
            if preset["name"] == name:
                # Update existing preset
                self.custom_presets[i] = {
                    "name": name,
                    "description": description,
                    "settings": settings_dict,
                    "custom": True,
                }
                self._save_custom_presets()
                return
        
        # Add new preset
        self.custom_presets.append({
            "name": name,
            "description": description,
            "settings": settings_dict,
            "custom": True,
        })
        self._save_custom_presets()
    
    def delete_custom_preset(self, name):
        """Delete a custom preset by name."""
        self.custom_presets = [p for p in self.custom_presets if p["name"] != name]
        self._save_custom_presets()
    
    def _load_custom_presets(self):
        """Load custom presets from file."""
        if os.path.exists(self.CUSTOM_PRESETS_FILE):
            try:
                with open(self.CUSTOM_PRESETS_FILE, 'r') as f:
                    self.custom_presets = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.custom_presets = []
        else:
            self.custom_presets = []
    
    def _save_custom_presets(self):
        """Save custom presets to file."""
        try:
            with open(self.CUSTOM_PRESETS_FILE, 'w') as f:
                json.dump(self.custom_presets, f, indent=2)
        except IOError:
            pass  # Silently fail if can't save
