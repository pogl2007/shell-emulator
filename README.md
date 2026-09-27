# Эмулятор оболочки

Практическая работа №1, вариант 12. Этапы 1-3.

Консольный эмулятор UNIX-оболочки. В приглашении показывается имя
VFS: `vfs:~$`.

## Команды

- `ls`, `cd` — пока заглушки, печатают свои аргументы
- `exit [код]` — выход

Аргументы в кавычках не разбиваются: `cd "my dir"`.
Ошибки: неизвестная команда, незакрытая кавычка, лишние аргументы.

## Параметры

- `--vfs PATH` — путь к файлу VFS, имя файла становится именем VFS
- `--script PATH` — путь к стартовому скрипту

Оба параметра печатаются при запуске.

Стартовый скрипт — текстовый файл, по команде в строке. Строки с `#`
пропускаются, команда печатается вместе с приглашением, на первой
ошибке выполнение прекращается.

Скрипт для проверки параметров: `os_scripts\test_params.bat`.

## VFS

VFS грузится из JSON-файла в память, сам файл не меняется. Двоичные
файлы лежат в base64.

```json
{
  "name": "mydisk",
  "root": {
    "type": "dir",
    "children": {
      "readme.txt": {"type": "file", "content": "Hello\n"},
      "logo.png": {"type": "file", "base64": "iVBORw0KGgo="},
      "home": {"type": "dir", "owner": "user", "children": {}}
    }
  }
}
```

Готовые VFS в папке `vfs/`: `minimal.json` (пустая), `several.json`
(несколько файлов), `deep.json` (больше 3 уровней). Файлы `bad_*.json`
для проверки ошибок: не JSON, нет root, неизвестный тип, плохой base64.

Проверка всех VFS: `os_scripts\test_vfs.bat`.

## Запуск

В PowerShell нужно писать `.\run.bat`, в cmd просто `run.bat`.

Интерактивный режим:

```
.\run.bat
```

Имя VFS в приглашении (`mydisk:~$`):

```
.\run.bat --vfs vfs\mydisk.json
```

Выполнение стартового скрипта:

```
.\run.bat --script scripts\stage2.txt
```

Скрипт с ошибкой, выполнение прекращается, код выхода 1:

```
.\run.bat --script scripts\stage2_error.txt
```

Оба параметра сразу:

```
.\run.bat --vfs vfs\mydisk.json --script scripts\stage2.txt
```

Загрузка VFS:

```
.\run.bat --vfs vfs\deep.json
```

Все варианты параметров одной командой:

```
.\os_scripts\test_params.bat
```

Все варианты VFS и ошибки загрузки:

```
.\os_scripts\test_vfs.bat
```

Можно запускать и напрямую: `python src\main.py [параметры]`.

## Тесты

```
python -m pytest
```

## Пример

```
vfs:~$ ls -l "my dir"
ls ['-l', 'my dir']
vfs:~$ cd a b
cd: too many arguments
vfs:~$ foo
foo: command not found
vfs:~$ exit
```
