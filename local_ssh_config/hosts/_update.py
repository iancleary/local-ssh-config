from typing import List

from local_ssh_config.hosts._constants import WINDOWS_HOST_FILE


def _update_host_file(virtual_machine_configs: List(dict)) -> None:
    # extract IP address and hostname from each o

    lines_to_add = []
    for config in virtual_machine_configs:
        ip_address = config["hostname"]
        host = config["host"]

        # add line
        lines_to_add.append(f"{ip_address} {host}\n")

    new_content = ""
    for line in lines_to_add:
        new_content = new_content + line

    with open(WINDOWS_HOST_FILE, "w+") as f:
        f.write(new_content)

    pass
