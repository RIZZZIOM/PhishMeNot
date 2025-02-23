import yaml
import os

# Path to the YAML config file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "backend", "data", "config.yaml")

# Load YAML configuration
def load_config():
    """Loads the configuration file and returns the settings as a dictionary."""
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file)

# Get default SMTP settings
def get_default_smtp():
    """Fetches the default SMTP settings from config.yaml."""
    config = load_config()
    return config["smtp"]

# Save updated settings back to YAML file
def save_config(new_config):
    """Updates the YAML config file with new settings."""
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(new_config, file, default_flow_style=False)


