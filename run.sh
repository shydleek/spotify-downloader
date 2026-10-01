#!/bin/bash
# Единая точка входа для macOS / Linux
# Использование: ./run.sh "ссылка_на_плейлист"

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 не найден. Установи его:"
    echo "  macOS: brew install python@3.12"
    echo "  Linux: sudo apt install python3 python3-venv"
    exit 1
fi

python3 run.py "$@"
