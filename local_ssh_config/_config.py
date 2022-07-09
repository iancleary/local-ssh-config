import json
from pathlib import Path

from local_ssh_config._constants import GLOBAL_CONFIG_FILE


def _load_config(config_file: Path = GLOBAL_CONFIG_FILE) -> dict:
    """
    Loads config from global scope, if they exist.
    """
    file_config = {}

    if config_file.exists():
        f = open(config_file)
        file_config = json.load(f)
        f.close()

    return file_config
