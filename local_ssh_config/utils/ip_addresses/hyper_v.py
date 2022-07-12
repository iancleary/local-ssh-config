from pathlib import Path

import typer

import local_ssh_config.utils.ip_addresses._powershell as ps


def get_hyper_v_ip_address(physical_address: str) -> str:
    # PowerShell command to run
    interface_command = "arp -a"
    info = ps.run(interface_command)
    if info.returncode != 0:
        typer.echo("Hyper-V: Powershell (arp -a): An error occured: %s", info.stderr)
    else:
        typer.echo(
            "Hyper-V: Powershell (arp -a): Interface command executed successfully!"
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
            if physical_address in line:
                ip_line = line
                found = True
                # break # uncomment to find first line that contains physical address

        if not found:
            typer.echo(f"{physical_address} not found in \n\n{str(info.stdout)}\n\n")

        ip_line_cleaned = [x for x in ip_line.split(" ") if x != ""]
        ip_address = ip_line_cleaned[0]

        return ip_address
