import sys

from config import Config
from errors import ConfigError, VfsError
from shell import Shell
from vfs import Vfs


def build_shell(config):
    if config.vfs is None:
        return Shell()
    vfs = Vfs.from_file(config.vfs, config.vfs_name())
    print(vfs.info())
    return Shell(vfs)


def main(argv=None):
    config = Config.from_args(argv)
    config.show()
    try:
        shell = build_shell(config)
    except VfsError as err:
        print(err)
        return 1
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
