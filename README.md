#GitHub Issue Extractor

GitHub Issue Extractor is a Python script that extracts information about GitHub issues and provides it in a structured format. You can extract a single issue's data or fetch all issues of a repository filtered by a tag.
##Features

    Extract a single GitHub issue's data
    Fetch all issues of a repository filtered by a tag
    Convert raw JSON data into a more digestible, structured format

##Requirements

    Nix package manager with flakes enabled

##Installation

    Clone the repository:

``` bash
git clone https://github.com/ford-perfect/github_issues_xd
cd github_issues_xd
nix develop
```


Usage

    Set the GITHUB_PERSONAL_ACCESS_TOKEN environment variable in the shell or put it in the .env file in the root directory of the project:

bash

``` bash
export GITHUB_PERSONAL_ACCESS_TOKEN=your_personal_access_token
```


    Extract a single GitHub issue's data:

bash
```
python main.py "https://github.com/owner/repo/issues/123"
```


    Fetch all issues of a repository filtered by a tag:

bash

```
python main.py "https://github.com/owner/repo" --tag "your_tag"
```


##Customization

You can customize the script by modifying the create_structured_issues_data and create_structured_issue_data functions to change the structured format of the issue data.

##License

This project is licensed under the GNU General Public License v.3.0
