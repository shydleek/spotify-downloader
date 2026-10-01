# Spotify Playlist Downloader

Скачивает все треки из плейлиста Spotify в MP3, находя их на YouTube.

Работает через официальный Spotify Web API (OAuth) и `yt-dlp`. Поддерживает **Windows**, **macOS** и **Linux**.

---

## Возможности

- 🎵 Скачивает плейлист Spotify целиком в MP3 (192 kbps)
- 🔍 Ищет каждый трек на YouTube по строке «Artist - Name»
- 🔐 Использует официальный Spotify OAuth
- 🍪 Работает с cookies из Chrome (через экспорт в `cookies.txt`)
- 🌍 Кроссплатформенный: Windows, macOS, Linux
- 🔄 Пропускает уже скачанные треки при повторном запуске

---

## Требования

- **Python 3.10+** (рекомендуется 3.12)
- **ffmpeg** — для конвертации аудио в MP3
- **Deno** — JS-рантайм, нужен `yt-dlp` для обхода защит YouTube
- **Spotify-аккаунт** и приложение в [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- **Chrome** (или любой Chromium-браузер) + расширение для экспорта cookies

---

## Установка

### 1. Клонируй репозиторий

```bash
git clone https://github.com/shydleek/spotify-downloader.git
cd spotify-downloader
```

### 2. Установи системные зависимости

**macOS (через Homebrew):**

```bash
brew install python@3.12 ffmpeg deno
```

**Windows (через winget):**

```powershell
winget install Python.Python.3.12
winget install Gyan.FFmpeg
winget install DenoLand.Deno
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt install python3.12 python3.12-venv ffmpeg
# Deno: https://deno.land/manual/getting_started/installation
```

После установки **перезапусти терминал**, чтобы PATH обновился.

### 3. Создай виртуальное окружение

**macOS / Linux:**

```bash
python3.12 -m venv venv
source venv/bin/activate
```

**Windows:**

```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Установи Python-зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Настройка

### Шаг 1. Spotify-приложение

1. Открой https://developer.spotify.com/dashboard
2. Нажми **Create app**
3. Заполни:
   - **App name**: любое, например `my-downloader`
   - **App description**: любое
   - **Redirect URI**: `http://127.0.0.1:8888/callback` ← **ровно так**
   - **Which API/SDKs**: отметь **Web API**
4. Сохрани и нажми **Settings**
5. Скопируй **Client ID** и **Client Secret**

### Шаг 2. Конфиг

Скопируй шаблон:

**macOS / Linux:**
```bash
cp config.example.py config.py
```

**Windows:**
```cmd
copy config.example.py config.py
```

Открой `config.py` и впиши свои ключи:

```python
SPOTIFY_CLIENT_ID = "твой_client_id"
SPOTIFY_CLIENT_SECRET = "твой_client_secret"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
DOWNLOAD_DIR = "downloads"
COOKIES_FILE = "cookies.txt"
```

### Шаг 3. Cookies из Chrome

Из-за ужесточения безопасности Chrome 127+ (Application-Bound Encryption) `yt-dlp` больше не может читать cookies напрямую. Используй экспорт в файл:

1. Установи расширение **«Get cookies.txt LOCALLY»** в Chrome:
   - Chrome Web Store → поиск `Get cookies.txt LOCALLY`
2. Открой **youtube.com** и убедись, что ты залогинен
3. Клик по иконке расширения → **Export** → сохрани как `cookies.txt` **в папку со скриптом**

Итоговая структура:

```
spotify-downloader/
├── downloader.py
├── config.py
├── cookies.txt       ← сюда
├── requirements.txt
├── .gitignore
└── downloads/
```

---

## Запуск

**macOS / Linux:**

```bash
source venv/bin/activate
python downloader.py "https://open.spotify.com/playlist/ВАШ_ID"
```

**Windows:**

```cmd
venv\Scripts\activate
python downloader.py "https://open.spotify.com/playlist/ВАШ_ID"
```

При первом запуске откроется браузер → залогинься в Spotify → нажми **Agree**. Увидишь «Authentication status: successful» — можно закрыть вкладку.

MP3 появятся в папке `downloads/`.

---

## Пример вывода

```
ОС: Darwin
Папка для загрузок: /Users/you/spotify-downloader/downloads
Файл cookies: /Users/you/spotify-downloader/cookies.txt

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

- **Чужие плейлисты не читаются.** Spotify API отдаёт содержимое только тех плейлистов, где ты владелец или коллаборант. Чужие публичные плейлисты возвращают `404 Resource not found`. Решение: скопировать плейлист в свой аккаунт (⋯ → Add to Library).
- **Точность поиска.** Трек ищется по строке «Artist - Name» через `ytsearch1`. Иногда YouTube находит кавер, live-версию или ремикс. Проверяй скачанное.
- **Cookies протухают.** Раз в несколько недель YouTube ротирует cookies. Если скачивание перестало работать — заново экспортируй `cookies.txt`.
- **Таймауты при скачивании.** Если сеть нестабильна — просто запусти скрипт повторно. Уже скачанные треки не будут качаться заново.

---

## Частые проблемы

| Проблема | Решение |
|---|---|
| `command not found: python3.12` | Установи Python 3.12 |
| `externally-managed-environment` | Активируй venv: `source venv/bin/activate` |
| `Invalid redirect URI` | В панели Spotify должен быть ровно `http://127.0.0.1:8888/callback` |
| `track = None` у всех треков | Плейлист чужой — скопируй его к себе |
| `Signature solving failed` | Установи Deno (`brew install deno` / `winget install DenoLand.Deno`) |
| `Requested format is not available` | Обнови yt-dlp: `pip install --upgrade yt-dlp` |
| `Failed to decrypt with DPAPI` | Не используй `--cookies-from-browser chrome`. Работай через `cookies.txt` |
| `Could not copy Chrome cookie database` | То же самое — экспорт cookies в файл |
| `Read timed out` | Запусти скрипт повторно; проверь сеть/VPN |
| `ModuleNotFoundError: No module named 'spotipy'` | Активируй venv: `source venv/bin/activate` |

---

## Структура проекта

```
spotify-downloader/
├── downloader.py          # Основной скрипт
├── config.example.py      # Шаблон конфига (можно коммитить)
├── config.py              # Личный конфиг (НЕ коммитить)
├── cookies.txt            # Cookies YouTube (НЕ коммитить)
├── requirements.txt       # Зависимости
├── .gitignore
├── README.md
└── downloads/             # Скачанные MP3 (НЕ коммитить)
```

---

## Как обновлять cookies

1. Открой Chrome → youtube.com
2. Иконка расширения «Get cookies.txt LOCALLY» → Export
3. Сохрани поверх старого `cookies.txt`

Всё, скрипт снова работает.

---

## Безопасность

- **`config.py` содержит твои Spotify-ключи.** Никогда не коммить его в git.
- **`cookies.txt` содержит сессию Google-аккаунта.** Утечка = доступ к твоему YouTube. Никогда не коммить.
- **`.gitignore` уже исключает оба файла.** Проверь `git status` перед коммитом.

Если случайно залил `config.py` или `cookies.txt` на GitHub:
1. Немедленно смени пароль Google и пересоздай `Client Secret` в Spotify.
2. Удали файлы: `git rm --cached config.py cookies.txt`
3. Закоммить и запушь.
4. Удали историю через [git-filter-repo](https://github.com/newren/git-filter-repo) или создай репозиторий заново.

---

## Лицензия

MIT

---

## Автор

**shydleek** — [github.com/shydleek](https://github.com/shydleek)
