import pytest

from errors import CommandError
from shell import Shell
from vfs import Vfs


@pytest.fixture
def shell():
    return Shell(Vfs.from_file("vfs/deep.json"))


def test_ls(shell):
    assert shell.execute("ls") == "etc/\nhome/\nreadme.txt"


def test_ls_long(shell):
    assert shell.execute("ls -l /home/user") == (
        "dir  user   docs/\ndir  user   my photos/")


def test_ls_file(shell):
    assert shell.execute("ls /readme.txt") == "readme.txt"


def test_ls_errors(shell):
    with pytest.raises(CommandError, match="нет такого файла"):
        shell.execute("ls /nope")
    with pytest.raises(CommandError, match="только один путь"):
        shell.execute("ls /etc /home")


def test_cd(shell):
    shell.execute("cd home/user")
    assert shell.cwd == "/home/user"
    shell.execute("cd ../..")
    assert shell.cwd == "/"
    shell.execute("cd \"/home/user/my photos\"")
    assert shell.prompt() == "deep:/home/user/my photos$ "


def test_cd_errors(shell):
    with pytest.raises(CommandError, match="нет такого файла"):
        shell.execute("cd /nope")
    with pytest.raises(CommandError, match="это не папка"):
        shell.execute("cd /readme.txt")
    assert shell.cwd == "/"


def test_head(shell):
    lines = shell.execute("head /home/user/docs/notes.txt").split("\n")
    assert lines == [str(number) for number in range(1, 11)]


def test_head_count(shell):
    assert shell.execute("head -n 3 /home/user/docs/notes.txt") == "1\n2\n3"


def test_tail(shell):
    assert shell.execute("tail -n 2 /home/user/docs/notes.txt") == "11\n12"


def test_tail_relative_path(shell):
    shell.execute("cd /home/user/docs")
    assert shell.execute("tail -n 1 todo.txt") == "learn git"


@pytest.mark.parametrize("line, message", [
    ("head", "нужно указать один файл"),
    ("head /nope", "нет такого файла"),
    ("head /etc", "это папка"),
    ("head -n abc /readme.txt", "неверное число строк"),
    ("tail \"/home/user/my photos/cat.png\"", "это двоичный файл"),
])
def test_head_tail_errors(shell, line, message):
    with pytest.raises(CommandError, match=message):
        shell.execute(line)


def test_clear_errors(shell):
    with pytest.raises(CommandError, match="too many arguments"):
        shell.execute("clear now")
