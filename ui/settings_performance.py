"""
SettingsPerformanceScreen - Performance tier and synergy settings
"""
import pygame
import config
from ui.settings_base import BaseSettingsScreen, SettingItem
from settings.runtime_config import runtime_config


class SettingsPerformanceScreen(BaseSettingsScreen):
    """Settings screen for performance configuration."""
    
    def __init__(self, surface):
        super().__init__(surface, "PERFORMANCE SETTINGS")
        self._init_items()
    
    def _init_items(self):
        """Initialize performance setting items."""
        self.items = [
            # Tier modifiers
            SettingItem(
                "S-Tier Modifier",
                "tier_s",
                runtime_config.tier_modifiers["S"],
                min_val=1.00,
                max_val=1.10,
                step=0.01,
                format_func=lambda v: f"+{(v-1)*100:.0f}%" if v >= 1 else f"{(v-1)*100:.0f}%"
            ),
            SettingItem(
                "A-Tier Modifier",
                "tier_a",
                runtime_config.tier_modifiers["A"],
                min_val=0.98,
                max_val=1.06,
                step=0.01,
                format_func=lambda v: f"+{(v-1)*100:.0f}%" if v >= 1 else f"{(v-1)*100:.0f}%"
            ),
            SettingItem(
                "B-Tier Modifier",
                "tier_b",
                runtime_config.tier_modifiers["B"],
                min_val=0.96,
                max_val=1.04,
                step=0.01,
                format_func=lambda v: f"+{(v-1)*100:.0f}%" if v >= 1 else f"{(v-1)*100:.0f}%"
            ),
            SettingItem(
                "C-Tier Modifier",
                "tier_c",
                runtime_config.tier_modifiers["C"],
                min_val=0.94,
                max_val=1.02,
                step=0.01,
                format_func=lambda v: f"+{(v-1)*100:.0f}%" if v >= 1 else f"{(v-1)*100:.0f}%"
            ),
            SettingItem(
                "D-Tier Modifier",
                "tier_d",
                runtime_config.tier_modifiers["D"],
                min_val=0.90,
                max_val=1.00,
                step=0.01,
                format_func=lambda v: f"+{(v-1)*100:.0f}%" if v >= 1 else f"{(v-1)*100:.0f}%"
            ),
            # Synergy modifiers
            SettingItem(
                "High Synergy",
                "synergy_high",
                runtime_config.synergy_modifiers["high"],
                min_val=1.00,
                max_val=1.05,
                step=0.005,
                format_func=lambda v: f"+{(v-1)*100:.1f}%"
            ),
            SettingItem(
                "Low Synergy",
                "synergy_low",
                runtime_config.synergy_modifiers["low"],
                min_val=0.95,
                max_val=1.00,
                step=0.005,
                format_func=lambda v: f"{(v-1)*100:.1f}%"
            ),
            # Lap variance
            SettingItem(
                "Lap Variance",
                "lap_variance_base",
                runtime_config.lap_variance_base,
                min_val=0.002,
                max_val=0.015,
                step=0.001,
                format_func=lambda v: f"±{v*100:.1f}%"
            ),
        ]
    
    def _on_value_changed(self, item):
        """Update runtime config when value changes."""
        if item.key == "tier_s":
            runtime_config.tier_modifiers["S"] = item.value
        elif item.key == "tier_a":
            runtime_config.tier_modifiers["A"] = item.value
        elif item.key == "tier_b":
            runtime_config.tier_modifiers["B"] = item.value
        elif item.key == "tier_c":
            runtime_config.tier_modifiers["C"] = item.value
        elif item.key == "tier_d":
            runtime_config.tier_modifiers["D"] = item.value
        elif item.key == "synergy_high":
            runtime_config.synergy_modifiers["high"] = item.value
        elif item.key == "synergy_low":
            runtime_config.synergy_modifiers["low"] = item.value
        elif item.key == "lap_variance_base":
            runtime_config.lap_variance_base = item.value
