from local_ssh_config.ssh._constants import (
    SSH_CONFIG_DIR,
    WINDOWS_MULTIPASS_DEFAULT_ID_RSA,
)
from local_ssh_config.utils.ip_addresses import _get_ip_address
from local_ssh_config.utils.jinja._helpers import _create_file_from_template


def _update_ssh_file(virtual_machine_config: dict) -> None:

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

    return virtual_machine_config
