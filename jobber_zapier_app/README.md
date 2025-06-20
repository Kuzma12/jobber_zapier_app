# README.md

## 📦 Jobber + Zapier + Google Sheets Integration

This is a Flask-based automation app that:
- Pulls quotes from **Zapier** (via Webhook)
- Pulls quotes from **Jobber API** (manual or scheduled)
- Validates math (`unit_cost × quantity`) vs. reported subtotal
- Fixes incorrect subtotals and logs "Fixed" notes
- Matches and organizes client data, dates, and amounts paid
- Logs everything cleanly to a designated **Google Sheet**
- Sends **email notifications** when a new quote is added
- Tracks imports in a `Tracking` tab

---

## 🚀 Features
- ✅ Realtime Zapier Webhook updates
- ✅ Scheduled Jobber quote sync (via endpoint or cron)
- ✅ Google Sheets logging with proper formatting
- ✅ Math correction and validation
- ✅ Notification system (email)

---

## 📁 Project Structure
```
jobber_zapier_app/
├── app.py                      # Main Flask app
├── requirements.txt           # All Python dependencies
├── .env                       # Environment variables
├── Procfile                   # Render deployment
├── your_service_account.json  # Google Sheets API credentials
├── .gitignore                 # Ignore secrets in Git
```

---

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up `.env`
```env
JOBBER_API_TOKEN=your_jobber_token
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_email_app_password
EMAIL_RECIPIENT=you@example.com
GOOGLE_SHEET_NAME=Quote Math Checker
```

### 3. Prepare Google Sheets
- Create a sheet with headers:
  ```
  Source | Quote ID | Client Name | Title | Status | Line Items Count | Reported Subtotal | Calculated Subtotal | Fixed? | Comment | Date | Amount Paid
  ```
- Create a second tab called `Tracking` with:
  ```
  Timestamp | Client Name | Quote ID | Source
  ```
- Share the sheet with your service account (from the JSON file)

### 4. Run App
```bash
python app.py
```

### 5. Trigger Endpoints
- POST from Zapier:
  ```
  https://your-deployment/webhook
  ```
- Sync Jobber manually:
  ```
  https://your-deployment/sync/jobber
  ```

---

## 🌐 Deploy to Render (Free)
- Push project to GitHub
- Go to [https://render.com](https://render.com)
- Click **"New Web Service"**, link your repo
- Set build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Set environment variables in dashboard
- Upload your `your_service_account.json` securely under "Secret Files"

---

## 📬 Example Zapier Payload
```json
{
  "quotes": [
    {
      "id": "123",
      "title": "Insulation Quote",
      "status": "draft",
      "client": {
        "first_name": "Alice",
        "last_name": "Smith"
      },
      "line_items": [
        {"quantity": 2, "unit_cost": 300.00}
      ],
      "subtotal": 600.00,
      "date": "2025-06-20",
      "amount_paid": 300.00
    }
  ]
}
```

---

## 🛠 Optional Enhancements
- Slack or Twilio SMS notifications
- Google Sheets charting tab
- Auto Jobber sync using Render cron or Zapier Scheduler

---

## 🧑‍💻 Maintainer
Built by you with help from ChatGPT 💡

Have questions? Need to deploy it fast? Just ask.
