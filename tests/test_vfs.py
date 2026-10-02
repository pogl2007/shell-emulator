import pytest

from errors import VfsError
from vfs import Vfs, split_path


def test_split_path():
    assert split_path("/home/user", "../docs") == ["home", "docs"]
    assert split_path("/home", "/etc/./hostname") == ["etc", "hostname"]
    assert split_path("/", "..") == []


def test_load_minimal():
    vfs = Vfs.from_file("vfs/minimal.json")
    assert vfs.name == "minimal"
    assert vfs.root.counts() == (1, 0)


def test_load_several():
    vfs = Vfs.from_file("vfs/several.json")
    assert vfs.root.counts() == (1, 3)
    assert vfs.resolve("/", "logo.png").binary is True


def test_text_decoded_from_base64():
    vfs = Vfs.from_file("vfs/several.json")
    node = vfs.resolve("/", "readme.txt")
    assert node.binary is False
    assert node.content == "Hello from VFS!\n"
    assert node.lines() == ["Hello from VFS!"]


def test_load_deep():
    vfs = Vfs.from_file("vfs/deep.json")
    node = vfs.resolve("/", "/home/user/docs/notes.txt")
    assert node.owner == "user"
    assert node.path() == "/home/user/docs/notes.txt"


def test_resolve_relative():
    vfs = Vfs.from_file("vfs/deep.json")
    assert vfs.resolve("/home/user/docs", "../my photos").is_dir
    assert vfs.resolve("/", "/nope") is None
    assert vfs.resolve("/", "/readme.txt/x") is None


def test_info():
    assert "VFS 'deep'" in Vfs.from_file("vfs/deep.json").info()


def test_file_not_found():
    with pytest.raises(VfsError, match="не найден"):
        Vfs.from_file("vfs/no_such_file.json")


@pytest.mark.parametrize("name", [
    "bad_json", "bad_format", "bad_type", "bad_base64",
])
def test_bad_files(name):
    with pytest.raises(VfsError):
        Vfs.from_file(f"vfs/{name}.json")


def test_file_not_modified():
    with open("vfs/deep.json", encoding="utf-8") as file:
        before = file.read()
    Vfs.from_file("vfs/deep.json")
    with open("vfs/deep.json", encoding="utf-8") as file:
        assert file.read() == before
