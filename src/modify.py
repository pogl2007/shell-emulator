from errors import CommandError

OWNER_AND_PATH = 2
MAX_PATHS = 1


class ModifyCommands:

    def do_chown(self, args):
        if len(args) != OWNER_AND_PATH:
            raise CommandError("chown: использование: chown владелец путь")
        owner, path = args
        self.find("chown", path).owner = owner
        return ""

    def do_rm(self, args):
        recursive = "-r" in args
        paths = [arg for arg in args if arg != "-r"]
        if not paths or len(paths) > MAX_PATHS:
            raise CommandError("rm: нужно указать один путь")
        node = self.find("rm", paths[0])
        if node.parent is None:
            raise CommandError("rm: нельзя удалить корневую папку")
        if node.is_dir and not recursive:
            raise CommandError(
                f"rm: {paths[0]}: это папка, используйте rm -r")
        self.drop(node)
        return ""

    def drop(self, node):
        removed = node.path()
        parent = node.parent
        parent.remove(node)
        if self.cwd == removed or self.cwd.startswith(removed + "/"):
            self.cwd = parent.path()
