from pathlib import Path

import local_ssh_config

INSTALLED_LOCATION = local_ssh_config.__file__
TEMPLATES_DIR = INSTALLED_LOCATION.replace("__init__.py", "")
TEMPLATES_PATH = Path(TEMPLATES_DIR) / "templates"
