import sys

from config import Config
from errors import ConfigError
from shell import Shell


def main(argv=None):
    config = Config.from_args(argv)
    config.show()
    shell = Shell(config.vfs_name())
    if config.script is None:
        shell.repl()
        return 0
    try:
        lines = config.script_lines()
    except ConfigError as err:
        print(err)
        return 1
    return 0 if shell.run_script(lines) else 1


if __name__ == "__main__":
    sys.exit(main())
