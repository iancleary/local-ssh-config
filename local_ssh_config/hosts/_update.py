import shutil
from pathlib import Path
from typing import List

import typer

from local_ssh_config.hosts._constants import WINDOWS_HOST_FILE, WINDOWS_HOST_FOLDER


def _prompt_to_update_hosts_file(virtual_machine_configs) -> None:
    # extract IP address and hostname from each o

    typer.echo("")
    message = "✨ If you'd like to update your hosts file ✨"

    thank_you_message = typer.style(message, typer.colors.BRIGHT_BLACK)
    typer.echo(thank_you_message)
    typer.echo(WINDOWS_HOST_FILE)
    typer.echo("")

    lines_to_add = []
    for config in virtual_machine_configs:
        ip_address = config["hostname"]
        host = config["host"]

        # add line
        new_line = f"{ip_address} {host}"
        lines_to_add.append(f"{new_line}\n")
        typer.echo(new_line)

    # typer.echo(lines_to_add)
    # shutil.copy(
    #     WINDOWS_HOST_FILE, Path(WINDOWS_HOST_FOLDER) / "hosts.local_ssh_config.backup"
    # )

    # f = open(WINDOWS_HOST_FILE, "w")
    # f.writelines(lines_to_add)
    # f.close()

    # typer.echo("")
