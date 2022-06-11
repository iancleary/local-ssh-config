from jinja2 import Environment, FileSystemLoader

from vmsshconfig._constants import TEMPLATES_PATH


def _create_jinja_environment() -> Environment:
    """
    Creates the Jinja Environment with the path to the package's templates
    """
    # typer.echo(TEMPLATES_PATH)
    loader = FileSystemLoader(TEMPLATES_PATH)
    return Environment(loader=loader)
