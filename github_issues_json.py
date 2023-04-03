import requests
import json
from urllib.parse import urlparse, urlsplit
import configargparse as argparse
import os

def fetch_github_issue(owner, repo, issue_number, personal_access_token):
    headers = {
        'Authorization': f'token {personal_access_token}',
        'Accept': 'application/vnd.github+json',
    }

    # Fetch issue data
    issue_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'
    issue_response = requests.get(issue_url, headers=headers)
    issue_data = issue_response.json()

    # Fetch comments data
    comments_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
    comments_response = requests.get(comments_url, headers=headers)
    comments_data = comments_response.json()
    structured_data = {
        'title': issue_data['title'],
        'author': issue_data['user']['login'],
        'timestamp': issue_data['created_at'],
        'body': issue_data['body'],
        'labels': [label['name'] for label in issue_data['labels']],
        'comments': [
            {
                'author': comment['user']['login'],
                'timestamp': comment['created_at'],
                'body': comment['body'],
            } for comment in comments_data
        ],
    }

    return structured_data

def fetch_issues_by_tag(repo_owner, repo_name, label, personal_access_token):
    issues_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {personal_access_token}"
    }
    params = None
    if label == "all":
        pass
    else:
        params = {
            "state": "all",
            "labels": label
        }

    response = requests.get(issues_url, headers=headers, params=params)
    response.raise_for_status()

    issues = response.json()
    return issues

def create_structured_issues_data(raw_issues):
    structured_issues = []

    for issue in raw_issues:
        labels = [label["name"] for label in issue["labels"]]
        structured_issue = {
            "title": issue["title"],
            "author": issue["user"]["login"],
            "timestamp": issue["created_at"],
            "body": issue["body"],
            "labels": labels
        }
        structured_issues.append(structured_issue)

    return structured_issues

def main():
    parser = argparse.ArgumentParser(description="GitHub Issue Extractor")
    parser.add_argument("url", help="URL of the GitHub issue")
    parser.add_argument("--tag", help="Filter issues by tag")

    args = parser.parse_args()
    issue_url = args.url
    tag = args.tag

    personal_access_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not personal_access_token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")

    parsed_url = urlparse(issue_url)
    if not parsed_url.netloc == "github.com":
        raise ValueError("Invalid GitHub URL")

    path_parts = parsed_url.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid issue URL format")


    if tag:
        repo_owner, repo_name = path_parts[:2]
        issues = fetch_issues_by_tag(repo_owner, repo_name, tag, personal_access_token)
        print(issues)
    else:
        # Call the issue extraction function with the repo_owner, repo_name, issue_number, and personal_access_token
        repo_owner, repo_name, _, issue_number = path_parts
        issue = fetch_github_issue(repo_owner, repo_name, issue_number, personal_access_token)
        structured_issue = create_structured_issues_data(issue)
        print(structured_issue)
if __name__ == "__main__":
    main()
