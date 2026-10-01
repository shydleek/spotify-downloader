import os
import sys
import platform
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp

# --- КОНФИГУРАЦИЯ (читается из config.py) ---
try:
    from config import (
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_REDIRECT_URI,
        DOWNLOAD_DIR,
        COOKIES_FILE,
    )
except ImportError:
    print("Ошибка: не найден файл config.py.")
    print("Скопируй config.example.py в config.py и впиши туда свои ключи Spotify.")
    sys.exit(1)

# Где хранится токен авторизации Spotify
CACHE_PATH = ".spotify_cache"

# Права доступа у Spotify
SCOPE = "playlist-read-private playlist-read-collaborative user-read-private user-read-email"

# Определение ОС (для подсказок в консоли)
IS_WINDOWS = platform.system() == "Windows"


def get_spotify_client():
    """Создаёт клиент Spotify с пользовательской авторизацией (OAuth)."""
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=CACHE_PATH,
        open_browser=True,
    ))


def extract_track_data(item):
    """Достаёт 'Artist - Name' из элемента плейлиста, поддерживая все форматы API."""
    if not isinstance(item, dict):
        return None

    candidates = []
    if isinstance(item.get('item'), dict):      # новый формат (2025)
        candidates.append(item['item'])
    if isinstance(item.get('track'), dict):     # старый формат
        candidates.append(item['track'])
    if item.get('type') == 'track' and item.get('name'):
        candidates.append(item)                 # плоский формат

    for track in candidates:
        if track.get('type') == 'track' or track.get('name'):
            artists = track.get('artists') or []
            name = track.get('name')
            if name and artists:
                artist_names = ", ".join(a['name'] for a in artists if a.get('name'))
                if artist_names:
                    return f"{artist_names} - {name}"
    return None


def get_playlist_tracks(sp, playlist_url):
    """Получает список треков из плейлиста Spotify."""
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    tracks = []

    results = sp.playlist_items(playlist_id)
    print(f"[debug] первая страница: total={results.get('total')}, "
          f"items={len(results.get('items', []))}")

    while results:
        for item in results.get('items', []):
            track_str = extract_track_data(item)
            if track_str:
                tracks.append(track_str)
        results = sp.next(results) if results.get('next') else None

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
        if IS_WINDOWS:
            print('  python downloader.py "https://open.spotify.com/playlist/..."')
        else:
            print('  python downloader.py "https://open.spotify.com/playlist/..."')
        return

    playlist_url = sys.argv[1]

    # Проверяем наличие файла cookies
    if not os.path.isfile(COOKIES_FILE):
        print(f"Ошибка: файл cookies не найден: {os.path.abspath(COOKIES_FILE)}")
        print("Экспортируй cookies из Chrome расширением 'Get cookies.txt LOCALLY'")
        print("и положи файл рядом со скриптом под именем cookies.txt.")
        return

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"ОС: {platform.system()}")
    print(f"Папка для загрузок: {os.path.abspath(DOWNLOAD_DIR)}")
    print(f"Файл cookies: {os.path.abspath(COOKIES_FILE)}")

    print("\nАвторизация в Spotify...")
    try:
        sp = get_spotify_client()
    except Exception as e:
        print(f"Ошибка авторизации: {e}")
        return

    print("Получение списка треков из Spotify...")
    try:
        tracks = get_playlist_tracks(sp, playlist_url)
    except Exception as e:
        print(f"Не удалось получить плейлист. Ошибка: {e}")
        return

    if not tracks:
        print("Плейлист пуст или треки не найдены.")
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
