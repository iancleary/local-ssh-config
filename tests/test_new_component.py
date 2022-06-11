import json
import os
import shutil
from pathlib import Path

from typer.testing import CliRunner

from vmsshconfig import __app_name__, __version__, cli
from vmsshconfig._constants import (
    DEFAULT_COMPONENTS_DIR,
    DEFAULT_FILE_EXTENSION,
    GLOBAL_CONFIG_FILE,
    GLOBAL_CONFIG_PATH,
    LOCAL_CONFIG_FILE,
)

# ensure component directory is empty
DEFAULT_COMPONENTS_DIR_PATH = Path(DEFAULT_COMPONENTS_DIR)
if DEFAULT_COMPONENTS_DIR_PATH.exists():
    shutil.rmtree(path=DEFAULT_COMPONENTS_DIR)

if LOCAL_CONFIG_FILE.exists():
    os.remove(LOCAL_CONFIG_FILE)

if GLOBAL_CONFIG_FILE.exists():
    os.remove(GLOBAL_CONFIG_FILE)

# create typer runner for testing
runner = CliRunner()


def test_version() -> None:

    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


def test_prompt_to_create_components_directory() -> None:

    result = runner.invoke(
        cli.app, ["Button"], input="y\n"
    )  # y to create components directory
    assert result.exit_code == 0
    assert (
        "./src/components/ doesn't exist. Do you want to create it? [y/N]:"
        in result.stdout
    )


def test_creating_component() -> None:

    result = runner.invoke(cli.app, ["AwesomeComponent"])
    assert result.exit_code == 0
    assert "AwesomeComponent" in result.stdout
    assert "✨ Creating a new AwesomeComponent Component ✨!" in result.stdout


def test_creating_component_with_directory_first_time() -> None:

    # ensure ./component directory is empty
    SPECIFIED_COMPONENTS_DIR_PATH = Path("./components")
    if SPECIFIED_COMPONENTS_DIR_PATH.exists():
        shutil.rmtree(path=SPECIFIED_COMPONENTS_DIR_PATH)

    result = runner.invoke(
        cli.app, ["DirectoryComponent", "--directory", "components"], input="y\n"
    )
    assert result.exit_code == 0
    assert (
        "./components/ doesn't exist. Do you want to create it? [y/N]:" in result.stdout
    )
    assert "DirectoryComponent" in result.stdout
    assert "✨ Creating a new DirectoryComponent Component ✨!" in result.stdout


def test_creating_component_with_directory_that_exists() -> None:

    result = runner.invoke(
        cli.app, ["DirectoryComponent2", "--directory", "components"]
    )
    assert result.exit_code == 0
    assert "DirectoryComponent2" in result.stdout
    assert "✨ Creating a new DirectoryComponent2 Component ✨!" in result.stdout


def test_creating_component_files() -> None:

    result = runner.invoke(cli.app, ["File"])
    assert result.exit_code == 0
    assert "File" in result.stdout
    assert "✨ Creating a new File Component ✨!" in result.stdout
    assert (
        Path(f"./src/components/File/index.{DEFAULT_FILE_EXTENSION}").exists() is True
    )
    assert Path(f"./src/components/File/File.{DEFAULT_FILE_EXTENSION}").exists() is True


def test_creating_component_with_extension() -> None:

    result = runner.invoke(cli.app, ["Extension", "--extension", "jsx"])
    assert result.exit_code == 0
    assert "Extension" in result.stdout
    assert "✨ Creating a new Extension Component ✨!" in result.stdout
    assert Path("./src/components/Extension/index.jsx").exists() is True
    assert Path("./src/components/Extension/Extension.jsx").exists() is True


def test_local_config_file() -> None:

    if LOCAL_CONFIG_FILE.exists():
        os.remove(LOCAL_CONFIG_FILE)

    if GLOBAL_CONFIG_FILE.exists():
        os.remove(GLOBAL_CONFIG_FILE)

    # Data to be written to LOCAL_CONFIG_FILE
    local_settings = {"extension": "jsx", "directory": "components"}

    with open(LOCAL_CONFIG_FILE, "w") as outfile:
        json.dump(local_settings, outfile, indent=4)

    result = runner.invoke(cli.app, ["LocalConfig"])

    assert result.exit_code == 0
    assert "LocalConfig" in result.stdout
    assert "✨ Creating a new LocalConfig Component ✨!" in result.stdout
    assert Path("./components/LocalConfig/index.jsx").exists() is True
    assert Path("./components/LocalConfig/LocalConfig.jsx").exists() is True


def test_global_config_file() -> None:

    if LOCAL_CONFIG_FILE.exists():
        os.remove(LOCAL_CONFIG_FILE)

    if GLOBAL_CONFIG_FILE.exists():
        os.remove(GLOBAL_CONFIG_FILE)

    if GLOBAL_CONFIG_PATH.exists() is False:
        GLOBAL_CONFIG_PATH.mkdir(parents=True)

    # Data to be written to LOCAL_CONFIG_FILE
    global_settings = {"extension": "jsx", "directory": "src/global/components"}

    with open(GLOBAL_CONFIG_FILE, "w") as outfile:
        json.dump(global_settings, outfile, indent=4)

    result = runner.invoke(cli.app, ["GlobalConfig"], input="y\n")

    assert result.exit_code == 0
    assert "GlobalConfig" in result.stdout
    assert "✨ Creating a new GlobalConfig Component ✨!" in result.stdout
    assert Path("./src/global/components/GlobalConfig/index.jsx").exists() is True
    assert (
        Path("./src/global/components/GlobalConfig/GlobalConfig.jsx").exists() is True
    )


def test_local_and_global_config_file() -> None:

    if LOCAL_CONFIG_FILE.exists():
        os.remove(LOCAL_CONFIG_FILE)

    if GLOBAL_CONFIG_FILE.exists():
        os.remove(GLOBAL_CONFIG_FILE)

    if GLOBAL_CONFIG_PATH.exists() is False:
        GLOBAL_CONFIG_PATH.mkdir(parents=True)

    # Data to be written to LOCAL_CONFIG_FILE
    local_settings = {"extension": "jsx", "directory": "components"}

    with open(LOCAL_CONFIG_FILE, "w") as outfile:
        json.dump(local_settings, outfile, indent=4)

    # Data to be written to LOCAL_CONFIG_FILE
    global_settings = {"extension": "jsx2", "directory": "src/global/components"}

    with open(GLOBAL_CONFIG_FILE, "w") as outfile:
        json.dump(global_settings, outfile, indent=4)

    result = runner.invoke(cli.app, ["LocalAndGlobalConfig"])

    assert result.exit_code == 0
    assert "LocalAndGlobalConfig" in result.stdout
    assert "✨ Creating a new LocalAndGlobalConfig Component ✨!" in result.stdout
    assert Path("./components/LocalAndGlobalConfig/index.jsx").exists() is True
    assert (
        Path("./components/LocalAndGlobalConfig/LocalAndGlobalConfig.jsx").exists()
        is True
    )
