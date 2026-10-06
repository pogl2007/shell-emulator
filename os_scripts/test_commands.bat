@echo off
cd /d "%~dp0.."

echo ===== 1. All commands of stage 4 =====
python src\main.py --vfs vfs\deep.json --script scripts\stage4.txt

echo ===== 2. Errors =====
for %%f in (scripts\errors4\*.txt) do (
    echo ----- %%f -----
    python src\main.py --vfs vfs\deep.json --script %%f
)
