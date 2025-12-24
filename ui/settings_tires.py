"""
SettingsTiresScreen - Tire degradation settings
"""
import pygame
import config
from ui.settings_base import BaseSettingsScreen, SettingItem
from settings.runtime_config import runtime_config


class SettingsTiresScreen(BaseSettingsScreen):
    """Settings screen for tire configuration."""
    
    def __init__(self, surface):
        super().__init__(surface, "TIRE SETTINGS")
        self._init_items()
    
    def _init_items(self):
        """Initialize tire setting items."""
        self.items = [
            # Degradation rates
            SettingItem(
                "Soft Deg Rate",
                "soft_deg",
                runtime_config.tire_deg_rates[config.TIRE_SOFT],
                min_val=0.001,
                max_val=0.010,
                step=0.001,
                format_func=lambda v: f"{v*100:.1f}%/lap"
            ),
            SettingItem(
                "Medium Deg Rate",
                "medium_deg",
                runtime_config.tire_deg_rates[config.TIRE_MEDIUM],
                min_val=0.001,
                max_val=0.008,
                step=0.001,
                format_func=lambda v: f"{v*100:.1f}%/lap"
            ),
            SettingItem(
                "Hard Deg Rate",
                "hard_deg",
                runtime_config.tire_deg_rates[config.TIRE_HARD],
                min_val=0.0005,
                max_val=0.005,
                step=0.0005,
                format_func=lambda v: f"{v*100:.2f}%/lap"
            ),
            # Cliff laps
            SettingItem(
                "Soft Cliff",
                "soft_cliff",
                runtime_config.tire_cliff_laps[config.TIRE_SOFT],
                min_val=5,
                max_val=25,
                step=1,
                format_func=lambda v: f"{v} laps"
            ),
            SettingItem(
                "Medium Cliff",
                "medium_cliff",
                runtime_config.tire_cliff_laps[config.TIRE_MEDIUM],
                min_val=10,
                max_val=40,
                step=2,
                format_func=lambda v: f"{v} laps"
            ),
            SettingItem(
                "Hard Cliff",
                "hard_cliff",
                runtime_config.tire_cliff_laps[config.TIRE_HARD],
                min_val=15,
                max_val=50,
                step=2,
                format_func=lambda v: f"{v} laps"
            ),
            # Cliff penalty
            SettingItem(
                "Cliff Penalty",
                "cliff_penalty",
                runtime_config.tire_cliff_penalty,
                min_val=0.05,
                max_val=0.25,
                step=0.01,
                format_func=lambda v: f"-{v*100:.0f}%"
            ),
        ]
    
    def _on_value_changed(self, item):
        """Update runtime config when value changes."""
        if item.key == "soft_deg":
            runtime_config.tire_deg_rates[config.TIRE_SOFT] = item.value
        elif item.key == "medium_deg":
            runtime_config.tire_deg_rates[config.TIRE_MEDIUM] = item.value
        elif item.key == "hard_deg":
            runtime_config.tire_deg_rates[config.TIRE_HARD] = item.value
        elif item.key == "soft_cliff":
            runtime_config.tire_cliff_laps[config.TIRE_SOFT] = item.value
        elif item.key == "medium_cliff":
            runtime_config.tire_cliff_laps[config.TIRE_MEDIUM] = item.value
        elif item.key == "hard_cliff":
            runtime_config.tire_cliff_laps[config.TIRE_HARD] = item.value
        elif item.key == "cliff_penalty":
            runtime_config.tire_cliff_penalty = item.value
