from app.utils import fetch_repo_contents, fetch_file_contents
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")


def fetch_repo_and_generate_message(repo_url):
    api_url = repo_url.replace("https://github.com", "https://api.github.com/repos")
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    repo_files = fetch_repo_contents(f"{api_url}/contents", headers)

    file_contents = fetch_file_contents(repo_files, headers)

    message = "Repository Analysis:\n\n"
    message += "Files Retrieved:\n"
    message += "\n".join(file["path"] for file in repo_files) + "\n\n"
    message += "File Contents:\n"
    for file_path, content in file_contents.items():
        message += f"--- {file_path} ---\n{content}...\n\n"

    return message
