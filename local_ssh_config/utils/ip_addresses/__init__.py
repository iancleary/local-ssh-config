from local_ssh_config.utils.ip_addresses.hyper_v import get_hyper_v_ip_address
from local_ssh_config.utils.ip_addresses.multipass import get_multipass_ip_address

VALID_SOURCES = {"hyper-v"}


def _get_ip_address(source_dict: dict[str]) -> str:

    if source_dict["source"] == "hyper-v":
        return get_hyper_v_ip_address(physical_address=source_dict["physical_address"])
    elif source_dict["source"] == "multipass":
        return get_multipass_ip_address(name=source_dict["name"])
    else:
        raise ValueError(
            f"""invalid or missing 'source' key in 'hostname' dict.
                Expect value in {str(VALID_SOURCES)}.
                Got {str(source_dict)}."""
        )
