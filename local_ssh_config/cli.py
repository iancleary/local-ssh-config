from pathlib import Path
from typing import Optional

import typer

from local_ssh_config._config import _load_config
from local_ssh_config._constants import (
    GLOBAL_CONFIG_FILE,
    SSH_CONFIG_DIR,
    WINDOWS_MULTIPASS_DEFAULT_ID_RSA,
)
from local_ssh_config._echos import _create_local_ssh_config_echo, _welcome_echo
from local_ssh_config._version import _version_callback
from local_ssh_config.ip_addresses import _get_ip_address
from local_ssh_config.ssh.structure import create_ssh_config_dir_if_needed
from local_ssh_config.utils.jinja._helpers import _create_file_from_template

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
    """
    Creates an `~/.ssh/config.d/` directory, checks to see
    if your ~/.ssh/config file include all files in that directory,
    and then creates config files for each virtual machine
    specified in your `~/.config/vm-ip-ssh-config/settings.json` file.

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
    for virtual_machine_config in virtual_machine_configs:
        typer.echo(f"Config: {virtual_machine_config}")  # debug

        # handle cases of where to get hostname (hyper-v, etc.)
        if "hostname" in virtual_machine_config.keys() and isinstance(
            virtual_machine_config["hostname"], dict
        ):
            if "source" in virtual_machine_config["hostname"].keys():
                if virtual_machine_config["hostname"]["source"] == "multipass":
                    # and platform == windows
                    IS_MULTIPASS = True
                else:
                    IS_MULTIPASS = False

            virtual_machine_config["hostname"] = _get_ip_address(
                source_dict=virtual_machine_config["hostname"]
            )

            if IS_MULTIPASS:
                if "identity_file" not in virtual_machine_config.keys():
                    # use default identity file
                    # https://github.com/canonical/multipass/issues/913#issuecomment-697235248
                    virtual_machine_config[
                        "identity_file"
                    ] = WINDOWS_MULTIPASS_DEFAULT_ID_RSA

            _create_file_from_template(
                template_name="config.d/config.j2",
                variables=virtual_machine_config,
                directory=SSH_CONFIG_DIR,
                filename=virtual_machine_config["host"],
            )

    # Echo final status to user
    _create_local_ssh_config_echo(
        hostnames=[
            SSH_CONFIG_DIR / Path(x["host"])
            for x in virtual_machine_configs
            if "host" in x.keys()
        ],
    )
