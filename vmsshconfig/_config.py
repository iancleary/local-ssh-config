import json

from vmsshconfig._constants import (
    DEFAULT_COMPONENTS_DIR,
    DEFAULT_FILE_EXTENSION,
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


def _merge_config(
    file_config: dict, directory: str = None, extension: str = None
) -> dict:
    """
    Merge config values, with command-line values overwriting local values,
    and local values overwriting global ones.
    """

    config = {}

    # This should confirm keys match API
    if "global" in file_config.keys():
        config.update(file_config["global"])

    # This should confirm keys match API
    if "local" in file_config.keys():
        config.update(file_config["local"])

    # Merge directory config and parameter
    if directory is not None:
        config.update({"directory": directory})
    elif "directory" in config.keys():
        # directory configured via global or local config file
        pass
    else:
        # no config nor option specified, use default
        config.update({"directory": DEFAULT_COMPONENTS_DIR})

    # Merge directory config and parameter
    if extension is not None:
        config.update({"extension": extension})
    elif "extension" in config.keys():
        # extension configured via global or local config file
        pass
    else:
        # no config nor option specified, use default
        config.update({"extension": DEFAULT_FILE_EXTENSION})

    # DEBUG
    # with open("./.new-component-merged-config.json", "w") as outfile:
    #     json.dump(config, outfile, indent=4)

    return config
