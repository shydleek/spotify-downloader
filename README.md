# Spotify Playlist Downloader

Скачивает все треки из плейлиста Spotify в MP3, находя их на YouTube.

Работает через официальный Spotify Web API (OAuth) и `yt-dlp`.

---

## Требования

- **macOS / Linux / Windows**
- **Python 3.10+** (рекомендуется 3.12)
- **ffmpeg** — для конвертации аудио в MP3
- **Deno** — JS-рантайм, нужен `yt-dlp` для обхода защит YouTube
- **Spotify-аккаунт** и приложение в [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)

---

## Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/твой_ник/spotify-downloader.git
cd spotify-downloader
```

### 2. Установи системные зависимости (macOS через Homebrew)

```bash
brew install python@3.12 ffmpeg deno
```

Для Linux (Ubuntu/Debian):

```bash
sudo apt install python3.12 python3.12-venv ffmpeg
# Deno: https://deno.land/manual/getting_started/installation
```

Для Windows:
- Python: https://www.python.org/downloads/
- ffmpeg: https://www.gyan.dev/ffmpeg/builds/
- Deno: https://deno.land/manual/getting_started/installation

### 3. Создай виртуальное окружение

```bash
python3.12 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. Установи Python-зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Настройка Spotify

1. Открой https://developer.spotify.com/dashboard
2. Нажми **Create app**
3. Заполни:
   - **App name**: любое, например `my-downloader`
   - **App description**: любое
   - **Redirect URI**: `http://127.0.0.1:8888/callback` ← **ровно так**
   - **Which API/SDKs**: отметь **Web API**
4. Сохрани и нажми **Settings**
5. Скопируй **Client ID** и **Client Secret**

Затем создай файл `config.py` из шаблона:

```bash
cp config.example.py config.py
```

И впиши туда свои ключи:

```python
SPOTIFY_CLIENT_ID = "твой_client_id"
SPOTIFY_CLIENT_SECRET = "твой_client_secret"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
DOWNLOAD_DIR = "downloads"
BROWSER_FOR_COOKIES = "chrome"   # или safari / firefox / edge / brave
```

**Важно:** `BROWSER_FOR_COOKIES` — браузер, в котором ты залогинен в YouTube. `yt-dlp` возьмёт оттуда cookies, чтобы YouTube не блокировал скачивание.

---

## Запуск

```bash
python downloader.py "https://open.spotify.com/playlist/ВАШ_ID"
```

При первом запуске:
- откроется браузер → залогинься в Spotify → нажми **Agree**
- увидишь «Authentication status: successful» — можно закрыть вкладку
- скрипт начнёт искать треки на YouTube и качать их

MP3 появятся в папке `downloads/`.

---

## Пример вывода

```
Папка для загрузок: /Users/you/spotify-downloader/downloads
Авторизация в Spotify...
Получение списка треков из Spotify...
[debug] первая страница: total=50, items=50
Найдено треков: 50

[1/50] Ищу: LILDRUGHILL - Show
  -> Скачиваю с: https://www.youtube.com/watch?v=...
  -> Готово.
[2/50] Ищу: VILLIAN, madk1d - ДИНАСТИЯ
  -> Скачиваю с: https://www.youtube.com/watch?v=...
  -> Готово.
...
```

---

## Известные ограничения

- **Чужие плейлисты могут не читаться.** Spotify API отдаёт содержимое только тех плейлистов, где ты владелец или коллаборант. Чужие публичные плейлисты возвращают `404 Resource not found`. Решение: скопировать плейлист в свой аккаунт.
- **Точность поиска.** Трек ищется по строке «Artist - Name» через `ytsearch1`. Иногда YouTube находит кавер, live-версию или ремикс. Проверяй скачанное.
- **Таймауты при скачивании.** Если сеть нестабильна — можно запустить скрипт повторно, уже скачанные треки не будут качаться заново.

---

## Если что-то не работает

| Проблема | Решение |
|---|---|
| `command not found: python3.12` | Установи Python 3.12 (`brew install python@3.12`) |
| `externally-managed-environment` | Активируй venv: `source venv/bin/activate` |
| `Invalid redirect URI` | В панели Spotify должен быть ровно `http://127.0.0.1:8888/callback` |
| `track = None` у всех треков | Плейлист чужой — скопируй его к себе |
| `Signature solving failed` | Установи Deno (`brew install deno`) и обнови yt-dlp |
| `Requested format is not available` | Обнови yt-dlp: `pip install --upgrade yt-dlp` |
| `Read timed out` | Запусти скрипт повторно; при частых таймаутах — проверь сеть/VPN |

---

## Лицензия

MIT — делай что хочешь, но не забудь про авторские права на саму музыку.
