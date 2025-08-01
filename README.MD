# 🎙️ Interview Assistant

AI-ассистент, помогающий на интервью в реальном времени. Слушает ваш голос, распознаёт речь на русском языке через OpenAI Whisper, отправляет её в GPT и выводит краткую подсказку на экран (например, поверх Zoom).

## 📦 Возможности

- 🎧 Активация записи по нажатию клавиши `Space`
- 🛑 Остановка записи и отправка текста в GPT — повторное нажатие `Space`
- ❌ Выход из программы — клавиша `X`
- 🧠 Распознавание речи на русском через OpenAI Whisper
- 🤖 Ответ от GPT с краткой подсказкой на русском
- 📺 Отправка результата на WebSocket-оверлей (например, поверх всех окон)

---

## 🧱 Установка

```bash
git clone https://github.com/yourname/interview-assistant.git
cd interview-assistant
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ⚙️ Настройки
Создай .env файл в корне:

```bash
OPENAI_API_KEY=your_openai_api_key
DEVICE_INDEX=2  # номер аудиоустройства, например микрофона или VB-Audio Cable
```

Чтобы узнать список устройств, используй:

```bash
python list_device.py
```

## 🚀 Запуск
Запусти WebSocket сервер (для отображения подсказок в интерфейсе):

```bash
python overlay_server_with_gui.py
```
Запусти слушатель:

```bash
python listener.py
```
Управление:
- Нажми Space — начать запись
- Ещё раз Space — остановить и отправить
- X — выход

## 🖼️ Интерфейс
Можно подключить любой overlay или Electron/Web-прослойку, которая будет принимать WebSocket сообщения по адресу ws://127.0.0.1:8765 и отображать их на экране.

## 🔒 Зависимости
- Python 3.10+
- openai
- pyaudio
- websockets
- python-dotenv

- Установятся через requirements.txt.

## 🧠 Применение
Поддержка на технических собеседованиях
Тренировка интервью
Подсказки в реальном времени, не отвлекаясь на экран

## 🧡 Автор
@Digkill

