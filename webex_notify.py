# webex_notify.py
import requests
import sys
import os

# --- Configuration ---
ROOM_ID = os.environ.get("Y2lzY29zcGFyazovL3VybjpURUFNOnVzLXdlc3QtMl9yL1JPT00vODEyNDA3NDAtY2Q1ZC0xMWYwLWFkMjctMmY0ZWY5NzZiMjIy")
TOKEN = os.environ.get("YzA2NmZkNDgtYzlhMS00ZjllLWEwZDEtYzYxN2UzYzcwNDY5YTg4YmRkZWYtN2Q4_P0A1_13494cac-24b4-4f89-8247-193cc92a7636") 

if len(sys.argv) < 2:
    print("Error: Build status argument not provided.")
    sys.exit(1)

STATUS = sys.argv[1] 

WEBEX_API = 'https://webexapis.com/v1/messages'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# --- Message Construction ---
build_url = os.environ.get("BUILD_URL", "N/A") 

if STATUS == "FAIL":
    message = "**CODE QUALITY CHECK FAILED!**\n"
    message += f"Please review the build log for Flake8 errors: [View Build]({build_url})"
elif STATUS == "PASS":
    message = "**CODE QUALITY CHECK PASSED!**\n"
    message += "Code is clean and ready for review."
else:
    message = "Unknown build status reported."

# --- API Call ---
payload = {
    "roomId": ROOM_ID,
    "markdown": message
}

try:
    if not TOKEN or not ROOM_ID:
        print("Webex variables not set. Skipping notification.")
        sys.exit(0)
        
    response = requests.post(WEBEX_API, headers=HEADERS, json=payload)
    response.raise_for_status() 
    print(f"Webex notification sent successfully (Status: {STATUS})")
    
except requests.exceptions.RequestException as e:
    print(f"Error sending Webex notification: {e}")
    pass
