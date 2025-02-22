import requests
import datetime
import os
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

class GitHubCommitAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            'Authorization': f'token {self.api_key}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.console = Console()

    def fetch_commits(self, repo_path, page=1, per_page=100, progress=None, task_id=None):
        """
        Fetch commits from a GitHub repository.
        
        Args:
            repo_path (str): Repository path in format 'owner/repo'
            page (int): Page number for pagination
            per_page (int): Number of commits per page
            progress (Progress, optional): Progress instance for tracking
            task_id: Task ID for the progress instance
            
        Returns:
            list: List of commit data
        """
        url = f'https://api.github.com/repos/{repo_path}/commits'
        params = {
            'page': page,
            'per_page': per_page
        }
        
        if progress and task_id is not None:
            progress.update(task_id, description=f"Fetching commits for {repo_path} (page {page})...")
            
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code != 200:
            self.console.print(f"[bold red]Error fetching commits: {response.status_code}[/bold red]")
            self.console.print(response.json())
            return []
        
        return response.json()
    
    def fetch_commit_details(self, repo_path, commit_sha, progress=None, task_id=None):
        """
        Fetch detailed information about a specific commit.
        
        Args:
            repo_path (str): Repository path in format 'owner/repo'
            commit_sha (str): The SHA of the commit
            progress (Progress, optional): Progress instance for tracking
            task_id: Task ID for the progress instance
            
        Returns:
            dict: Commit details including stats
        """
        url = f'https://api.github.com/repos/{repo_path}/commits/{commit_sha}'
        
        if progress and task_id is not None:
            progress.update(task_id, description=f"Fetching details for commit {commit_sha[:7]}...")
            
        response = requests.get(url, headers=self.headers)
        
        if response.status_code != 200:
            self.console.print(f"[bold red]Error fetching commit details: {response.status_code}[/bold red]")
            return None
        
        return response.json()

    def format_date(self, date_str):
        """Format GitHub API date string to local timezone and readable format."""
        utc_time = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
        
        local_time = utc_time.astimezone(datetime.datetime.now().astimezone().tzinfo)
        
        return local_time.strftime("%Y-%m-%d %H:%M:%S")

    def display_commits(self, repo_path, limit=None):
        """
        Display commits in a visually appealing way with diff stats.
        
        Args:
            repo_path (str): Repository path in format 'owner/repo'
            limit (int, optional): Limit the number of commits to display
        """
        page = 1
        per_page = 100
        all_commits = []
        
        self.console.print(f"[bold blue]Analyzing repository: {repo_path}[/bold blue]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("Loading commits...", total=None)
            
            while True:
                progress.update(task, description=f"Fetching commit page {page}...")
                commits = self.fetch_commits(repo_path, page, per_page, progress, task)
                
                if not commits:
                    break
                
                progress.update(task, description=f"Processing {len(commits)} commits from page {page}...")
                
                for i, commit in enumerate(commits):
                    progress.update(task, description=f"Processing commit {i+1}/{len(commits)} on page {page}...")
                    details = self.fetch_commit_details(repo_path, commit['sha'], progress, task)
                    if details:
                        all_commits.append(details)
                        
                    if limit and len(all_commits) >= limit:
                        break
                
                if limit and len(all_commits) >= limit:
                    break
                    
                if len(commits) < per_page:
                    break
                    
                page += 1
        
        if not all_commits:
            self.console.print("[bold red]No commits found for this repository.[/bold red]")
            return
        
        table = Table(title=f"Commits for {repo_path}")
        
        table.add_column("Date", style="cyan")
        table.add_column("Author", style="green")
        table.add_column("Message", style="bright_white")
        table.add_column("Additions", style="green")
        table.add_column("Deletions", style="red")
        table.add_column("SHA", style="dim")
        
        for commit in all_commits:
            commit_date = self.format_date(commit['commit']['author']['date'])
            author = commit['commit']['author']['name']
            message = commit['commit']['message'].split('\n')[0]
            
            additions = commit['stats']['additions']
            deletions = commit['stats']['deletions']
            
            sha = commit['sha'][:7]
            
            table.add_row(
                commit_date,
                author,
                message,
                f"+{additions}",
                f"-{deletions}",
                sha
            )
        
        self.console.print(table)
        
        total_additions = sum(commit['stats']['additions'] for commit in all_commits)
        total_deletions = sum(commit['stats']['deletions'] for commit in all_commits)
        
        summary = Panel(
            f"[bold]Repository:[/bold] {repo_path}\n"
            f"[bold]Total Commits:[/bold] {len(all_commits)}\n"
            f"[bold]Total Additions:[/bold] [green]+{total_additions}[/green]\n"
            f"[bold]Total Deletions:[/bold] [red]-{total_deletions}[/red]\n"
            f"[bold]Net Change:[/bold] {total_additions - total_deletions:+}",
            title="Summary",
            border_style="blue"
        )
        
        self.console.print(summary)


def main():
    parser = argparse.ArgumentParser(description='Analyze GitHub repository commits')
    parser.add_argument('repo', help='Repository path in format owner/repo')
    parser.add_argument('--limit', type=int, help='Limit the number of commits to display')
    parser.add_argument('--api-key', help='GitHub API Key (can also be set as GITHUB_API_KEY env var)')
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get('GITHUB_API_KEY')
    
    # Uncomment the following lines to hardcode for API key if not provided in args or env var
    # if not api_key:
    #     api_key = ""
        
    analyzer = GitHubCommitAnalyzer(api_key)
    analyzer.display_commits(args.repo, args.limit)


if __name__ == '__main__':
    main()