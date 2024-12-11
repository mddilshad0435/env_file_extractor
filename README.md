# Scan Public GitHub Repositories for `.env` Files and Comment Mentions

## Description

This script identifies exposed `.env` files in public GitHub repositories using the GitHub API and checks if there are any issues or comments mentioning those files. It helps proactively identify potential data leaks and associated risks.

## Features

- Searches for `.env` files in public repositories.
- Checks for issues or comments mentioning these `.env` files.
- Logs the results to both a log file (`scan_env_files.log`) and the console.
- Dynamically handles GitHub API rate limits to prevent request failures.

## Requirements

- Python 3.8+
- A GitHub Personal Access Token (PAT)
- Dependencies: Install via `pip install -r requirements.txt`
  - `requests`
  - `python-dotenv`

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/mddilshad0435/env_file_extractor.git
   cd env_file_extractor

2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt

3. Create a .env file in the project directory with the following content:
    ```env
    GITHUB_TOKEN=your_github_personal_access_token
    
4. Replace your_github_personal_access_token with your GitHub PAT.

## Usage
Run the script using:
```bash
python main.py
```

Output is logged in:
  - `Console`
  - `scan_env_files.log`

##

### Approach to Solving the Problem
1. Authenticate with GitHub:
    - Use a secure GitHub PAT for accessing the API.

2. Search for .env Files:
    - Use the search/code API endpoint with the query filename:.env.

3. Check Mentions:
    - Query repository issues and comments to find mentions of the .env file.

4. Handle Rate Limits:
    - Monitor X-RateLimit-Remaining and delay requests when limits are near.

5. Logging:
    - Record all activities and results for analysis using Python's logging module.

##

### Challenges and Solutions
1. API Rate Limits:
    - Use X-RateLimit-Reset to dynamically handle and delay requests.

2. Search Limitations:
    - Implement efficient querying and pagination for large results.
3. Error Handling:
    - Log and retry failed API requests gracefully.

##

### Future Improvements
1. Add multithreading or async functionality to enhance performance.
2. Extend the search to include other file types (e.g., .json, .yml) containing sensitive information.
3. Automate notifications for detected .env files.