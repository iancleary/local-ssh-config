import json

from vmsshconfig._constants import (
    GLOBAL_CONFIG_FILE,
)


def _load_config() -> dict:
    """
    Loads config from global scope, if they exist.
    """
    file_config = {}

    if GLOBAL_CONFIG_FILE.exists():
        f = open(GLOBAL_CONFIG_FILE)
        file_config["global"] = json.load(f)
        f.close()

    return file_config
