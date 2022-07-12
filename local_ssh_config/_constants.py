from pathlib import Path

GLOBAL_CONFIG_DIR = Path.home() / Path(".config/local-ssh-config")
GLOBAL_CONFIG_PATH = Path(GLOBAL_CONFIG_DIR)
GLOBAL_CONFIG_FILE = Path(f"{GLOBAL_CONFIG_DIR}/settings.json")
