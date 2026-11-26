@echo off
rem Chay file nay sau khi sua du-lieu.txt hoac them nhac audio\theme.mp3
chcp 65001 >nul
cd /d "%~dp0"
py -3 "%~dp0dung_lai.py"
pause
