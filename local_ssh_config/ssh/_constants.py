import os
from pathlib import Path

SSH_DIR = Path.home() / ".ssh/"
SSH_CONFIG_DIR = Path.home() / ".ssh/config.d/"
SSH_CONFIG_FILE = Path.home() / ".ssh/config"

SSH_CONFIG_INCLUDE_DIRECTIVE = "Include config.d/*"

_PROGRAM_DATA = Path(os.getenv("PROGRAMDATA", "C:\\ProgramData"))

WINDOWS_MULTIPASS_DEFAULT_ID_RSA = Path(
    _PROGRAM_DATA / Path("Multipass/data/ssh-keys/id_rsa")
).as_posix()
