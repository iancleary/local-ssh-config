from pathlib import Path

import typer


def _create_vmsshconfig_echo(
    component_name: str, path_to_component_directory: Path
) -> None:
    """
    Echos the newly created component and directory.
    """

    typer.echo("")
    message_start = "✨ Creating a new "
    component = typer.style(component_name, fg=typer.colors.YELLOW, bold=True)
    message_end = " Component ✨!"
    message = message_start + component + message_end
    typer.echo(message)
    typer.echo("")

    new_directory_path = typer.style(
        path_to_component_directory, fg=typer.colors.BLUE, bold=True
    )
    message = "Directory:".ljust(11) + new_directory_path
    typer.echo(message)

    styled_component = "styled 💅"
    component_type = typer.style(styled_component, typer.colors.BLUE, bold=True)
    message = "Type:".ljust(11) + component_type
    typer.echo(message)

    created_messages = [
        "Directory created.",
        f"{component_name} component created and saved to disk.",
        "Index file created and saved to disk.",
    ]

    typer.echo("")
    for created_message in created_messages:
        typer.echo("✅ " + created_message)
    typer.echo("")

    component_type = typer.style(component_name, typer.colors.GREEN, bold=True)
    message = component_type + " component created! 🚀"
    typer.echo(message)

    message = "Thank you for using new-component."

    thank_you_message = typer.style(message, typer.colors.BRIGHT_BLACK)
    typer.echo(thank_you_message)
    typer.echo("")


def _create_components_dir_echo(components_directory: Path) -> None:
    message = f"Warning: created the {components_directory} directory."
    styled_message = typer.style(message, fg=typer.colors.YELLOW, bold=True)
    typer.echo(styled_message)


def _overwrite_component_echo(components_directory: Path, component_name: str) -> None:
    warning_message = (
        f"{component_name} component already exists in ./{components_directory}/."
    )
    styled_warning = typer.style(warning_message, typer.colors.YELLOW, bold=True)
    typer.echo(styled_warning)
