import ctypes
import sys

from local_ssh_config import __app_name__, cli


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main() -> None:
    if is_admin():
        # Code of your program here
        cli.app(prog_name=__app_name__)
    else:
        # Re-run the program with admin rights
        # ctypes.windll.shell32.ShellExecuteW(
        #     None, "runas", sys.executable, " ".join(sys.argv), None, 1
        # )

        cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
