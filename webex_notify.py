# webex_notify.py
import requests
import sys
import os

# --- Environment Variables ---
ROOM_ID = os.environ.get("WEBEX_ROOM_ID")
TOKEN = os.environ.get("WEBEX_BOT_TOKEN")
BUILD_URL = os.environ.get("BUILD_URL", "N/A")
FLAKE8_OUTPUT = os.environ.get("FLAKE8_OUTPUT", "")

# --- Check for build status argument ---
if len(sys.argv) < 2:
    print("Error: Build status argument not provided.")
    sys.exit(1)

STATUS = sys.argv[1].upper()  # Expecting 'SUCCESS' or 'FAILURE'

WEBEX_API = 'https://webexapis.com/v1/messages'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# --- Construct the message ---
if STATUS == "SUCCESS":
    message = "**CODE QUALITY CHECK PASSED!** ✅\n"
    message += "Code is clean and ready for review."
elif STATUS == "FAILURE":
    message = "**CODE QUALITY CHECK FAILED!** ❌\n"
    message += f"Please review the build log for Flake8 errors: [View Build]({BUILD_URL})"
else:
    message = "Unknown build status reported."

# Append Flake8 output if available
if FLAKE8_OUTPUT:
    message += f"\n\n**Flake8 Errors:**\n```\n{FLAKE8_OUTPUT}\n```"

# --- Send Webex message ---
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
    sys.exit(1)

