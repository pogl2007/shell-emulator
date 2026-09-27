@echo off
cd /d "%~dp0.."

echo ===== 1. Minimal VFS =====
echo exit| python src\main.py --vfs vfs\minimal.json

echo ===== 2. VFS with several files =====
echo exit| python src\main.py --vfs vfs\several.json

echo ===== 3. VFS with 3+ levels =====
echo exit| python src\main.py --vfs vfs\deep.json

echo ===== 4. Start script for stages 1-3 =====
python src\main.py --vfs vfs\deep.json --script scripts\stage3.txt
echo exit code: %ERRORLEVEL%

echo ===== 5. VFS file not found =====
python src\main.py --vfs vfs\nope.json
echo exit code: %ERRORLEVEL%

echo ===== 6. Not JSON =====
python src\main.py --vfs vfs\bad_json.json

echo ===== 7. No root =====
python src\main.py --vfs vfs\bad_format.json

echo ===== 8. Unknown node type =====
python src\main.py --vfs vfs\bad_type.json

echo ===== 9. Wrong base64 =====
python src\main.py --vfs vfs\bad_base64.json
