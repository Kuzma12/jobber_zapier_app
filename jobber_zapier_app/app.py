from flask import Flask, request, jsonify
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

app = Flask(__name__)

# -------------------------------
# CONFIGURATION
# -------------------------------
JOBBER_API_TOKEN = os.getenv("JOBBER_API_TOKEN")
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "Quote Math Checker")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# -------------------------------
# GOOGLE SHEETS AUTH
# -------------------------------
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open(GOOGLE_SHEET_NAME).sheet1

# -------------------------------
# SETUP SHEET HEADERS
# -------------------------------
def init_headers():
    if sheet.cell(1, 1).value != "Source":
        headers = [
            "Source", "Quote ID", "Client Name", "Title", "Status",
            "Line Items Count", "Reported Subtotal", "Calculated Subtotal",
            "Fixed?", "Comment"
        ]
        sheet.clear()
        sheet.append_row(headers)
    try:
        tracking = client.open(GOOGLE_SHEET_NAME).worksheet("Tracking")
    except:
        tracking = client.open(GOOGLE_SHEET_NAME).add_worksheet(title="Tracking", rows="1000", cols="4")
        tracking.append_row(["Timestamp", "Client Name", "Quote ID", "Source"])

# -------------------------------
# EMAIL NOTIFICATION
# -------------------------------
def send_notification(client_name, quote_id, source):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    subject = "✅ Quote Imported"
    message = f"""
    ✅ New quote imported:
    - Client: {client_name}
    - Quote ID: {quote_id}
    - Source: {source}
    - Time: {timestamp}
    """
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECIPIENT

    try:
        smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        smtp.starttls()
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg.as_string())
        smtp.quit()
        print("✅ Email sent.")
    except Exception as e:
        print("❌ Email error:", e)

    try:
        tracking_sheet = client.open(GOOGLE_SHEET_NAME).worksheet("Tracking")
        tracking_sheet.append_row([timestamp, client_name, quote_id, source])
    except Exception as e:
        print("❌ Tracking sheet error:", e)

# -------------------------------
# PROCESS A SINGLE QUOTE
# -------------------------------
def process_quote(source, quote):
    quote_id = quote.get("id", "")
    title = quote.get("title", "")
    status = quote.get("status", "")
    client = quote.get("client", {})
    client_name = f"{client.get('first_name', '')} {client.get('last_name', '')}".strip()
    line_items = quote.get("line_items", [])

    reported_subtotal = quote.get("subtotal", 0.0)
    calculated_subtotal = 0.0
    for item in line_items:
        quantity = float(item.get("quantity", 1))
        unit_cost = float(item.get("unit_cost", 0.0))
        calculated_subtotal += quantity * unit_cost

    fixed = ""
    comment = ""
    if abs(calculated_subtotal - reported_subtotal) > 0.01:
        reported_subtotal = round(calculated_subtotal, 2)
        fixed = "Yes"
        comment = "Subtotal corrected"

    row = [
        source, quote_id, client_name, title, status,
        len(line_items), reported_subtotal, round(calculated_subtotal, 2),
        fixed, comment
    ]
    sheet.append_row(row)
    send_notification(client_name, quote_id, source)

# -------------------------------
# PULL JOBBER QUOTES
# -------------------------------
def pull_jobber_quotes():
    url = 'https://api.getjobber.com/api/quotes'
    headers = {
        'Authorization': f'Bearer {JOBBER_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json().get("quotes", [])

# -------------------------------
# ZAPIER POST ENDPOINT
# -------------------------------
@app.route('/webhook', methods=['POST'])
def receive_zapier_post():
    data = request.json
    init_headers()
    quotes = data.get("quotes", [])

    for quote in quotes:
        process_quote("Zapier", quote)

    return jsonify({"status": "received", "quotes_processed": len(quotes)}), 200

# -------------------------------
# JOBBER SYNC ENDPOINT
# -------------------------------
@app.route('/sync/jobber', methods=['GET'])
def sync_jobber_quotes():
    init_headers()
    quotes = pull_jobber_quotes()
    for quote in quotes:
        process_quote("Jobber", quote)

    return jsonify({"status": "jobber sync complete", "quotes_synced": len(quotes)}), 200

# -------------------------------
# RUN
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
