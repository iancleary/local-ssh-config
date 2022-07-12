from pathlib import Path
from typing import Optional

import typer

from local_ssh_config._config import _load_config
from local_ssh_config._constants import GLOBAL_CONFIG_FILE
from local_ssh_config._echos import _create_local_ssh_config_echo, _welcome_echo
from local_ssh_config._version import _version_callback
from local_ssh_config.hosts._update import _prompt_to_update_hosts_file
from local_ssh_config.ssh._constants import SSH_CONFIG_DIR
from local_ssh_config.ssh._update import _update_ssh_file
from local_ssh_config.ssh.structure import create_ssh_config_dir_if_needed

app = typer.Typer()


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
    f"""
    Creates an `~/.ssh/config.d/` directory, checks to see
    if your ~/.ssh/config file include all files in that directory,
    and then creates config files for each virtual machine
    specified in your `~/.config/{GLOBAL_CONFIG_FILE}` file.

    See https://github.com/iancleary/local-ssh-config for more information.
    """

    _welcome_echo()

    create_ssh_config_dir_if_needed()

    # load config
    (NEW_CONFIG_FILE_CREATED, config) = _load_config(config_file=Path(file))

    if NEW_CONFIG_FILE_CREATED:
        typer.echo(f"New empty config file created!\n{GLOBAL_CONFIG_FILE}")

    # accomodate single virtual machine
    if isinstance(config, dict):
        virtual_machine_configs = [config]
    else:
        virtual_machine_configs = config
    # typer.echo(str(virtual_machine_configs)) # debug

    # loop through virtual machines and create ~/.ssh/config.d/ files
    updated_virtual_machine_configs = []
    for virtual_machine_config in virtual_machine_configs:
        typer.echo(f"Config: {virtual_machine_config}")  # debug

        virtual_machine_config = _update_ssh_file(
            virtual_machine_config=virtual_machine_config
        )

        updated_virtual_machine_configs.append(virtual_machine_config)

    _prompt_to_update_hosts_file(
        virtual_machine_configs=updated_virtual_machine_configs
    )

    # Echo final status to user
    _create_local_ssh_config_echo(
        hostnames=[
            SSH_CONFIG_DIR / Path(x["host"])
            for x in virtual_machine_configs
            if "host" in x.keys()
        ],
    )
