# Report Bot

## ВАЖНО

Файлы `google_creds.json` и `config.py` **не включены** в репозиторий и добавлены в `.gitignore` (никогда не коммить секреты!).

**Перед запуском создайте локально:**
- `google_creds.json` — получите через Google Cloud Console (сервисный аккаунт).
- `config.py` — заполните по шаблону ниже:

```python
# config.py (пример)
BOT_TOKEN = "your_telegram_bot_token"
GOOGLE_CREDENTIALS_FILE = "google_creds.json"
GOOGLE_SHEET_ID = "your_google_sheet_id"
ADMIN_IDS = [123456789]
BOT_TOKEN — получите у @BotFather
GOOGLE_CREDENTIALS_FILE — имя файла, который вы скачаете из Google Cloud Console
GOOGLE_SHEET_ID — ID вашей Google-таблицы (из url)
ADMIN_IDS — Telegram user_id админа (можно пустой список)

Запуск
Установить зависимости:

nginx
Copy code
pip install -r requirements.txt
Заполнить config.py и положить google_creds.json рядом с кодом.

Запустить бота:

nginx
Copy code
python bot.py

1. Запуск: python bot.py
2. Где вопросы: questions.json
3. Где лежат ответы: В Google Sheets (ID см. config.py)
4. Как добавить вопрос: Добавить в questions.json, перезапустить бота
5. Как сменить расписание: scheduler_start() в bot.py
6. Логи: app.log / Google Sheets (каждый ответ с user_id и датой)
7. Как интегрировать: Google Sheets API, файл google_creds.json (service account)
#   r e p o r t _ b o t 
 
 
