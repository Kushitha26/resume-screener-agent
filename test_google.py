import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# 1. Auth scopes
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# 2. Load credentials.json (must be in same folder as this script)
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# 3. Open sheet BY URL (more reliable than open("title"))
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1F0l1wKxvitTcAqGjroYYVk8M2ZP0mMTS6hekToEdiFY/edit?gid=0#gid=0"
).sheet1

# 4. Dummy data to test
data = pd.DataFrame({
    "Name": ["Kushitha", "Virinchy"],
    "Score": [92, 76]
})

# 5. Write headers + rows into sheet
sheet.clear()
sheet.update([data.columns.values.tolist()] + data.values.tolist())

print("✅ Successfully wrote to Google Sheet!")
