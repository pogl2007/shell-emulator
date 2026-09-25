import argparse
import os

from errors import ConfigError

DEFAULT_NAME = "vfs"


class Config:

    def __init__(self, vfs=None, script=None):
        self.vfs = vfs
        self.script = script

    @classmethod
    def from_args(cls, argv=None):
        parser = argparse.ArgumentParser(
            description="Эмулятор командной строки UNIX")
        parser.add_argument("--vfs", help="путь к файлу VFS")
        parser.add_argument("--script", help="путь к стартовому скрипту")
        args = parser.parse_args(argv)
        return cls(args.vfs, args.script)

    def show(self):
        print("[DEBUG] vfs =", self.vfs)
        print("[DEBUG] script =", self.script)

    def vfs_name(self):
        if self.vfs is None:
            return DEFAULT_NAME
        name = os.path.basename(self.vfs)
        return os.path.splitext(name)[0] or DEFAULT_NAME

    def script_lines(self):
        try:
            with open(self.script, encoding="utf-8") as file:
                text = file.read()
        except FileNotFoundError as err:
            raise ConfigError(
                f"Ошибка: файл скрипта не найден: {self.script}") from err
        return [line for line in text.splitlines()
                if line.strip() and not line.startswith("#")]
