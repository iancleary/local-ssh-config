import json
from pathlib import Path

from local_ssh_config._constants import GLOBAL_CONFIG_FILE


def _load_config(config_file: Path = GLOBAL_CONFIG_FILE) -> dict:
    """
    Loads config from global scope, if they exist.
    """
    file_config = {}

    NEW_CONFIG_FILE_CREATED = False

    if config_file.exists():
        f = open(config_file)
        file_config = json.load(f)
        f.close()
    else:
        NEW_CONFIG_FILE_CREATED = True
        with open(config_file, "w") as f:
            initial_config = {}
            json.dump(initial_config, f)
            f.close()

    return (NEW_CONFIG_FILE_CREATED, file_config)
