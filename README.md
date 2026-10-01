# Spotify Playlist Downloader

Скачивает все треки из плейлиста Spotify в MP3, находя их на YouTube.

Работает через официальный Spotify Web API и `yt-dlp`. Поддерживает **Windows**, **macOS** и **Linux**.

---

## Быстрый старт

```bash
# 1. Клонируй
git clone https://github.com/shydleek/spotify-downloader.git
cd spotify-downloader

# 2. Поставь системные зависимости (один раз)
# macOS:
brew install python@3.12 ffmpeg deno

# Windows (PowerShell):
winget install Python.Python.3.12 Gyan.FFmpeg DenoLand.Deno

# Linux (Ubuntu/Debian):
sudo apt install python3.12 python3.12-venv ffmpeg
# Deno: https://deno.land/manual/getting_started/installation

# 3. Настрой ключи и cookies (см. ниже)

# 4. Запусти
# macOS / Linux:
./run.sh "https://open.spotify.com/playlist/ВАШ_ID"

# Windows:
run.bat "https://open.spotify.com/playlist/ВАШ_ID"
```

Всё остальное — venv, зависимости, авторизация — **делается автоматически при первом запуске**.

---

## Настройка (один раз)

### 1. Ключи Spotify

1. Создай приложение на https://developer.spotify.com/dashboard
2. В **Redirect URIs** добавь: `http://127.0.0.1:8888/callback`
3. Скопируй **Client ID** и **Client Secret**

Скопируй шаблон конфига:

```bash
# macOS / Linux
cp config.example.py config.py

# Windows
copy config.example.py config.py
```

Открой `config.py` и впиши ключи:

```python
SPOTIFY_CLIENT_ID = "твой_client_id"
SPOTIFY_CLIENT_SECRET = "твой_client_secret"
```

### 2. Cookies из Chrome

Chrome 127+ не даёт читать cookies напрямую — работаем через экспорт:

1. Установи расширение **«Get cookies.txt LOCALLY»** в Chrome
2. Открой youtube.com и убедись, что залогинен
3. Экспортируй cookies и сохрани файл как **`cookies.txt`** в папку проекта

Итоговая структура:

```
spotify-downloader/
├── run.sh / run.bat / run.py     ← единая точка входа
├── downloader.py
├── config.py                     ← твои ключи (не коммитить)
├── cookies.txt                   ← cookies YouTube (не коммитить)
├── requirements.txt
├── .gitignore
└── downloads/                    ← сюда падают MP3
```

---

## Что делает `run.py`

При первом запуске автоматически:

- ✅ проверяет наличие `ffmpeg` и `deno`
- ✅ создаёт виртуальное окружение `venv/`
- ✅ устанавливает зависимости из `requirements.txt`
- ✅ проверяет, что `config.py` и `cookies.txt` на месте
- ✅ запускает `downloader.py`

При последующих запусках — просто запускает скачивание.

---

## Пример вывода

```
============================================================
  Spotify Playlist Downloader
============================================================

📦 Первый запуск: создаю виртуальное окружение...
📚 Устанавливаю зависимости (один раз, может занять минуту)...
🚀 Запускаю скачивание...

ОС: Windows
Папка для загрузок: C:\Users\you\spotify-downloader\downloads
Файл cookies: C:\Users\you\spotify-downloader\cookies.txt

Авторизация в Spotify...
[debug] первая страница: total=3, items=3
Найдено треков: 3

[1/3] Ищу: LILDRUGHILL - Show
  -> Скачиваю с: https://www.youtube.com/watch?v=...
  -> Готово.
...
```

---

## Известные ограничения

- **Чужие плейлисты не читаются.** Spotify API отдаёт содержимое только тех плейлистов, где ты владелец или коллаборант. Скопируй чужой плейлист в свой аккаунт (⋯ → Add to Library).
- **Точность поиска.** Трек ищется по строке «Artist - Name» через `ytsearch1`. Иногда YouTube находит кавер или ремикс.
- **Cookies протухают.** Раз в несколько недель переэкспортируй `cookies.txt`.
- **Таймауты при скачивании.** Если сеть нестабильна — запусти скрипт повторно.

---

## Частые проблемы

| Проблема | Решение |
|---|---|
| `Не найдены: ffmpeg, deno` | Установи их (см. «Быстрый старт») и перезапусти терминал |
| `Не найден config.py` | `cp config.example.py config.py` и впиши ключи |
| `Не найден cookies.txt` | Экспортируй cookies из Chrome расширением |
| `Invalid redirect URI` | В панели Spotify должен быть ровно `http://127.0.0.1:8888/callback` |
| `track = None` у всех треков | Плейлист чужой — скопируй к себе |
| `Signature solving failed` | Установи Deno |
| `Read timed out` | Запусти скрипт повторно |

---

## Лицензия

MIT

---

## Автор

**shydleek** — [github.com/shydleek](https://github.com/shydleek)
