from pathlib import Path

GLOBAL_CONFIG_DIR = Path.home() / Path(".config/local-ssh-config")
GLOBAL_CONFIG_PATH = Path(GLOBAL_CONFIG_DIR)
GLOBAL_CONFIG_FILE = Path(f"{GLOBAL_CONFIG_DIR}/settings.json")

WINDOWS_MULTIPASS_DEFAULT_ID_RSA = "C:/Windows/System32/config/systemprofile/AppData/Roaming/multipassd/ssh-keys/id_rsa"
