"""
SettingsRaceScreen - Race settings (laps, simulation speed)
"""
import pygame
import config
from ui.settings_base import BaseSettingsScreen, SettingItem
from settings.runtime_config import runtime_config


class SettingsRaceScreen(BaseSettingsScreen):
    """Settings screen for race configuration."""
    
    def __init__(self, surface):
        super().__init__(surface, "RACE SETTINGS")
        self._init_items()
    
    def _init_items(self):
        """Initialize race setting items."""
        self.items = [
            SettingItem(
                "Race Laps",
                "race_laps",
                runtime_config.race_laps,
                min_val=5,
                max_val=70,
                step=5,
                format_func=lambda v: f"{v} laps"
            ),
            SettingItem(
                "Default Sim Speed",
                "simulation_speed",
                runtime_config.simulation_speed,
                options=[1, 2, 5, 10, 20],
                format_func=lambda v: f"{v}x"
            ),
        ]
    
    def _on_value_changed(self, item):
        """Update runtime config when value changes."""
        if item.key == "race_laps":
            runtime_config.race_laps = item.value
        elif item.key == "simulation_speed":
            runtime_config.simulation_speed = item.value
