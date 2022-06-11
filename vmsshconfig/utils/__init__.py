from .hyper_v import get_hyper_v_ip_address

VALID_SOURCES = {"hyper-v"}


def _get_ip_address(source_dict: dict(str)) -> str:

    if source_dict["source"] == "hyper-v":
        return get_hyper_v_ip_address(physical_address=source_dict["physical_address"])
    else:
        raise ValueError(
            f"""invalid or missing 'source' key in 'hostname' dict.
                Expect value in {str(VALID_SOURCES)}.
                Got {str(source_dict)}."""
        )
