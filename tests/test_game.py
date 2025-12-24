#!/usr/bin/env python3
"""
F1 Manager - Headless Test Suite
================================

Runs automated tests without requiring a display.
Tests settings, presets, persistence, race engine, and integration.

Usage:
    python tests/test_game.py           # Run all tests
    python tests/test_game.py settings  # Run specific suite
    python tests/test_game.py presets
    python tests/test_game.py persistence
    python tests/test_game.py race
    python tests/test_game.py integration
    python tests/test_game.py pygame

Exit codes:
    0 = All tests passed
    1 = Some tests failed
"""

# CRITICAL: Set headless mode BEFORE importing pygame
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
import tempfile
import json

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


# =============================================================================
# TEST FRAMEWORK (No external dependencies)
# =============================================================================

class TestResult:
    """Tracks test results."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, name):
        """Record a passing test."""
        self.passed += 1
        print(f"  [PASS] {name}")
    
    def add_fail(self, name, reason):
        """Record a failing test."""
        self.failed += 1
        self.errors.append((name, reason))
        print(f"  [FAIL] {name}")
        print(f"         Reason: {reason}")
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"RESULTS: {self.passed}/{total} tests passed")
        if self.failed > 0:
            print(f"\nFailed tests:")
            for name, reason in self.errors:
                print(f"  - {name}: {reason}")
        print(f"{'='*60}")
        return self.failed == 0


def run_test(result, name, test_func):
    """Run a single test and record result."""
    try:
        test_func()
        result.add_pass(name)
    except AssertionError as e:
        result.add_fail(name, str(e) if str(e) else "Assertion failed")
    except Exception as e:
        result.add_fail(name, f"Exception: {type(e).__name__}: {e}")


# =============================================================================
# HELPER: Reset RuntimeConfig singleton
# =============================================================================

def reset_runtime_config():
    """Reset RuntimeConfig singleton to defaults."""
    from settings.runtime_config import RuntimeConfig, runtime_config
    # Reset the singleton's initialized flag and reset to defaults
    runtime_config._initialized = False
    runtime_config.__init__()
    return runtime_config


# =============================================================================
# TEST SUITE: Settings (RuntimeConfig)
# =============================================================================

def test_settings(result):
    """Test RuntimeConfig singleton and basic operations."""
    print("\n--- Settings Tests ---")
    
    # Test: RuntimeConfig is singleton
    def test_singleton():
        from settings.runtime_config import RuntimeConfig
        config1 = RuntimeConfig()
        config2 = RuntimeConfig()
        assert config1 is config2, "RuntimeConfig should be singleton"
    run_test(result, "RuntimeConfig is singleton", test_singleton)
    
    # Test: Default race_laps is 20
    def test_default_race_laps():
        rc = reset_runtime_config()
        assert rc.race_laps == 20, f"Expected race_laps=20, got {rc.race_laps}"
    run_test(result, "Default race_laps is 20", test_default_race_laps)
    
    # Test: Default simulation_speed is 1.0
    def test_default_simulation_speed():
        rc = reset_runtime_config()
        assert rc.simulation_speed == 1.0, f"Expected simulation_speed=1.0, got {rc.simulation_speed}"
    run_test(result, "Default simulation_speed is 1.0", test_default_simulation_speed)
    
    # Test: to_dict() returns all expected keys
    def test_to_dict_keys():
        rc = reset_runtime_config()
        data = rc.to_dict()
        expected_keys = [
            "race_laps", "simulation_speed", "tire_deg_rates", "tire_cliff_laps",
            "tire_cliff_penalty", "max_tire_penalty", "fuel_start_penalty",
            "fuel_burn_per_lap", "pit_stop_base_time", "pit_stop_variance",
            "pit_speed_penalty", "pit_window_laps", "pit_chance_after_cliff",
            "pit_chance_near_cliff", "last_laps_no_pit", "tier_modifiers",
            "synergy_modifiers", "lap_variance_base"
        ]
        for key in expected_keys:
            assert key in data, f"Missing key in to_dict(): {key}"
    run_test(result, "to_dict() returns all expected keys", test_to_dict_keys)
    
    # Test: from_dict() applies values correctly
    def test_from_dict():
        rc = reset_runtime_config()
        test_data = {"race_laps": 50, "simulation_speed": 2.0}
        rc.from_dict(test_data)
        assert rc.race_laps == 50, f"Expected race_laps=50, got {rc.race_laps}"
        assert rc.simulation_speed == 2.0, f"Expected simulation_speed=2.0, got {rc.simulation_speed}"
    run_test(result, "from_dict() applies values correctly", test_from_dict)
    
    # Test: reset_to_defaults() works
    def test_reset_to_defaults():
        rc = reset_runtime_config()
        rc.race_laps = 100
        rc.simulation_speed = 5.0
        rc.reset_to_defaults()
        assert rc.race_laps == 20, f"Expected race_laps=20 after reset, got {rc.race_laps}"
        assert rc.simulation_speed == 1.0, f"Expected simulation_speed=1.0 after reset, got {rc.simulation_speed}"
    run_test(result, "reset_to_defaults() works", test_reset_to_defaults)
    
    # Test: Tire settings exist
    def test_tire_settings():
        rc = reset_runtime_config()
        assert "SOFT" in rc.tire_deg_rates, "Missing SOFT in tire_deg_rates"
        assert "MEDIUM" in rc.tire_deg_rates, "Missing MEDIUM in tire_deg_rates"
        assert "HARD" in rc.tire_deg_rates, "Missing HARD in tire_deg_rates"
    run_test(result, "Tire settings exist", test_tire_settings)
    
    # Test: Tier modifiers exist
    def test_tier_modifiers():
        rc = reset_runtime_config()
        for tier in ["S", "A", "B", "C", "D"]:
            assert tier in rc.tier_modifiers, f"Missing tier {tier} in tier_modifiers"
    run_test(result, "Tier modifiers exist", test_tier_modifiers)


# =============================================================================
# TEST SUITE: Presets
# =============================================================================

def test_presets(result):
    """Test preset system."""
    print("\n--- Presets Tests ---")
    
    # Test: 3 built-in presets exist
    def test_builtin_presets_count():
        from settings.presets import BUILTIN_PRESETS
        assert len(BUILTIN_PRESETS) == 3, f"Expected 3 built-in presets, got {len(BUILTIN_PRESETS)}"
    run_test(result, "3 built-in presets exist", test_builtin_presets_count)
    
    # Test: Preset names are correct
    def test_preset_names():
        from settings.presets import BUILTIN_PRESETS
        names = [p["name"] for p in BUILTIN_PRESETS]
        assert "Realistic" in names, "Missing 'Realistic' preset"
        assert "Balanced" in names, "Missing 'Balanced' preset"
        assert "Chaos" in names, "Missing 'Chaos' preset"
    run_test(result, "Preset names are correct", test_preset_names)
    
    # Test: Chaos preset has race_laps = 15
    def test_chaos_race_laps():
        from settings.presets import PRESET_CHAOS
        laps = PRESET_CHAOS["settings"]["race_laps"]
        assert laps == 15, f"Chaos preset should have race_laps=15, got {laps}"
    run_test(result, "Chaos preset has race_laps = 15", test_chaos_race_laps)
    
    # Test: Realistic preset has race_laps = 20
    def test_realistic_race_laps():
        from settings.presets import PRESET_REALISTIC
        laps = PRESET_REALISTIC["settings"]["race_laps"]
        assert laps == 20, f"Realistic preset should have race_laps=20, got {laps}"
    run_test(result, "Realistic preset has race_laps = 20", test_realistic_race_laps)
    
    # Test: PresetManager can get preset by name
    def test_preset_manager_get_by_name():
        from settings.presets import PresetManager
        pm = PresetManager()
        preset = pm.get_preset_by_name("Chaos")
        assert preset is not None, "PresetManager should find 'Chaos' preset"
        assert preset["name"] == "Chaos", "Preset name should be 'Chaos'"
    run_test(result, "PresetManager can get preset by name", test_preset_manager_get_by_name)
    
    # Test: Preset applies to RuntimeConfig
    def test_preset_applies_to_config():
        from settings.presets import PRESET_CHAOS
        rc = reset_runtime_config()
        rc.from_dict(PRESET_CHAOS["settings"])
        assert rc.race_laps == 15, f"After applying Chaos preset, race_laps should be 15, got {rc.race_laps}"
    run_test(result, "Preset applies to RuntimeConfig", test_preset_applies_to_config)
    
    # Test: Each preset has required keys
    def test_preset_structure():
        from settings.presets import BUILTIN_PRESETS
        for preset in BUILTIN_PRESETS:
            assert "name" in preset, f"Preset missing 'name'"
            assert "description" in preset, f"Preset {preset.get('name', '?')} missing 'description'"
            assert "settings" in preset, f"Preset {preset.get('name', '?')} missing 'settings'"
    run_test(result, "Each preset has required keys", test_preset_structure)


# =============================================================================
# TEST SUITE: Persistence
# =============================================================================

def test_persistence(result):
    """Test settings persistence (save/load/delete)."""
    print("\n--- Persistence Tests ---")
    
    # Use temp directory for test files
    temp_dir = tempfile.mkdtemp()
    original_config_file = None
    
    # Test: save() creates file
    def test_save_creates_file():
        from settings.persistence import SettingsPersistence
        nonlocal original_config_file
        original_config_file = SettingsPersistence.CONFIG_FILE
        
        # Use temp file
        test_file = os.path.join(temp_dir, "test_config.json")
        SettingsPersistence.CONFIG_FILE = test_file
        
        rc = reset_runtime_config()
        rc.race_laps = 42
        
        success = SettingsPersistence.save(rc)
        assert success, "save() should return True"
        assert os.path.exists(test_file), "save() should create config file"
    run_test(result, "save() creates file", test_save_creates_file)
    
    # Test: load() restores values
    def test_load_restores_values():
        from settings.persistence import SettingsPersistence
        
        # Save with specific value
        rc = reset_runtime_config()
        rc.race_laps = 77
        rc.simulation_speed = 3.0
        SettingsPersistence.save(rc)
        
        # Reset and load
        rc2 = reset_runtime_config()
        assert rc2.race_laps == 20, "Should start with default"
        
        success = SettingsPersistence.load(rc2)
        assert success, "load() should return True"
        assert rc2.race_laps == 77, f"load() should restore race_laps=77, got {rc2.race_laps}"
        assert rc2.simulation_speed == 3.0, f"load() should restore simulation_speed=3.0, got {rc2.simulation_speed}"
    run_test(result, "load() restores values", test_load_restores_values)
    
    # Test: exists() returns correct value
    def test_exists():
        from settings.persistence import SettingsPersistence
        
        # File should exist from previous test
        assert SettingsPersistence.exists(), "exists() should return True when file exists"
    run_test(result, "exists() returns correct value", test_exists)
    
    # Test: delete() removes file
    def test_delete_removes_file():
        from settings.persistence import SettingsPersistence
        
        # Ensure file exists
        rc = reset_runtime_config()
        SettingsPersistence.save(rc)
        assert SettingsPersistence.exists(), "File should exist before delete"
        
        success = SettingsPersistence.delete()
        assert success, "delete() should return True"
        assert not SettingsPersistence.exists(), "delete() should remove file"
    run_test(result, "delete() removes file", test_delete_removes_file)
    
    # Test: load() returns False when no file
    def test_load_no_file():
        from settings.persistence import SettingsPersistence
        
        # Ensure file doesn't exist
        SettingsPersistence.delete()
        
        rc = reset_runtime_config()
        success = SettingsPersistence.load(rc)
        assert not success, "load() should return False when no file exists"
    run_test(result, "load() returns False when no file", test_load_no_file)
    
    # Cleanup: restore original config file path
    def cleanup():
        from settings.persistence import SettingsPersistence
        if original_config_file:
            SettingsPersistence.CONFIG_FILE = original_config_file
        # Clean up temp directory
        import shutil
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass
    
    cleanup()


# =============================================================================
# TEST SUITE: Race Engine
# =============================================================================

def test_race(result):
    """Test RaceEngine and Car."""
    print("\n--- Race Tests ---")
    
    # Test: RaceEngine initializes with 20 cars
    def test_race_engine_car_count():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        assert len(engine.cars) == 20, f"Expected 20 cars, got {len(engine.cars)}"
    run_test(result, "RaceEngine initializes with 20 cars", test_race_engine_car_count)
    
    # Test: RaceEngine uses runtime_config.race_laps
    def test_race_engine_uses_config_laps():
        rc = reset_runtime_config()
        rc.race_laps = 35
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        assert engine.total_laps == 35, f"Expected total_laps=35, got {engine.total_laps}"
    run_test(result, "RaceEngine uses runtime_config.race_laps", test_race_engine_uses_config_laps)
    
    # Test: RaceEngine uses runtime_config.simulation_speed
    def test_race_engine_uses_config_speed():
        rc = reset_runtime_config()
        rc.simulation_speed = 2.0
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        assert engine.simulation_speed == 2.0, f"Expected simulation_speed=2.0, got {engine.simulation_speed}"
    run_test(result, "RaceEngine uses runtime_config.simulation_speed", test_race_engine_uses_config_speed)
    
    # Test: Car has valid initial state
    def test_car_initial_state():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        car = engine.cars[0]
        
        assert car.lap == 1, f"Car should start on lap 1, got {car.lap}"
        assert car.fuel_load == 1.0, f"Car should start with full fuel, got {car.fuel_load}"
        assert car.tire_age == 0, f"Car should start with fresh tires, got {car.tire_age}"
        assert car.pit_stops == 0, f"Car should start with 0 pit stops, got {car.pit_stops}"
    run_test(result, "Car has valid initial state", test_car_initial_state)
    
    # Test: Car calculates valid pace
    def test_car_pace_calculation():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        import config
        engine = RaceEngine()
        car = engine.cars[0]
        
        pace = car._calculate_current_pace()
        # Pace should be within reasonable bounds (50% to 150% of base)
        min_pace = config.BASE_SPEED * 0.5
        max_pace = config.BASE_SPEED * 1.5
        assert min_pace < pace < max_pace, f"Pace {pace} outside reasonable bounds [{min_pace}, {max_pace}]"
    run_test(result, "Car calculates valid pace", test_car_pace_calculation)
    
    # Test: RaceEngine update() doesn't crash
    def test_race_engine_update():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        engine.start_race()
        
        # Run several updates
        for _ in range(100):
            engine.update()
        
        # Check cars are still valid
        assert len(engine.cars) == 20, "Should still have 20 cars after updates"
        leader = engine.get_leader()
        assert leader is not None, "Should have a leader"
    run_test(result, "RaceEngine update() doesn't crash", test_race_engine_update)
    
    # Test: Cars have different teams
    def test_cars_have_teams():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        
        teams = set(car.team for car in engine.cars)
        assert len(teams) == 10, f"Expected 10 different teams, got {len(teams)}"
    run_test(result, "Cars have different teams", test_cars_have_teams)
    
    # Test: Race finished detection
    def test_race_finished():
        reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        
        assert not engine.is_race_finished(), "Race should not be finished at start"
        
        # Manually set leader past finish
        engine.cars[0].lap = engine.total_laps + 1
        assert engine.is_race_finished(), "Race should be finished when leader completes all laps"
    run_test(result, "Race finished detection", test_race_finished)


# =============================================================================
# TEST SUITE: Integration
# =============================================================================

def test_integration(result):
    """Test integration between components."""
    print("\n--- Integration Tests ---")
    
    # Test: Preset -> RuntimeConfig -> RaceEngine flow
    def test_preset_to_race_engine():
        from settings.presets import PRESET_CHAOS
        rc = reset_runtime_config()
        
        # Apply Chaos preset
        rc.from_dict(PRESET_CHAOS["settings"])
        assert rc.race_laps == 15, "Chaos preset should set race_laps=15"
        
        # Create RaceEngine - should use the config
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        assert engine.total_laps == 15, f"RaceEngine should use race_laps=15 from config, got {engine.total_laps}"
    run_test(result, "Preset -> RuntimeConfig -> RaceEngine flow", test_preset_to_race_engine)
    
    # Test: Save -> Load -> RaceEngine flow
    def test_save_load_race_engine():
        from settings.persistence import SettingsPersistence
        import tempfile
        
        # Use temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        temp_path = temp_file.name
        temp_file.close()
        
        original_file = SettingsPersistence.CONFIG_FILE
        SettingsPersistence.CONFIG_FILE = temp_path
        
        try:
            # Save custom settings
            rc = reset_runtime_config()
            rc.race_laps = 99
            SettingsPersistence.save(rc)
            
            # Reset and load
            rc2 = reset_runtime_config()
            SettingsPersistence.load(rc2)
            
            # Create RaceEngine
            from race.race_engine import RaceEngine
            engine = RaceEngine()
            assert engine.total_laps == 99, f"RaceEngine should use loaded race_laps=99, got {engine.total_laps}"
        finally:
            SettingsPersistence.CONFIG_FILE = original_file
            try:
                os.unlink(temp_path)
            except Exception:
                pass
    run_test(result, "Save -> Load -> RaceEngine flow", test_save_load_race_engine)
    
    # Test: Tier modifiers affect car pace
    def test_tier_modifiers_affect_pace():
        rc = reset_runtime_config()
        from race.race_engine import RaceEngine
        engine = RaceEngine()
        
        # Find S-tier and D-tier cars
        s_tier_car = None
        d_tier_car = None
        for car in engine.cars:
            if car.team_tier == "S" and s_tier_car is None:
                s_tier_car = car
            if car.team_tier == "D" and d_tier_car is None:
                d_tier_car = car
        
        if s_tier_car and d_tier_car:
            # S-tier should generally be faster (higher pace)
            # Note: Other factors affect pace, so we just check they're different
            s_pace = s_tier_car._calculate_current_pace()
            d_pace = d_tier_car._calculate_current_pace()
            # S-tier modifier is 1.04, D-tier is 0.95 - significant difference
            assert s_pace != d_pace, "S-tier and D-tier cars should have different pace"
    run_test(result, "Tier modifiers affect car pace", test_tier_modifiers_affect_pace)
    
    # Test: Changing runtime_config affects new RaceEngine
    def test_config_change_affects_new_engine():
        rc = reset_runtime_config()
        
        from race.race_engine import RaceEngine
        engine1 = RaceEngine()
        laps1 = engine1.total_laps
        
        # Change config
        rc.race_laps = laps1 + 10
        
        # New engine should use new value
        engine2 = RaceEngine()
        assert engine2.total_laps == laps1 + 10, "New RaceEngine should use updated config"
    run_test(result, "Changing runtime_config affects new RaceEngine", test_config_change_affects_new_engine)


# =============================================================================
# TEST SUITE: Pygame Headless
# =============================================================================

def test_pygame(result):
    """Test pygame headless mode."""
    print("\n--- Pygame Headless Tests ---")
    
    # Test: Pygame imports without error
    def test_pygame_import():
        import pygame
        assert pygame is not None, "pygame should import"
    run_test(result, "Pygame imports without error", test_pygame_import)
    
    # Test: Pygame init works in headless mode
    def test_pygame_init():
        import pygame
        pygame.init()
        assert pygame.get_init(), "pygame should initialize"
        pygame.quit()
    run_test(result, "Pygame init works in headless mode", test_pygame_init)
    
    # Test: Can create display in dummy mode
    def test_pygame_display():
        import pygame
        pygame.init()
        try:
            screen = pygame.display.set_mode((100, 100))
            assert screen is not None, "Should create display surface"
        finally:
            pygame.quit()
    run_test(result, "Can create display in dummy mode", test_pygame_display)
    
    # Test: Can create surfaces
    def test_pygame_surface():
        import pygame
        pygame.init()
        try:
            surface = pygame.Surface((50, 50))
            assert surface is not None, "Should create surface"
            assert surface.get_width() == 50, "Surface width should be 50"
            assert surface.get_height() == 50, "Surface height should be 50"
        finally:
            pygame.quit()
    run_test(result, "Can create surfaces", test_pygame_surface)
    
    # Test: Can use fonts
    def test_pygame_font():
        import pygame
        pygame.init()
        try:
            font = pygame.font.Font(None, 24)
            assert font is not None, "Should create font"
            text = font.render("Test", True, (255, 255, 255))
            assert text is not None, "Should render text"
        finally:
            pygame.quit()
    run_test(result, "Can use fonts", test_pygame_font)
    
    # Test: SDL_VIDEODRIVER is dummy
    def test_sdl_driver():
        driver = os.environ.get("SDL_VIDEODRIVER", "")
        assert driver == "dummy", f"SDL_VIDEODRIVER should be 'dummy', got '{driver}'"
    run_test(result, "SDL_VIDEODRIVER is dummy", test_sdl_driver)


# =============================================================================
# MAIN: Run tests
# =============================================================================

def main():
    """Run test suites."""
    print("=" * 60)
    print("F1 Manager - Headless Test Suite")
    print("=" * 60)
    
    # Available test suites
    suites = {
        "settings": test_settings,
        "presets": test_presets,
        "persistence": test_persistence,
        "race": test_race,
        "integration": test_integration,
        "pygame": test_pygame,
    }
    
    # Parse command line args
    args = sys.argv[1:]
    
    if args:
        # Run specific suites
        suites_to_run = []
        for arg in args:
            if arg in suites:
                suites_to_run.append((arg, suites[arg]))
            else:
                print(f"Unknown test suite: {arg}")
                print(f"Available: {', '.join(suites.keys())}")
                sys.exit(1)
    else:
        # Run all suites
        suites_to_run = list(suites.items())
    
    # Run tests
    result = TestResult()
    
    for name, suite_func in suites_to_run:
        try:
            suite_func(result)
        except Exception as e:
            print(f"\n!!! Suite '{name}' crashed: {e}")
            result.add_fail(f"Suite {name}", f"Crashed: {e}")
    
    # Print summary
    all_passed = result.summary()
    
    # Exit code
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
