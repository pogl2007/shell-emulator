import shlex

from errors import CommandError

VFS_NAME = "vfs"
MAX_ARGS = 1


class Shell:

    def __init__(self, name=VFS_NAME):
        self.name = name
        self.running = True
        self.commands = {
            "ls": self.do_ls,
            "cd": self.do_cd,
            "exit": self.do_exit,
        }

    def prompt(self):
        return f"{self.name}:~$ "

    @staticmethod
    def parse(line):
        words = shlex.split(line)
        if not words:
            return None, []
        return words[0], words[1:]

    def execute(self, line):
        try:
            name, args = self.parse(line)
        except ValueError as err:
            raise CommandError(f"syntax error: {err}") from err
        if name is None:
            return ""
        if name not in self.commands:
            raise CommandError(f"{name}: command not found")
        return self.commands[name](args)

    def do_ls(self, args):
        return f"ls {args}"

    def do_cd(self, args):
        if len(args) > MAX_ARGS:
            raise CommandError("cd: too many arguments")
        return f"cd {args}"

    def do_exit(self, args):
        if len(args) > MAX_ARGS:
            raise CommandError("exit: too many arguments")
        if args and not args[0].isdigit():
            raise CommandError(f"exit: {args[0]}: numeric argument required")
        self.running = False
        return ""

    @staticmethod
    def show(text):
        if text:
            print(text)

    def repl(self):
        while self.running:
            try:
                line = input(self.prompt())
            except EOFError:
                break
            try:
                self.show(self.execute(line))
            except CommandError as err:
                print(err)

    def run_script(self, lines):
        for line in lines:
            if not self.running:
                break
            print(self.prompt() + line)
            try:
                self.show(self.execute(line))
            except CommandError as err:
                print(err)
                print("Скрипт остановлен из-за ошибки")
                return False
        return True
