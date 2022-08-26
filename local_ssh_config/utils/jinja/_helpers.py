from pathlib import Path

from local_ssh_config.utils.jinja._environment import JINJA_ENVIRONMENT


def _create_file_from_template(
    template_name: str,
    directory: Path,
    filename: Path = None,
    variables: dict = {},
) -> None:
    """
    Write new file to disk, within `directory`,
    by rendering the jinja template `template_name`
    """
    if filename is None:
        config_filename = template_name.replace(".j2", "")  # remove extension
        filename = Path(config_filename)

    template = JINJA_ENVIRONMENT.get_template(f"{template_name}")

    output = template.render(variables)

    with open(f"{directory}/{filename}", "w") as f:
        f.write(output)
