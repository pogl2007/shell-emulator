import pytest

from config import Config
from errors import ConfigError
from shell import Shell


def make_script(tmp_path, text):
    path = tmp_path / "script.txt"
    path.write_text(text, encoding="utf-8")
    return Config(script=str(path))


def test_from_args():
    config = Config.from_args(["--vfs", "disk.json", "--script", "s.txt"])
    assert config.vfs == "disk.json"
    assert config.script == "s.txt"


def test_vfs_name():
    assert Config(vfs="vfs/disk.json").vfs_name() == "disk"
    assert Config().vfs_name() == "vfs"


def test_script_lines(tmp_path):
    config = make_script(tmp_path, "# комментарий\nls\n\ncd /\n")
    assert config.script_lines() == ["ls", "cd /"]


def test_script_not_found():
    with pytest.raises(ConfigError):
        Config(script="no_such_file.txt").script_lines()


def test_run_script(tmp_path, capsys):
    config = make_script(tmp_path, "ls -l\nexit\n")
    assert Shell().run_script(config.script_lines()) is True
    out = capsys.readouterr().out
    assert "vfs:~$ ls -l\nls ['-l']\n" in out


def test_run_script_stops_on_error(tmp_path, capsys):
    config = make_script(tmp_path, "ls 1\nfoo\nls 2\n")
    assert Shell().run_script(config.script_lines()) is False
    out = capsys.readouterr().out
    assert "foo: command not found" in out
    assert "Скрипт остановлен из-за ошибки" in out
    assert "ls ['2']" not in out
