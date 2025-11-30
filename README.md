# Code Quality Checker Project

This project demonstrates automated code quality checks for Python applications using **Flake8**, integrated with Jenkins, Docker, and Webex notifications. The goal is to show how an automated pipeline can detect coding errors and style violations, enforce consistent coding standards, and notify the development team in real-time about the build and code quality status. 

The workflow starts with cloning the repository, building a Docker image with Python, Flake8, and the application files, running Flake8 inside the container to detect code issues, and sending a Webex notification to the team containing the results.

## Sample Application: `sample_app.py`

The sample Python application includes deliberate Flake8 errors for demonstration. It imports `os` and `json`, but `json` is unused (F401). The `AppConfig` class has multiple spaces after a comment and in an assignment (E261/E262). The dictionary `user_data` contains extra spaces before a colon (E201). There may also be indentation warnings if extra blank lines or spaces exist. After correcting these issues, Flake8 reports no errors, indicating a clean codebase.

```python
# sample_app.py
import os 
import json # Flake8 will flag 'json' as unused (F401 error)

class AppConfig:
    """Basic configuration settings."""
    # Flake8 will check for multiple spaces after the '#' (E261/E262 error)
    DEFAULT_TIMEOUT  = 30 
    
    def __init__(self, debug_mode):
        self.debug = debug_mode

# A dictionary with an extra space before the colon (E201 error)
user_data = {
    'name' : 'Alice',
    'status': 'active'
}

def process_config(config):
    if config.debug:
        print("Debug mode enabled. Timeout:", config.DEFAULT_TIMEOUT)
    return True

config_instance = AppConfig(debug_mode=True)

if process_config(config_instance):
    print("Configuration processed successfully.")
```

Running Flake8 on this file highlights the following issues:  
- `F401`: Unused import `json`.  
- `E261/E262`: Multiple spaces after comments.  
- `E201`: Whitespace before colon in dictionary key `'name' : 'Alice'`.  
- Indentation warnings if extra blank lines or spaces exist.  

After correcting these issues, Flake8 reports no errors, indicating the code is clean.

## Dockerfile

The Dockerfile sets up a Python 3.9 slim container, copies the project files, and installs Flake8 and `requests` (needed for Webex notifications). This ensures a reproducible environment for the Flake8 checks.

```dockerfile
FROM python:3.9-slim

WORKDIR /var/jenkins_home/workspace/Code-Quality-Checker-Project

COPY . .

RUN pip install flake8 requests
```

## Webex Notification Script: `webex_notify.py`

This Python script sends build status notifications to a Webex room. It reads the following environment variables: `WEBEX_ROOM_ID`, `WEBEX_BOT_TOKEN`, `BUILD_URL`, and optional `FLAKE8_OUTPUT`. It expects a build status argument (`SUCCESS` or `FAILURE`) and constructs a message. Flake8 errors are included if present. The message is sent using the Webex API, and any errors in sending are handled.

```python
# webex_notify.py
import requests
import sys
import os

ROOM_ID = os.environ.get("WEBEX_ROOM_ID")
TOKEN = os.environ.get("WEBEX_BOT_TOKEN")
BUILD_URL = os.environ.get("BUILD_URL", "N/A")
FLAKE8_OUTPUT = os.environ.get("FLAKE8_OUTPUT", "")

if len(sys.argv) < 2:
    print("Error: Build status argument not provided.")
    sys.exit(1)

STATUS = sys.argv[1].upper()  

WEBEX_API = 'https://webexapis.com/v1/messages'
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

if STATUS == "SUCCESS":
    message = "**CODE QUALITY CHECK PASSED!** ✅\nCode is clean and ready for review."
elif STATUS == "FAILURE":
    message = f"**CODE QUALITY CHECK FAILED!** ❌\nPlease review the build log for Flake8 errors: [View Build]({BUILD_URL})"
else:
    message = "Unknown build status reported."

if FLAKE8_OUTPUT:
    message += f"\n\n**Flake8 Errors:**\n```\n{FLAKE8_OUTPUT}\n```"

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
```

## Jenkins Pipeline

The Jenkins pipeline automates the code quality check workflow. It consists of the following stages:

1. **Checkout Code & Fix Permissions**: Clones the repository and fixes permissions for `webex_notify.py`.  
2. **Build Docker Image**: Builds a Docker image containing Python, Flake8, and the project files.  
3. **Run Flake8 Quality Check**: Executes Flake8 inside the Docker container. If any errors are detected, the build fails.  
4. **Post Build Actions**: Sends a Webex notification with the build status (`PASS` or `FAIL`) and Flake8 output.

This pipeline ensures that all commits are automatically validated, coding standards are enforced, and the team is notified in real-time.

## Benefits

This project provides automated code review, reducing human errors in style and formatting. Continuous integration ensures that all commits are validated. Team communication is improved through real-time notifications via Webex. Docker ensures a reproducible environment with consistent builds across machines.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/amanimaran14/devops-final-assignment.git
cd devops-final-assignment
```

Configure Jenkins with Docker installed on the host, the Webex Bot Token stored as a secret, and the Webex Room ID set in the pipeline environment. Trigger the Jenkins build to observe Flake8 results. The initial run will show Flake8 errors. Fix the errors and re-run to confirm a successful build.

This setup ensures consistent code quality across all commits.

## Contact

For any questions about this project, please reach out to **Ashween Manimaran**.
