from pathlib import Path


def _create_directory(directory: Path, parents: bool = True) -> None:
    if directory.exists() is False:
        directory.mkdir(
            parents=parents  # create missing parent folders
        )  # Create directory
