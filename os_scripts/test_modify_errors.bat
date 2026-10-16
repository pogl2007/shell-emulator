@echo off
cd /d "%~dp0.."

echo ===== Errors of stage 5 =====
for %%f in (scripts\errors5\*.txt) do (
    echo ----- %%f -----
    python src\main.py --vfs vfs\deep.json --script %%f
)
