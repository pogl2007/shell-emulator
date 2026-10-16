@echo off
cd /d "%~dp0.."

echo ===== Errors of stage 4 =====
for %%f in (scripts\errors4\*.txt) do (
    echo ----- %%f -----
    python src\main.py --vfs vfs\deep.json --script %%f
)
