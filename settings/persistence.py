"""
SettingsPersistence - Save/load settings to user_config.json
"""
import json
import os


class SettingsPersistence:
    """Handles saving and loading settings to/from disk."""
    
    CONFIG_FILE = "user_config.json"
    
    @classmethod
    def save(cls, runtime_config):
        """
        Save current settings to user_config.json.
        
        Args:
            runtime_config: RuntimeConfig instance to save
        """
        try:
            data = {
                "version": 1,
                "settings": runtime_config.to_dict(),
            }
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except IOError as e:
            print(f"Failed to save settings: {e}")
            return False
    
    @classmethod
    def load(cls, runtime_config):
        """
        Load settings from user_config.json into runtime_config.
        
        Args:
            runtime_config: RuntimeConfig instance to load into
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        if not os.path.exists(cls.CONFIG_FILE):
            return False
        
        try:
            with open(cls.CONFIG_FILE, 'r') as f:
                data = json.load(f)
            
            # Check version for future compatibility
            version = data.get("version", 1)
            if version > 1:
                print(f"Warning: Config file version {version} may not be fully compatible")
            
            settings = data.get("settings", {})
            runtime_config.from_dict(settings)
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"Failed to load settings: {e}")
            return False
    
    @classmethod
    def exists(cls):
        """Check if saved settings file exists."""
        return os.path.exists(cls.CONFIG_FILE)
    
    @classmethod
    def delete(cls):
        """Delete saved settings file."""
        if os.path.exists(cls.CONFIG_FILE):
            try:
                os.remove(cls.CONFIG_FILE)
                return True
            except IOError:
                return False
        return True
