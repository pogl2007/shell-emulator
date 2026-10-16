@echo off
cd /d "%~dp0.."

echo ===== chown and rm =====
python src\main.py --vfs vfs\deep.json --script scripts\stage5.txt

echo ===== VFS file is not modified: new start shows everything =====
echo ls -l| python src\main.py --vfs vfs\deep.json
