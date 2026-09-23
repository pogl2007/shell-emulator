import pytest

from errors import CommandError
from shell import Shell


@pytest.fixture
def shell():
    return Shell()


def test_parse_simple():
    assert Shell.parse("ls -l /home") == ("ls", ["-l", "/home"])


def test_parse_quotes():
    assert Shell.parse("cd \"my dir\" 'a b'") == ("cd", ["my dir", "a b"])


def test_parse_empty():
    assert Shell.parse("   ") == (None, [])


def test_prompt(shell):
    assert shell.prompt() == "vfs:~$ "


def test_ls_stub(shell):
    assert shell.execute("ls -l \"my dir\"") == "ls ['-l', 'my dir']"


def test_cd_stub(shell):
    assert shell.execute("cd /home") == "cd ['/home']"


def test_empty_line(shell):
    assert shell.execute("") == ""


def test_unclosed_quote(shell):
    with pytest.raises(CommandError, match="syntax error"):
        shell.execute("ls \"abc")


def test_unknown_command(shell):
    with pytest.raises(CommandError, match="command not found"):
        shell.execute("foo")


def test_cd_too_many_args(shell):
    with pytest.raises(CommandError, match="too many arguments"):
        shell.execute("cd a b")


def test_exit(shell):
    shell.execute("exit")
    assert shell.running is False


def test_exit_errors(shell):
    with pytest.raises(CommandError, match="numeric argument required"):
        shell.execute("exit abc")
    with pytest.raises(CommandError, match="too many arguments"):
        shell.execute("exit 1 2")
    assert shell.running is True
