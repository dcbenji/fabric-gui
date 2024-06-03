import os
import json

# Default configuration values
DEFAULT_CONFIG = {
    "api_key": "",
    "api_endpoint": "https://api.example.com",
    "default_model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 100,
    "theme": "light"
}

# Configuration file path
CONFIG_FILE = "config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
    else:
        config = DEFAULT_CONFIG
        save_config(config)
    return config

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=2)

def get_api_key():
    config = load_config()
    return config["api_key"]

def set_api_key(api_key):
    config = load_config()
    config["api_key"] = api_key
    save_config(config)

def get_default_model():
    config = load_config()
    return config["default_model"]

def set_default_model(default_model):
    config = load_config()
    config["default_model"] = default_model
    save_config(config)

def get_temperature():
    config = load_config()
    return config["temperature"]

def set_temperature(temperature):
    config = load_config()
    config["temperature"] = temperature
    save_config(config)

def get_max_tokens():
    config = load_config()
    return config["max_tokens"]

def set_max_tokens(max_tokens):
    config = load_config()
    config["max_tokens"] = max_tokens
    save_config(config)

def get_theme():
    config = load_config()
    return config["theme"]

def set_theme(theme):
    config = load_config()
    config["theme"] = theme
    save_config(config)