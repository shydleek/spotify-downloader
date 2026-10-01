# Spotify Playlist Downloader

Скачивает все треки из плейлиста Spotify в MP3, находя их на YouTube.

Не требует Spotify Developer API. Работает через CSV-экспорт и `yt-dlp`.  
Поддерживает **Windows**, **macOS** и **Linux**.

---

## Как это работает

1. Ты экспортируешь свой плейлист в CSV (через [Exportify](https://exportify.net/))
2. Скрипт читает CSV, ищет каждый трек на YouTube
3. Скачивает аудио и конвертирует в MP3

Никакой регистрации приложений, Client ID, Client Secret и OAuth-танцев.

---

## Быстрый старт

### 1. Клонируй репозиторий

```bash
git clone https://github.com/shylleek/spotify-downloader.git
cd spotify-downloader
```

### 2. Установи системные зависимости (один раз)

**macOS:**
```bash
brew install python@3.12 ffmpeg deno
```

**Windows (PowerShell от админа):**
```powershell
winget install Python.Python.3.12 Gyan.FFmpeg DenoLand.Deno
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install python3.12 python3.12-venv ffmpeg
# Deno: https://deno.land/manual/getting_started/installation
```

После установки **перезапусти терминал**.

### 3. Подготовь `config.py`

```bash
# macOS / Linux
cp config.example.py config.py

# Windows
copy config.example.py config.py
```

Внутри `config.py` уже всё готово по умолчанию:
```python
DOWNLOAD_DIR = "downloads"
COOKIES_FILE = "cookies.txt"
```

### 4. Экспортируй cookies YouTube

Chrome 127+ не даёт читать cookies напрямую, поэтому используем экспорт в файл:

1. Установи расширение **«Get cookies.txt LOCALLY»** в Chrome (Chrome Web Store)
2. Открой **youtube.com**, убедись, что залогинен
3. Клик по иконке расширения → **Export** → сохрани как `cookies.txt` в папку проекта

### 5. Экспортируй плейлист в CSV через Exportify

1. Открой https://exportify.net/
2. Нажми **Log in with Spotify** и залогинься
3. Найди нужный плейлист → нажми **Export**
4. Сохрани CSV в папку проекта, например как `playlist.csv`

### 6. Запусти

**macOS / Linux:**
```bash
./run.sh "playlist.csv"
```

**Windows:**
```cmd
run.bat "playlist.csv"
```

Всё. При первом запуске скрипт сам создаст venv, поставит зависимости и начнёт качать.

---

## Структура проекта

```
spotify-downloader/
├── run.sh / run.bat / run.py   # Единая точка входа
├── downloader.py               # Основной скрипт
├── config.py                   # Личный конфиг (НЕ коммитить)
├── config.example.py           # Шаблон конфига
├── cookies.txt                 # Cookies YouTube (НЕ коммитить)
├── playlist.csv                # Твой экспорт из Exportify
├── requirements.txt
├── .gitignore
└── downloads/                  # Сюда падают MP3
```

---

## Пример вывода

```
============================================================
  Spotify Playlist Downloader (via CSV)
============================================================

ОС: Darwin
Папка для загрузок: /Users/you/spotify-downloader/downloads
CSV-файл: /Users/you/spotify-downloader/playlist.csv
Файл cookies: /Users/you/spotify-downloader/cookies.txt

Чтение треков из CSV...
Найдено треков: 50

[1/50] Ищу: LILDRUGHILL - Show
  -> Скачиваю с: https://www.youtube.com/watch?v=...
  -> Готово.
[2/50] Ищу: VILLIAN; madk1d - ДИНАСТИЯ
  -> Скачиваю с: https://www.youtube.com/watch?v=...
  -> Готово.
...
```

---

## Частые вопросы

**Почему не через Spotify Web API?**  
Spotify в 2024–2025 ужесточил политику API: чужие плейлисты не читаются, требуется создание приложения и OAuth. Экспорт через Exportify проще, надёжнее и без регистрации приложений.

**Как экспортировать большой плейлист?**  
Exportify справляется с плейлистами любого размера. Если плейлист 5000+ треков — займёт несколько минут.

**Можно ли сразу несколько CSV?**  
Пока скрипт принимает один CSV за раз. Для нескольких плейлистов — запусти несколько раз (уже скачанные треки не будут качаться заново).

**Как часто обновлять cookies.txt?**  
Раз в несколько недель, когда YouTube ротирует cookies. Если скачивание перестало работать — переэкспортируй.

**Можно ли без cookies?**  
Нет. Без cookies YouTube отдаёт только storyboard-картинки и блокирует скачивание аудио.

---

## Известные ограничения

- **Точность поиска.** Трек ищется по строке «Artist - Name» через `ytsearch1`. Иногда YouTube находит кавер, live-версию или ремикс. Проверяй скачанное.
- **Несколько артистов.** Exportify пишет их через `;`. Скрипт оставляет как есть — YouTube всё равно находит.
- **Таймауты.** При нестабильной сети — запусти скрипт повторно, уже скачанные треки не перекачиваются.

---

## Лицензия

MIT

---

## Автор

**shydleek** — [github.com/shydleek](https://github.com/shydleek)
