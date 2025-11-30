# sample_app.py

class AppConfig:
    """Basic configuration settings."""

    DEFAULT_TIMEOUT = 30

    def __init__(self, debug_mode):
        self.debug = debug_mode


# A dictionary with proper spacing around colons
user_data = {
    'name': 'Alice',
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

