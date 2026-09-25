@echo off
cd /d "%~dp0.."

echo ===== 1. No parameters =====
echo exit| python src\main.py

echo ===== 2. Only --vfs =====
echo exit| python src\main.py --vfs vfs\mydisk.json

echo ===== 3. Only --script =====
python src\main.py --script scripts\stage2.txt
echo exit code: %ERRORLEVEL%

echo ===== 4. --vfs and --script =====
python src\main.py --vfs vfs\mydisk.json --script scripts\stage2.txt

echo ===== 5. Script with error =====
python src\main.py --script scripts\stage2_error.txt
echo exit code: %ERRORLEVEL%

echo ===== 6. Script not found =====
python src\main.py --script scripts\nope.txt
echo exit code: %ERRORLEVEL%

echo ===== 7. Help =====
python src\main.py --help
