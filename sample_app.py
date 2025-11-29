# sample_app.py

import os 
import json # Flake8 will flag 'json' as unused (F401 error)

class AppConfig:
    """Basic configuration settings."""
    # Flake8 will check for multiple spaces after the '#' (E261/E262 error)
    DEFAULT_TIMEOUT  = 30 
    
    def __init__(self, debug_mode):
        self.debug = debug_mode

# A dictionary with an extra space before the colon (E201 error)
user_data = {
    'name' : 'Alice',
    'status': 'active'
}

# Function to simulate processing the config
def process_config(config):
    if config.debug:
        print("Debug mode enabled. Timeout:", config.DEFAULT_TIMEOUT)
    return True

# Create an instance
config_instance = AppConfig(debug_mode=True)

# Process it
if process_config(config_instance):
    print("Configuration processed successfully.")
    