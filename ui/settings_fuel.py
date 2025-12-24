"""
SettingsFuelScreen - Fuel system settings
"""
import pygame
import config
from ui.settings_base import BaseSettingsScreen, SettingItem
from settings.runtime_config import runtime_config


class SettingsFuelScreen(BaseSettingsScreen):
    """Settings screen for fuel configuration."""
    
    def __init__(self, surface):
        super().__init__(surface, "FUEL SETTINGS")
        self._init_items()
    
    def _init_items(self):
        """Initialize fuel setting items."""
        self.items = [
            SettingItem(
                "Start Penalty",
                "fuel_start_penalty",
                runtime_config.fuel_start_penalty,
                min_val=0.01,
                max_val=0.10,
                step=0.01,
                format_func=lambda v: f"-{v*100:.0f}% pace"
            ),
            SettingItem(
                "Burn Rate",
                "fuel_burn_per_lap",
                runtime_config.fuel_burn_per_lap,
                min_val=0.001,
                max_val=0.005,
                step=0.0005,
                format_func=lambda v: f"+{v*100:.2f}%/lap"
            ),
        ]
    
    def _on_value_changed(self, item):
        """Update runtime config when value changes."""
        if item.key == "fuel_start_penalty":
            runtime_config.fuel_start_penalty = item.value
        elif item.key == "fuel_burn_per_lap":
            runtime_config.fuel_burn_per_lap = item.value
