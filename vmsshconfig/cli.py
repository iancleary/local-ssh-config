from pathlib import Path
from typing import Optional

import typer

from vmsshconfig._config import _load_config, _merge_config
from vmsshconfig._constants import SSH_CONFIG_DIR
from vmsshconfig._confirms import (
    _create_components_dir_confirm,
    _overwrite_component_confirm,
)
from vmsshconfig._echos import (
    _create_components_dir_echo,
    _create_vmsshconfig_echo,
    _overwrite_component_echo,
)
from vmsshconfig._jinja import _create_jinja_environment
from vmsshconfig._utils import _create_directory
from vmsshconfig._version import _version_callback

app = typer.Typer()

JINJA_ENVIRONMENT = _create_jinja_environment()


def _create_output(
    new_directory: Path,
    template_name: str,
    variables: dict,
    filename: str = None,
) -> None:
    """
    Write new file to disk, within `new_directory`,
    by rendering the jinja template `template_name`
    """
    if filename is None:
        filename = template_name

    template = JINJA_ENVIRONMENT.get_template(f"{template_name}.j2")
    output = template.render(variables)

    with open(f"{SSH_CONFIG_DIR}/{filename}", "w") as f:
        f.write(output)


@app.command()
def main(
    name: str = typer.Argument(
        ...,  # Required to give name, as in `new-component ContactForm`
        help="Name of component to create.",
    ),
    directory: str = typer.Option(
        None,
        "--directory",
        "-d",
        help="The directory in which to create the component.",
    ),
    extension: str = typer.Option(
        None,
        "--extension",
        "-e",
        help="The file extension for the created component files.",
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
    Creates an new component directory in a React project,
    with opinionated defaults for styled-components.

    For information on styled-components, see https://styled-components.com/.

    For online documentation, see https://new-component.iancleary.me/.
    """

    # load and merge config
    file_config = _load_config()
    config = _merge_config(
        file_config=file_config, directory=directory, extension=extension
    )

    # update variables form config
    directory = config["directory"]
    extension = config["extension"]

    # path to components directory
    components_directory = Path(directory)

    # Prompt user to create components directory, if it doesn't exist
    if components_directory.exists() is False:
        _create_components_dir_confirm(components_directory=components_directory)
        _create_directory(directory=components_directory)
        _create_components_dir_echo(components_directory=components_directory)

    # Create Paths to the new Component directory
    vmsshconfig_directory = components_directory / name
    full_path_to_component_directory = Path.cwd() / vmsshconfig_directory

    # Allow user to abort if component already exists, else create component directory
    if full_path_to_component_directory.exists() is True:
        _overwrite_component_echo(
            components_directory=vmsshconfig_directory, component_name=name
        )
        _overwrite_component_confirm(component_name=name)

    else:
        _create_directory(directory=full_path_to_component_directory)

    # Setup Jinja Variables used in template render
    variables = {"ComponentName": name}

    # Render component files in your components directory
    _create_output(
        new_directory=full_path_to_component_directory,
        template_name="index",
        variables=variables,
        extension=extension,
    )
    _create_output(
        new_directory=full_path_to_component_directory,
        template_name="component",
        variables=variables,
        extension=extension,
        filename=f"{name}",
    )

    # Echo final status to user
    _create_vmsshconfig_echo(
        component_name=name,
        path_to_component_directory=vmsshconfig_directory,
    )
