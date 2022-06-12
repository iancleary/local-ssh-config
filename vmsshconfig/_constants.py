from pathlib import Path

import vmsshconfig

SSH_DIR = Path.home() / ".ssh/"
SSH_CONFIG_DIR = Path.home() / ".ssh/config.d/"
SSH_CONFIG_FILE = Path.home() / ".ssh/config"

SSH_CONFIG_INCLUDE_DIRECTIVE = "Include config.d/*"

INSTALLED_LOCATION = vmsshconfig.__file__
TEMPLATES_DIR = INSTALLED_LOCATION.replace("__init__.py", "")
TEMPLATES_PATH = Path(TEMPLATES_DIR) / "templates"

GLOBAL_CONFIG_DIR = Path.home() / Path(".config/vm-ssh-config")
GLOBAL_CONFIG_PATH = Path(GLOBAL_CONFIG_DIR)
GLOBAL_CONFIG_FILE = Path(f"{GLOBAL_CONFIG_DIR}/settings.json")
