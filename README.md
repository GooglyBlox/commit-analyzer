# GitHub Commit Analyzer

A Python application to analyze and display commit history for GitHub repositories with diff stats.
![image](https://github.com/user-attachments/assets/807d656c-b5ed-45ba-908d-bffa3000b851)

## Requirements

- Python 3.6+
- `requests` library
- `rich` library for console display

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python github_commit_analyzer.py OWNER/REPO [--limit N] [--api-key YOUR_API_KEY]
```

Where:
- `OWNER/REPO` is the repository path (e.g., `octocat/Hello-World`)
- `--limit N` (optional) limits the display to N most recent commits
- `--api-key YOUR_API_KEY` (optional) provides GitHub API key

You can also set your GitHub API key as an environment variable:

```bash
export GITHUB_API_KEY=your_github_api_key
```

## API Key Information

While the tool can work without an API key for public repositories, using an API key is recommended for:

- Higher rate limits (5,000 requests per hour instead of 60)
- Access to private repositories
- More reliable operation

### Without API Key:
- Can only access public repositories
- Limited to 60 requests per hour
- May encounter rate limits with larger repositories

### Getting a GitHub API Key:
1. Go to your GitHub account settings
2. Navigate to Developer settings > Personal access tokens
3. Generate a new token with the `repo` scope
4. Use this token with the `--api-key` option or set it as the `GITHUB_API_KEY` environment variable

## Example

```bash
# With API key
python github_commit_analyzer.py microsoft/vscode --limit 10 --api-key YOUR_API_KEY

# Without API key (public repos only, rate-limited)
python github_commit_analyzer.py microsoft/vscode --limit 10
```

## Notes

- This application uses the GitHub REST API v3
- For private repositories, you must provide a GitHub API key with appropriate permissions
- Rate limiting applies based on GitHub's API limits
