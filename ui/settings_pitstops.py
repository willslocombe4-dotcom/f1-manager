"""
SettingsPitstopsScreen - Pit stop settings
"""
import pygame
import config
from ui.settings_base import BaseSettingsScreen, SettingItem
from settings.runtime_config import runtime_config


class SettingsPitstopsScreen(BaseSettingsScreen):
    """Settings screen for pit stop configuration."""
    
    def __init__(self, surface):
        super().__init__(surface, "PIT STOP SETTINGS")
        self._init_items()
    
    def _init_items(self):
        """Initialize pit stop setting items."""
        self.items = [
            SettingItem(
                "Base Time",
                "pit_stop_base_time",
                runtime_config.pit_stop_base_time,
                min_val=2.0,
                max_val=8.0,
                step=0.5,
                format_func=lambda v: f"{v:.1f}s"
            ),
            SettingItem(
                "Time Variance",
                "pit_stop_variance",
                runtime_config.pit_stop_variance,
                min_val=0.0,
                max_val=3.0,
                step=0.25,
                format_func=lambda v: f"±{v:.2f}s"
            ),
            SettingItem(
                "Pit Window",
                "pit_window_laps",
                runtime_config.pit_window_laps,
                min_val=1,
                max_val=5,
                step=1,
                format_func=lambda v: f"{v} laps before cliff"
            ),
            SettingItem(
                "Pit Chance (After Cliff)",
                "pit_chance_after_cliff",
                runtime_config.pit_chance_after_cliff,
                min_val=0.5,
                max_val=1.0,
                step=0.05,
                format_func=lambda v: f"{v*100:.0f}%"
            ),
            SettingItem(
                "Pit Chance (Near Cliff)",
                "pit_chance_near_cliff",
                runtime_config.pit_chance_near_cliff,
                min_val=0.1,
                max_val=0.6,
                step=0.05,
                format_func=lambda v: f"{v*100:.0f}%"
            ),
            SettingItem(
                "No Pit (Last Laps)",
                "last_laps_no_pit",
                runtime_config.last_laps_no_pit,
                min_val=1,
                max_val=5,
                step=1,
                format_func=lambda v: f"Last {v} laps"
            ),
        ]
    
    def _on_value_changed(self, item):
        """Update runtime config when value changes."""
        if item.key == "pit_stop_base_time":
            runtime_config.pit_stop_base_time = item.value
        elif item.key == "pit_stop_variance":
            runtime_config.pit_stop_variance = item.value
        elif item.key == "pit_window_laps":
            runtime_config.pit_window_laps = item.value
        elif item.key == "pit_chance_after_cliff":
            runtime_config.pit_chance_after_cliff = item.value
        elif item.key == "pit_chance_near_cliff":
            runtime_config.pit_chance_near_cliff = item.value
        elif item.key == "last_laps_no_pit":
            runtime_config.last_laps_no_pit = item.value
