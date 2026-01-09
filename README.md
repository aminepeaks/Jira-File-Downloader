# Jira File Downloader

Simple internal script to download attachments from Jira issues for project `TRK`.

## Requirements

- Python 3.8+
- A working `requirements.txt` (already provided)

## Quick setup (macOS / zsh)

1. Create a virtual environment:

```bash
python3 -m venv .venv
```

2. Activate it:

```bash
source .venv/bin/activate
```

3. Upgrade pip and install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Ensure environment variables are set. At minimum set:

- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_BASE_URL` (e.g. https://yourcompany.atlassian.net/)
- `JIRA_PROJECT_KEY` (should be `TRK`)

You can export them in the shell or create a `.env` file and load them before running.

Create a `.env` file (recommended for local use). Example `.env` contents:


Or export temporarily in the shell (do NOT commit secrets):

```bash
export JIRA_EMAIL=you@example.com
export JIRA_API_TOKEN=xxxxxxxxxxxxxxxx
export JIRA_BASE_URL=https://yourcompany.atlassian.net/
export JIRA_PROJECT_KEY=TRK
```

To get the API token, Click on the user icon (top right) > Account settings > Security > Create and manage API tokens > Create API token.


## Run

With the venv active and env vars set:

```bash
python main.py
```

Follow prompts to enter the issue number (e.g. `123`) — the script will use the configured project key and download attachments to `downloads/`.

## Notes

- This repository is for internal use; keep credentials secret.
- To deactivate the venv:‰

```bash
deactivate
```
