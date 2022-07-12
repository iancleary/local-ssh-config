from pathlib import Path

SSH_DIR = Path.home() / ".ssh/"
SSH_CONFIG_DIR = Path.home() / ".ssh/config.d/"
SSH_CONFIG_FILE = Path.home() / ".ssh/config"

SSH_CONFIG_INCLUDE_DIRECTIVE = "Include config.d/*"

GLOBAL_CONFIG_DIR = Path.home() / Path(".config/local-ssh-config")
GLOBAL_CONFIG_PATH = Path(GLOBAL_CONFIG_DIR)
GLOBAL_CONFIG_FILE = Path(f"{GLOBAL_CONFIG_DIR}/settings.json")

WINDOWS_MULTIPASS_DEFAULT_ID_RSA = "C:/Windows/System32/config/systemprofile/AppData/Roaming/multipassd/ssh-keys/id_rsa"
WINDOWS_HOST_FILE = "C:/Windows/System32/drivers/etc/hosts"
