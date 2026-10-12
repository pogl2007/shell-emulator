@echo off
cd /d "%~dp0.."

echo ===== 1. chown and rm =====
python src\main.py --vfs vfs\deep.json --script scripts\stage5.txt

echo ===== 2. VFS file is not modified: new start shows everything =====
echo ls -l| python src\main.py --vfs vfs\deep.json

echo ===== 3. Errors =====
for %%f in (scripts\errors5\*.txt) do (
    echo ----- %%f -----
    python src\main.py --vfs vfs\deep.json --script %%f
)
