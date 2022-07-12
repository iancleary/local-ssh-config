from pathlib import Path

import typer

import local_ssh_config.utils.ip_addresses._powershell as ps


def get_multipass_ip_address(name: str) -> str:
    # PowerShell command to run
    interface_command = "multipass list"
    info = ps.run(interface_command)
    if info.returncode != 0:
        typer.echo(
            "Multipass: Powershell (multipass list: An error occured: %s", info.stderr
        )
    else:
        typer.echo(
            "Multipass-V: Powershell (multipass list): Interface command executed successfully!"
        )

        print("-------------------------")

        # convert b"" to string
        output = info.stdout.decode("utf-8")

        # print(type(output))
        # print(output)

        lines = iter(output.splitlines())

        # Find last line that contains physical address
        # See https://github.com/iancleary/local-ssh-config/issues/3 for more details
        found = False
        for line in lines:
            if name in line:
                ip_line = line
                found = True
                # break # uncomment to find first line that contains physical address

        if not found:
            typer.echo(f"{name} not found in \n\n{str(info.stdout)}\n\n")

        ip_line_cleaned = [x for x in ip_line.split(" ") if x != ""]
        ip_address = ip_line_cleaned[2]

        return ip_address
