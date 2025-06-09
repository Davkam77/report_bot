import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_ID

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).sheet1

def save_report(user_id, username, answers: dict):
    row = [datetime.now().isoformat(), str(user_id), username] + [answers[k] for k in answers]
    sheet.append_row(row)

def get_stats():
    # Достаём агрегаты (примерно, можно адаптировать)
    records = sheet.get_all_records()
    # Например: сумма по 'money_earned'
    try:
        total_money = sum(float(r.get('money_earned', 0) or 0) for r in records)
    except Exception:
        total_money = 0
    return total_money
