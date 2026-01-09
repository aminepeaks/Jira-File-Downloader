import os
import base64
import requests
from pathlib import Path

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # If python-dotenv isn't installed, continue — user can set env vars manually
    pass

# -----------------------------
# Configuration
# -----------------------------
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

if not all([JIRA_EMAIL, JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_PROJECT_KEY]):
    missing = [
        var_name for var_name, var_value in [
            ("JIRA_EMAIL", JIRA_EMAIL),
            ("JIRA_API_TOKEN", JIRA_API_TOKEN),
            ("JIRA_BASE_URL", JIRA_BASE_URL),
            ("JIRA_PROJECT_KEY", JIRA_PROJECT_KEY)
        ] if not var_value
    ]
    raise EnvironmentError(
        "Missing one or more environment variables: "
        + ", ".join(missing)
    )

# -----------------------------
# Auth header
# -----------------------------
auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
auth_b64 = base64.b64encode(auth_str.encode()).decode()

HEADERS = {
    "Authorization": f"Basic {auth_b64}",
    "Accept": "application/json"
}

# -----------------------------
# Helpers
# -----------------------------
def get_issue(issue_key):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def list_attachments(issue):
    return issue.get("fields", {}).get("attachment", [])

def download_attachment(attachment, download_dir="downloads"):
    url = attachment["content"]
    filename = attachment["filename"]

    Path(download_dir).mkdir(parents=True, exist_ok=True)
    file_path = Path(download_dir) / filename

    print(f"\n⬇️ Downloading: {filename}")

    with requests.get(url, headers=HEADERS, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    print(f"✅ Saved to: {file_path.resolve()}")

# -----------------------------
# Main
# -----------------------------
def main():
    user_input = input(
        f"Enter Jira issue number (e.g. 123). Project will be {JIRA_PROJECT_KEY}: "
    ).strip()

    # Accept either a plain number (e.g. "123") or a full key (e.g. "TRK-123").
    if "-" in user_input:
        _, id_part = user_input.split("-", 1)
    else:
        id_part = user_input

    if not id_part:
        print("Invalid issue identifier.")
        return

    issue_key = f"{JIRA_PROJECT_KEY}-{id_part}"

    issue = get_issue(issue_key)
    attachments = list_attachments(issue)

    if not attachments:
        print("❌ No attachments found on this issue.")
        return

    print(f"\n📎 Attachments for {issue_key}:\n")

    for idx, att in enumerate(attachments, start=1):
        size_mb = att["size"] / (1024 * 1024)
        print(
            f"{idx}. {att['filename']} "
            f"({size_mb:.2f} MB) "
            f"- uploaded by {att['author']['displayName']}"
        )

    while True:
        try:
            choice = int(input("\nSelect attachment number to download: "))
            if 1 <= choice <= len(attachments):
                break
            print("Invalid selection.")
        except ValueError:
            print("Please enter a number.")

    selected_attachment = attachments[choice - 1]
    download_attachment(selected_attachment)

if __name__ == "__main__":
    main()
