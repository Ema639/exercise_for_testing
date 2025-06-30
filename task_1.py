import requests
import zipfile
import io
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import *

"""Авторизация Google Sheets"""
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
gc = gspread.authorize(creds)

"""Инициализация Google Drive API"""

drive_service = build('drive', 'v3', credentials=creds)

"""Копирование исходной таблицы"""

copied_file = drive_service.files().copy(
    fileId=ORIGINAL_SPREADSHEET_ID,
    body={"name": f"Копия {YOUR_NAME}"}
).execute()

copied_spreadsheet_id = copied_file['id']
spreadsheet = gc.open_by_key(copied_spreadsheet_id)

print(f"Создана копия таблицы: https://docs.google.com/spreadsheets/d/{copied_spreadsheet_id}")

"""Получение данных с Wildberries"""

headers = {"Authorization": TOKEN}
payload = {"category": CATEGORY}

if SERVICE_NAMES:
    payload["serviceName"] = SERVICE_NAMES

response = requests.post(API_URL, headers=headers, json=payload)
response.raise_for_status()

print("✅ Данные получены, распаковка архива...")

"""Распаковка zip-архива"""

zip_file = zipfile.ZipFile(io.BytesIO(response.content))
report_files = zip_file.namelist()

"""Загрузка каждого отчёта на отдельный лист"""
for file_name in report_files:
    with zip_file.open(file_name) as f:
        content = f.read().decode('utf-8')
        rows = [line.split(',') for line in content.splitlines()]

        sheet_title = file_name.split('.')[0]

        try:
            worksheet = spreadsheet.add_worksheet(title=sheet_title, rows="100", cols="20")
        except gspread.exceptions.APIError:
            worksheet = spreadsheet.worksheet(sheet_title)
            worksheet.clear()

        worksheet.update('A1', rows)
        print(f" Загружен отчёт: {sheet_title}")

print("Все отчёты успешно загружены в Google Sheets")
