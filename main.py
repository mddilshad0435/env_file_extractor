import requests
import time
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scan_env_files.log"), logging.StreamHandler()],
)

# Load GitHub token from .env file
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("GitHub Personal Access Token not found in .env file.")

# GitHub API base URL
GITHUB_API_URL = "https://api.github.com"
HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}


def search_env_files():
    """Search public repositories for .env files."""
    query = "filename:.env"
    page = 1
    per_page = 100
    results = []
    total_count = 0

    try:
        while True:
            url = f"{GITHUB_API_URL}/search/code"
            params = {"q": query, "page": page, "per_page": per_page}

            logging.info(f"Searching for .env files on page {page}")
            response = requests.get(url, headers=HEADERS, params=params)

            if response.status_code == 403:  # Rate limit hit
                reset_time = int(
                    response.headers.get("X-RateLimit-Reset", time.time() + 60)
                )
                sleep_duration = reset_time - int(time.time())
                logging.warning(
                    f"Rate limit reached. Sleeping for {sleep_duration} seconds..."
                )
                time.sleep(sleep_duration)
                continue

            if response.status_code == 422:
                logging.error("Search query is invalid or timeout occurred")
                break

            response.raise_for_status()
            data = response.json()

            if page == 1:
                total_count = data["total_count"]

            items = data.get("items", [])
            if not items:  # No more results
                break

            results.extend(items)

            if page * per_page >= total_count:
                break

            page += 1

    except requests.exceptions.RequestException as e:
        logging.error(f"Error occurred while searching: {str(e)}")
        return results

    return results


def check_comments_and_issues(repo_full_name, file_path):
    """Check for issues and comments mentioning the .env file in a repository."""
    logging.info(
        f"Checking comments and issues for repo: {repo_full_name}, file: {file_path}"
    )
    issues_url = f"{GITHUB_API_URL}/repos/{repo_full_name}/issues"
    params = {"q": file_path}

    response = requests.get(issues_url, headers=HEADERS, params=params)
    response.raise_for_status()

    return response.json()


def main():
    logging.info("Starting search for .env files in public repositories...")
    env_files = search_env_files()
    if not env_files:
        logging.info("No .env files found.")
        return

    logging.info(
        f"Found {len(env_files)} .env files. Checking for comments and issues..."
    )

    for item in env_files:
        repo_full_name = item["repository"]["full_name"]
        file_path = item["path"]
        file_url = item["html_url"]

        logging.info(f"Repository: {repo_full_name}")
        logging.info(f"File: {file_url}")

        issues = check_comments_and_issues(repo_full_name, file_path)
        if issues:
            logging.info(f"Issues mentioning {file_path}:")
            for issue in issues:
                logging.info(f"- {issue['html_url']} (Title: {issue['title']})")
        else:
            logging.info(f"No issues or comments mentioning {file_path}.")

        logging.info("-" * 70)


if __name__ == "__main__":
    main()
