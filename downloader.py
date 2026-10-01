import os
import sys
import csv
import platform
import yt_dlp


# --- КОНФИГУРАЦИЯ (читается из config.py) ---
try:
    from config import (
        DOWNLOAD_DIR,
        COOKIES_FILE,
    )
except ImportError:
    print("Ошибка: не найден файл config.py.")
    print("Скопируй config.example.py в config.py.")
    sys.exit(1)

# Определение ОС (для подсказок в консоли)
IS_WINDOWS = platform.system() == "Windows"


def get_tracks_from_csv(csv_path):
    """
    Читает CSV-файл, экспортированный из Spotify (например, через Spotify Scraper
    или Exportify), и возвращает список строк вида "Artist - Name".
    Поддерживает разные названия колонок.
    """
    tracks = []

    # Возможные названия колонок в разных экспортёрах
    artist_keys = ["Artist Name(s)", "Artist Name", "Artist", "Artists", "artist"]
    name_keys = ["Track Name", "Name", "Title", "Song", "track", "name"]

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        # Ищем подходящие колонки (регистронезависимо)
        def find_key(candidates):
            for cand in candidates:
                for fld in fieldnames:
                    if fld.strip().lower() == cand.strip().lower():
                        return fld
            return None

        artist_key = find_key(artist_keys)
        name_key = find_key(name_keys)

        if not artist_key or not name_key:
            print("Ошибка: не удалось найти колонки с артистом и названием трека в CSV.")
            print(f"Доступные колонки: {fieldnames}")
            print("Пожалуйста, убедись, что CSV экспортирован из Spotify Scraper или Exportify.")
            return []

        for row in reader:
            artist = (row.get(artist_key) or "").strip()
            name = (row.get(name_key) or "").strip()
            if artist and name:
                tracks.append(f"{artist} - {name}")

    return tracks


def search_youtube(query):
    """Ищет первое видео на YouTube через yt-dlp и возвращает его URL."""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'default_search': 'ytsearch1',
            'extract_flat': True,
            'cookiefile': COOKIES_FILE,
            'remote_components': ['ejs:github'],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)
            if info and info.get('entries'):
                entry = info['entries'][0]
                if entry.get('url'):
                    return entry['url']
                if entry.get('id'):
                    return f"https://www.youtube.com/watch?v={entry['id']}"
    except Exception as e:
        print(f"  [!] Ошибка поиска на YouTube: {e}")
    return None


def download_audio(youtube_url, output_dir):
    """Скачивает аудио с YouTube и конвертирует в MP3."""
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'cookiefile': COOKIES_FILE,
        'remote_components': ['ejs:github'],
        'socket_timeout': 60,
        'retries': 10,
        'fragment_retries': 10,
        'retry_sleep_functions': {
            'http': lambda n: min(4 ** n, 60),
        },
        'extractor_args': {
            'youtube': {
                'player_client': ['web_safari', 'web', 'web_embedded', 'tv'],
            },
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        print(f"  [!] Ошибка загрузки: {e}")


def main():
    if len(sys.argv) < 2:
        print("Использование:")
        print('  python downloader.py "путь_к_плейлисту.csv"')
        print()
        print("Как получить CSV:")
        print("  1. Установи расширение 'Spotify Scraper' или используй https://exportify.net/")
        print("  2. Открой свой плейлист на open.spotify.com")
        print("  3. Экспортируй в CSV и сохрани файл")
        return

    csv_path = sys.argv[1]

    # Проверяем файлы
    if not os.path.isfile(csv_path):
        print(f"Ошибка: CSV-файл не найден: {os.path.abspath(csv_path)}")
        return

    if not os.path.isfile(COOKIES_FILE):
        print(f"Ошибка: файл cookies не найден: {os.path.abspath(COOKIES_FILE)}")
        print("Экспортируй cookies из Chrome расширением 'Get cookies.txt LOCALLY'")
        print("и положи файл рядом со скриптом под именем cookies.txt.")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"ОС: {platform.system()}")
    print(f"Папка для загрузок: {os.path.abspath(DOWNLOAD_DIR)}")
    print(f"CSV-файл: {os.path.abspath(csv_path)}")
    print(f"Файл cookies: {os.path.abspath(COOKIES_FILE)}")

    print("\nЧтение треков из CSV...")
    tracks = get_tracks_from_csv(csv_path)

    if not tracks:
        print("Не удалось прочитать треки из CSV. Проверь формат файла.")
        return

    print(f"Найдено треков: {len(tracks)}\n")

    for i, track in enumerate(tracks, 1):
        print(f"[{i}/{len(tracks)}] Ищу: {track}")
        youtube_url = search_youtube(track)
        if youtube_url:
            print(f"  -> Скачиваю с: {youtube_url}")
            download_audio(youtube_url, DOWNLOAD_DIR)
            print("  -> Готово.")
        else:
            print("  -> Видео на YouTube не найдено. Пропускаю.")


if __name__ == "__main__":
    main()
