import yaml
import os

# Path to YAML config file
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "backend", "data", "config.yaml")

# Load YAML configuration
def load_config():
    """Loads the configuration file and returns the settings as a dictionary."""
    with open(CONFIG_FILE, "r") as file:
        return yaml.safe_load(file) or {}

# Get SMTP settings, prioritizing user settings over defaults
def get_smtp_settings():
    """Fetch SMTP settings: Use user-defined values if available; otherwise, fallback to defaults."""
    config = load_config()
    default_smtp = config["smtp"]["default"]
    user_smtp = config["smtp"].get("user", {})

    # Merge user settings with defaults (fallback to defaults if user settings are empty)
    return {
        "server": user_smtp.get("server") or default_smtp["server"],
        "port": user_smtp.get("port") or default_smtp["port"],
        "encryption": user_smtp.get("encryption") or default_smtp["encryption"]
    }

# Get Port Forwarding settings, prioritizing user settings over defaults
# def get_port_forwarding_settings():
#     """Fetch Port Forwarding settings: Use user-defined values if available; otherwise, fallback to defaults."""
#     config = load_config()
#     default_pf = config["port_forwarding"]["default"]
#     user_pf = config["port_forwarding"].get("user", {})

#     # Merge user settings with defaults (fallback to defaults if user settings are empty)
#     return {
#         "enabled": user_pf.get("enabled") if user_pf.get("enabled") is not None else default_pf["enabled"],
#         "service": user_pf.get("service") or default_pf["service"],
#         "url": user_pf.get("url") or default_pf["url"]
#     }

# Save user settings inside the `user` section of `config.yaml`
def save_user_settings(new_settings):
    """Updates only the user settings inside `config.yaml` without modifying defaults."""
    config = load_config()

    # Update only the "user" section
    if "smtp" in new_settings:
        config["smtp"]["user"] = new_settings["smtp"]
    
    # if "port_forwarding" in new_settings:
    #     config["port_forwarding"]["user"] = new_settings["port_forwarding"]

    # Save updated settings back to `config.yaml`
    with open(CONFIG_FILE, "w") as file:
        yaml.dump(config, file, default_flow_style=False)

