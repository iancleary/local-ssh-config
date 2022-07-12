from pathlib import Path

SSH_DIR = Path.home() / ".ssh/"
SSH_CONFIG_DIR = Path.home() / ".ssh/config.d/"
SSH_CONFIG_FILE = Path.home() / ".ssh/config"

SSH_CONFIG_INCLUDE_DIRECTIVE = "Include config.d/*"

WINDOWS_MULTIPASS_DEFAULT_ID_RSA = "C:/Windows/System32/config/systemprofile/AppData/Roaming/multipassd/ssh-keys/id_rsa"
