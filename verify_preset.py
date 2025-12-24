# Save as: verify_preset.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from settings.runtime_config import runtime_config
from settings.presets import PRESET_CHAOS

print("=== Preset Loading Verification ===")
print()

# Check initial state
print(f"Before loading preset:")
print(f"  race_laps = {runtime_config.race_laps}")
print()

# Load Chaos preset
print(f"Loading Chaos preset...")
print(f"  preset['settings']['race_laps'] = {PRESET_CHAOS['settings']['race_laps']}")
runtime_config.from_dict(PRESET_CHAOS["settings"])
print()

# Check after loading
print(f"After loading preset:")
print(f"  race_laps = {runtime_config.race_laps}")
print()

# Verify
if runtime_config.race_laps == 15:
    print("SUCCESS: Preset loaded correctly!")
else:
    print(f"FAILURE: Expected 15, got {runtime_config.race_laps}")

# Reset for next test
runtime_config.reset_to_defaults()
