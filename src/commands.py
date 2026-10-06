import os

from errors import CommandError

DEFAULT_LINES = 10
MAX_PATHS = 1


class BasicCommands:

    def find(self, command, path):
        node = self.vfs.resolve(self.cwd, path)
        if node is None:
            raise CommandError(
                f"{command}: {path}: нет такого файла или папки")
        return node

    @staticmethod
    def format_item(node, long_format):
        name = node.name + "/" if node.is_dir else node.name
        if long_format:
            return f"{node.kind:4} {node.owner:6} {name}"
        return name

    def do_ls(self, args):
        long_format = "-l" in args
        paths = [arg for arg in args if arg != "-l"]
        if len(paths) > MAX_PATHS:
            raise CommandError("ls: можно указать только один путь")
        node = self.find("ls", paths[0] if paths else ".")
        if node.is_dir:
            items = sorted(node.children.values(), key=lambda x: x.name)
        else:
            items = [node]
        return "\n".join(self.format_item(item, long_format)
                         for item in items)

    def do_cd(self, args):
        if len(args) > MAX_PATHS:
            raise CommandError("cd: too many arguments")
        path = args[0] if args else "/"
        node = self.find("cd", path)
        if not node.is_dir:
            raise CommandError(f"cd: {path}: это не папка")
        self.cwd = node.path()
        return ""

    @staticmethod
    def line_count(command, values):
        if not values or not values[0].isdigit():
            raise CommandError(f"{command}: неверное число строк")
        return int(values[0])

    def file_lines(self, command, args):
        count = DEFAULT_LINES
        if args[:1] == ["-n"]:
            count = self.line_count(command, args[1:2])
            args = args[2:]
        if len(args) != MAX_PATHS:
            raise CommandError(f"{command}: нужно указать один файл")
        node = self.find(command, args[0])
        if node.is_dir:
            raise CommandError(f"{command}: {args[0]}: это папка")
        if node.binary:
            raise CommandError(f"{command}: {args[0]}: это двоичный файл")
        return node.lines(), count

    def do_head(self, args):
        lines, count = self.file_lines("head", args)
        return "\n".join(lines[:count])

    def do_tail(self, args):
        lines, count = self.file_lines("tail", args)
        return "\n".join(lines[-count:] if count else [])

    @staticmethod
    def do_clear(args):
        if args:
            raise CommandError("clear: too many arguments")
        os.system("cls" if os.name == "nt" else "clear")
        return ""
