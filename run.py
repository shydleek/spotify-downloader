"""
Единая точка входа для Spotify Downloader.
Сам создаёт venv, ставит зависимости и запускает downloader.py.
Пользователю достаточно запустить: python run.py "ссылка_на_плейлист"
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
VENV_DIR = PROJECT_DIR / "venv"
IS_WINDOWS = platform.system() == "Windows"


def print_header():
    print("=" * 60)
    print("  Spotify Playlist Downloader")
    print("=" * 60)


def check_system_deps():
    """Проверяет наличие ffmpeg и deno."""
    missing = []

    if not shutil.which("ffmpeg"):
        missing.append("ffmpeg")
    if not shutil.which("deno"):
        missing.append("deno")

    if missing:
        print(f"\n⚠️  Не найдены системные программы: {', '.join(missing)}")
        print("\nУстанови их одной командой:")
        if IS_WINDOWS:
            print("  winget install Gyan.FFmpeg DenoLand.Deno")
        else:
            print("  brew install ffmpeg deno")
        print("\nПосле установки закрой и заново открой терминал, потом запусти снова.")
        sys.exit(1)


def get_venv_python():
    """Возвращает путь к python внутри venv."""
    if IS_WINDOWS:
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_venv():
    """Создаёт venv, если его нет."""
    if get_venv_python().exists():
        return

    print("\n📦 Первый запуск: создаю виртуальное окружение...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка создания venv: {e}")
        sys.exit(1)


def ensure_dependencies():
    """Устанавливает зависимости из requirements.txt, если их нет."""
    venv_python = get_venv_python()

    # Проверяем, установлены ли нужные пакеты
    check = subprocess.run(
        [str(venv_python), "-c", "import spotipy, yt_dlp"],
        capture_output=True,
    )
    if check.returncode == 0:
        return

    print("\n📚 Устанавливаю зависимости (один раз, может занять минуту)...")
    try:
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "--upgrade", "pip"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [str(venv_python), "-m", "pip", "install", "-r",
             str(PROJECT_DIR / "requirements.txt")],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Ошибка установки зависимостей: {e}")
        sys.exit(1)


def ensure_config():
    """Проверяет, что config.py создан, иначе даёт подсказку."""
    config_path = PROJECT_DIR / "config.py"
    if not config_path.exists():
        print("\n⚠️  Не найден config.py")
        print("\nСкопируй шаблон и впиши свои ключи Spotify:")
        if IS_WINDOWS:
            print("  copy config.example.py config.py")
        else:
            print("  cp config.example.py config.py")
        print("\nКлючи получить здесь: https://developer.spotify.com/dashboard")
        sys.exit(1)


def ensure_cookies():
    """Проверяет, что cookies.txt есть."""
    cookies_path = PROJECT_DIR / "cookies.txt"
    if not cookies_path.exists():
        print("\n⚠️  Не найден cookies.txt")
        print("\nЭкспортируй cookies из Chrome:")
        print("  1. Установи расширение 'Get cookies.txt LOCALLY'")
        print("  2. Зайди на youtube.com и убедись, что залогинен")
        print("  3. Экспортируй cookies и сохрани как cookies.txt рядом с run.py")
        sys.exit(1)


def run_downloader(args):
    """Запускает downloader.py с переданными аргументами."""
    venv_python = get_venv_python()
    downloader = PROJECT_DIR / "downloader.py"

    result = subprocess.run([str(venv_python), str(downloader)] + args)
    sys.exit(result.returncode)


def main():
    print_header()

    args = sys.argv[1:]
    if not args:
        print("\nИспользование:")
        print('  python run.py "https://open.spotify.com/playlist/..."')
        print("\nПри первом запуске скрипт сам:")
        print("  • создаст виртуальное окружение")
        print("  • установит зависимости")
        print("  • запросит авторизацию Spotify (откроется браузер)")
        sys.exit(0)

    check_system_deps()
    ensure_venv()
    ensure_dependencies()
    ensure_config()
    ensure_cookies()

    print("\n🚀 Запускаю скачивание...\n")
    run_downloader(args)


if __name__ == "__main__":
    main()
