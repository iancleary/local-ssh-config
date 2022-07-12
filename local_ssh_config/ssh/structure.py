from local_ssh_config._echos import _append_echo, _create_dir_echo, _create_file_echo
from local_ssh_config.ssh._constants import (
    SSH_CONFIG_DIR,
    SSH_CONFIG_FILE,
    SSH_CONFIG_INCLUDE_DIRECTIVE,
    SSH_DIR,
)
from local_ssh_config.utils.jinja._helpers import _create_file_from_template


def create_ssh_config_dir_if_needed() -> None:
    # create ~/.ssh/config.d/ directory
    if not SSH_CONFIG_DIR.is_dir():
        SSH_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        _create_dir_echo(directory=SSH_CONFIG_DIR)


def ensure_ssh_config_file_has_include_directive() -> None:
    # create ~/.ssh/config file or appended to it, as needed
    if not SSH_CONFIG_FILE.is_file():
        # create file with SSH_CONFIG_INCLUDE_DIRECTIVE as sole line
        _create_file_from_template(directory=SSH_DIR, template_name="config.j2")
        _create_file_echo(file=SSH_CONFIG_FILE)
    else:
        # check if SSH_CONFIG_INCLUDE_DIRECTIVE is in SSH_CONFIG_FILE
        ssh_config_include_directive_found = False
        with SSH_CONFIG_FILE.open("r", encoding="utf-8") as ssh_config_file:
            lines = [x for x in ssh_config_file]
            # typer.echo(lines) # debug

            for line in lines:
                if SSH_CONFIG_INCLUDE_DIRECTIVE in line:
                    ssh_config_include_directive_found = True
        # typer.echo(str(ssh_config_include_directive_found)) # debug

        # append SSH_CONFIG_INCLUDE_DIRECTIVE to SSH_CONFIG_FILE
        if ssh_config_include_directive_found == False:
            with SSH_CONFIG_FILE.open("a", encoding="utf-8") as ssh_config_file:
                ssh_config_file.write(SSH_CONFIG_INCLUDE_DIRECTIVE)
            _append_echo(file=SSH_CONFIG_FILE, text=SSH_CONFIG_INCLUDE_DIRECTIVE)
