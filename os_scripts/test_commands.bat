@echo off
cd /d "%~dp0.."

echo ===== Commands of stage 4 =====
python src\main.py --vfs vfs\deep.json --script scripts\stage4.txt
