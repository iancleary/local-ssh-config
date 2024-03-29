from pathlib import Path

import typer
from typer.testing import CliRunner

from local_ssh_config import __app_name__, __version__, cli
from local_ssh_config.ssh._constants import SSH_CONFIG_DIR  # GLOBAL_CONFIG_FILE,

# if GLOBAL_CONFIG_FILE.exists():
#     os.remove(GLOBAL_CONFIG_FILE)

# create typer runner for testing
runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_cli() -> None:
    result = runner.invoke(cli.app, ["--file", "tests/settings.json"])
    typer.echo(Path.cwd())
    typer.echo(result.stdout)
    assert result.exit_code == 0

    assert str(SSH_CONFIG_DIR / "test.local") in result.stdout

    assert "SSH config updated! 🚀 ✨!" in result.stdout
