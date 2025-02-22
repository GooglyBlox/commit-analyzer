# GitHub Commit Analyzer

A Python application to analyze and display commit history for GitHub repositories with diff stats.

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

## Example

```bash
python github_commit_analyzer.py microsoft/vscode --limit 10
```

This will display the 10 most recent commits from the Microsoft VS Code repository.

## Notes

- This application uses the GitHub REST API v3
- For private repositories, you must provide a GitHub API key with appropriate permissions
- Rate limiting applies based on GitHub's API limits