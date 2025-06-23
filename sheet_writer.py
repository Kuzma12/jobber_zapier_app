import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = "Data Recording"

def write_to_sheet(data):
    creds_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    if isinstance(data, dict):
        sheet.append_row([str(data.get(key, "")) for key in data])
    elif isinstance(data, list):
        for row in data:
            sheet.append_row([str(row.get(key, "")) for key in row])
