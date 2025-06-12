import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

def save_report(user_id, username, answers: dict, questions: list):
    print("Answers to save:", answers)  # Логируем ответы для отладки
    answers_list = [answers.get(q['id'], '') for q in questions]
    row = [datetime.now().isoformat(), str(user_id), username] + answers_list
    sheet.append_row(row)

def get_stats():
    records = sheet.get_all_records()
    print("Records from sheet:", records)  # DEBUG
    total_money = 0.0
    for r in records:
        val = r.get('money_earned', 0)
        print("Got value:", val)  # 👈 добавь это
        try:
            total_money += float(str(val).replace(',', '.'))
        except (ValueError, TypeError) as e:
            print(f"❗ Warning: Невозможно преобразовать '{val}' в число ({e})")
            continue
    return total_money
