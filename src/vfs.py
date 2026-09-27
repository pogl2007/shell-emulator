import base64
import binascii
import json

from errors import VfsError

DIR = "dir"
FILE = "file"
DEFAULT_NAME = "vfs"
DEFAULT_OWNER = "root"


def split_path(cwd, path):
    if path.startswith("/"):
        parts = []
    else:
        parts = [part for part in cwd.split("/") if part]
    for part in path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return parts


class Node:

    def __init__(self, name, kind, owner=DEFAULT_OWNER):
        self.name = name
        self.kind = kind
        self.owner = owner
        self.parent = None
        self.children = {}
        self.content = ""
        self.binary = False

    @property
    def is_dir(self):
        return self.kind == DIR

    def add(self, child):
        child.parent = self
        self.children[child.name] = child

    def remove(self, child):
        del self.children[child.name]
        child.parent = None

    def path(self):
        parts = []
        node = self
        while node.parent is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts))

    def lines(self):
        return self.content.splitlines()

    def counts(self):
        if not self.is_dir:
            return 0, 1
        dirs, files = 1, 0
        for child in self.children.values():
            child_dirs, child_files = child.counts()
            dirs += child_dirs
            files += child_files
        return dirs, files


class Vfs:

    def __init__(self, name=DEFAULT_NAME, root=None):
        self.name = name
        self.root = root if root is not None else Node("", DIR)

    @classmethod
    def from_file(cls, path, default_name=DEFAULT_NAME):
        data = cls.read_json(path)
        if not isinstance(data, dict) or "root" not in data:
            raise VfsError("Ошибка: неверный формат VFS, нет поля root")
        root = cls.build_node("", data["root"], "/")
        if not root.is_dir:
            raise VfsError("Ошибка: root должен быть папкой")
        return cls(data.get("name", default_name), root)

    @staticmethod
    def read_json(path):
        try:
            with open(path, encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError as err:
            raise VfsError(f"Ошибка: файл VFS не найден: {path}") from err
        except json.JSONDecodeError as err:
            raise VfsError(
                f"Ошибка: файл VFS не является JSON: {path}") from err

    @classmethod
    def build_node(cls, name, spec, where):
        if not isinstance(spec, dict):
            raise VfsError(f"Ошибка: неверный узел VFS: {where}")
        node = Node(name, spec.get("type"), spec.get("owner", DEFAULT_OWNER))
        if node.kind == DIR:
            cls.build_children(node, spec.get("children", {}), where)
        elif node.kind == FILE:
            cls.fill_file(node, spec, where)
        else:
            raise VfsError(f"Ошибка: неизвестный тип узла: {where}")
        return node

    @classmethod
    def build_children(cls, node, children, where):
        if not isinstance(children, dict):
            raise VfsError(f"Ошибка: children должен быть объектом: {where}")
        for name, spec in children.items():
            child_path = where.rstrip("/") + "/" + name
            node.add(cls.build_node(name, spec, child_path))

    @staticmethod
    def fill_file(node, spec, where):
        if "base64" in spec:
            node.binary = True
            try:
                base64.b64decode(spec["base64"], validate=True)
            except (binascii.Error, ValueError) as err:
                raise VfsError(
                    f"Ошибка: неверные данные base64: {where}") from err
            return
        content = spec.get("content", "")
        if not isinstance(content, str):
            raise VfsError(f"Ошибка: content должен быть строкой: {where}")
        node.content = content

    def resolve(self, cwd, path):
        node = self.root
        for name in split_path(cwd, path):
            if not node.is_dir or name not in node.children:
                return None
            node = node.children[name]
        return node

    def info(self):
        dirs, files = self.root.counts()
        return f"VFS '{self.name}' загружена: папок {dirs}, файлов {files}"
