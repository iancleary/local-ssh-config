from pathlib import Path
from typing import Optional

import typer

from local_ssh_config._config import _load_config
from local_ssh_config._constants import (
    GLOBAL_CONFIG_FILE,
    SSH_CONFIG_DIR,
    SSH_CONFIG_FILE,
    SSH_CONFIG_INCLUDE_DIRECTIVE,
    SSH_DIR,
    WINDOWS_MULTIPASS_DEFAULT_ID_RSA,
)
from local_ssh_config._echos import (
    _append_echo,
    _create_dir_echo,
    _create_file_echo,
    _create_local_ssh_config_echo,
)
from local_ssh_config._jinja import _create_jinja_environment
from local_ssh_config._version import _version_callback
from local_ssh_config.utils import _get_ip_address

app = typer.Typer()

JINJA_ENVIRONMENT = _create_jinja_environment()


def _create_output(
    template_name: str,
    variables: dict = {},
    filename: Path = None,
    directory: Path = SSH_CONFIG_DIR,
) -> None:
    """
    Write new file to disk, within `new_directory`,
    by rendering the jinja template `template_name`
    """
    if filename is None:
        filename = Path(template_name)

    template = JINJA_ENVIRONMENT.get_template(f"{template_name}")

    # handle cases of where to get hostname (hyper-v, etc.)
    if "hostname" in variables.keys() and isinstance(variables["hostname"], dict):
        if "source" in variables["hostname"].keys():
            if variables["hostname"]["source"] == "multipass":
                # and platform == windows
                IS_MULTIPASS = True
            else:
                IS_MULTIPASS = False

        variables["hostname"] = _get_ip_address(source_dict=variables["hostname"])

        if IS_MULTIPASS:
            if "identity_file" not in variables.keys():
                # use default identity file
                # https://github.com/canonical/multipass/issues/913#issuecomment-697235248
                variables["identity_file"] = WINDOWS_MULTIPASS_DEFAULT_ID_RSA

    output = template.render(variables)

    with open(f"{directory}/{filename}", "w") as f:
        f.write(output)


@app.command()
def main(
    file: str = typer.Option(
        GLOBAL_CONFIG_FILE,
        "--file",
        "-f",
        help="The JSON file containing the virtual machine configuration",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """
    Creates an `~/.ssh/config.d/` directory, checks to see
    if your ~/.ssh/config file include all files in that directory,
    and then creates config files for each virtual machine
    specified in your `~/.config/vm-ip-ssh-config/settings.json` file.

    See https://github.com/iancleary/local-ssh-config for more information.
    """

    # create ~/.ssh/config.d/ directory
    if not SSH_CONFIG_DIR.is_dir():
        SSH_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        _create_dir_echo(directory=SSH_CONFIG_DIR)

    # create ~/.ssh/config file or appended to it, as needed
    if not SSH_CONFIG_FILE.is_file():
        # create file with SSH_CONFIG_INCLUDE_DIRECTIVE as sole line
        _create_output(directory=SSH_DIR, template_name="config.j2")
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

    # load and merge config
    config = _load_config(config_file=Path(file))

    # accomodate single virtual machine
    if isinstance(config, dict):
        virtual_machine_configs = [config]
    else:
        virtual_machine_configs = config
    # typer.echo(str(virtual_machine_configs)) # debug

    # loop through virtual machines and create ~/.ssh/config.d/ files
    for virtual_machine_config in virtual_machine_configs:
        typer.echo(virtual_machine_config)  # debug
        _create_output(
            template_name="config.d/config.j2",
            variables=virtual_machine_config,
            directory=SSH_CONFIG_DIR,
            filename=virtual_machine_config["host"],
        )

    # Echo final status to user
    _create_local_ssh_config_echo(
        hostnames=[SSH_CONFIG_DIR / Path(x["host"]) for x in virtual_machine_configs],
    )
