# webex_notify.py
import requests
import sys
import os

# --- Configuration ---
ROOM_ID = os.environ.get("WEBEX_ROOM_ID")
TOKEN = os.environ.get("WEBEX_BOT_TOKEN")
FLAKE8_OUTPUT = os.environ.get("FLAKE8_OUTPUT", "")

if len(sys.argv) < 2:
    print("Error: Build status argument not provided.")
    sys.exit(1)

STATUS = sys.argv[1] 
BUILD_URL = os.environ.get("BUILD_URL", "N/A")
WEBEX_API = 'https://webexapis.com/v1/messages'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# --- Message Construction ---
if STATUS == "FAILURE":
    message = "**CODE QUALITY CHECK FAILED!**\n"
    if FLAKE8_OUTPUT:
        message += f"```\n{FLAKE8_OUTPUT}\n```"
    else:
        message += f"Flake8 errors exist but could not be captured.\nBuild URL: {BUILD_URL}"
elif STATUS == "SUCCESS":
    message = "**CODE QUALITY CHECK PASSED!**\nCode is clean and ready for review."
else:
    message = "Unknown build status reported."

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

