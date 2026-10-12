import pytest

from errors import CommandError
from shell import Shell
from vfs import Vfs

DEEP = "vfs/deep.json"


@pytest.fixture
def shell():
    return Shell(Vfs.from_file(DEEP))


def test_chown(shell):
    shell.execute("chown guest /readme.txt")
    assert shell.vfs.resolve("/", "/readme.txt").owner == "guest"


def test_chown_folder(shell):
    shell.execute("chown guest \"/home/user/my photos\"")
    assert shell.execute("ls -l /home/user").endswith("my photos/")


@pytest.mark.parametrize("line", [
    "chown",
    "chown guest",
    "chown guest a b",
    "chown guest /nope",
])
def test_chown_errors(shell, line):
    with pytest.raises(CommandError):
        shell.execute(line)


def test_rm_file(shell):
    shell.execute("rm /readme.txt")
    assert shell.vfs.resolve("/", "/readme.txt") is None


def test_rm_folder_needs_r(shell):
    with pytest.raises(CommandError, match="используйте rm -r"):
        shell.execute("rm /home")
    shell.execute("rm -r /home")
    assert shell.vfs.resolve("/", "/home") is None


def test_rm_current_folder(shell):
    shell.execute("cd /home/user/docs")
    shell.execute("rm -r /home/user")
    assert shell.cwd == "/home"


@pytest.mark.parametrize("line", ["rm", "rm /nope", "rm -r /"])
def test_rm_errors(shell, line):
    with pytest.raises(CommandError):
        shell.execute(line)
    assert shell.vfs.resolve("/", "/home") is not None


def test_file_not_modified(shell):
    with open(DEEP, encoding="utf-8") as file:
        before = file.read()
    shell.execute("rm -r /home")
    shell.execute("chown nobody /etc")
    with open(DEEP, encoding="utf-8") as file:
        assert file.read() == before
