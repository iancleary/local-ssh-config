from pathlib import Path

import typer


def _create_components_dir_confirm(components_directory: Path) -> None:
    styled_component_directory = typer.style(
        f"./{components_directory}/", typer.colors.YELLOW, bold=True
    )
    confirm_message = (
        styled_component_directory + " doesn't exist. Do you want to create it?"
    )
    typer.confirm(confirm_message, abort=True)


def _overwrite_component_confirm(component_name: str) -> None:
    styled_component = typer.style(f"{component_name}", typer.colors.YELLOW, bold=True)
    confirm_message = (
        "Are you sure you want to overwrite your " + styled_component + " component?"
    )
    typer.confirm(confirm_message, abort=True)
