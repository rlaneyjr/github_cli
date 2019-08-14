Command line utility to search github.com's v3 API
==================================================

## Installation
Just use pip like so:
  ``` language bash
  pip install github_cli
  ```

Or clone the repo and add your twist:
  ``` language bash
  git clone https://github.com/rlaneyjr/github_cli.git
  ```

## Quick Run-down:
After installation, you will have two new commands "gh_find" and "gh_list".  Use these two commands perform advanced queries on the Github v3 API.
I wrote this simple script because got tired of typing curl commands that keep getting longer.  Plus I could never remember how to stucture the URLs.
# Example using curl: curl https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc

USAGE_FIND = """gh_find [SEARCH_TYPE] [OPTIONS] QUERY

SEARCH_TYPE:
    repo    -  Find repositories via various criteria (100 results per page max).
    topic   -  Find topics via various criteria (100 results per page max).
    user    -  Find users via various criteria (100 results per page max).

QUERY: Accepts Githubv3 API query.
       Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
       Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
       Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'

OPTIONS:
    -s --sort  Sort by stars, forks, help-wanted-issues,
               or updated. (Optional default=best-match)
    -o --order Order-by desc or asc. (Optional default=desc)
    -c --count Number of items to return. (Optional default=100)
"""

USAGE_LIST = """gh_list [OPTIONS] USER
List public repositories for the specified user.

USER: Github username to list public repositories.

OPTIONS:
    -s --sort  Sort by stars, forks, help-wanted-issues,
               or updated. (Optional default=best-match)
    -c --count Number of items to return. (Optional default=100)
"""

SEARCH_TYPE_HELP = """
SEARCH_TYPE: Identify the type of search you wish to perform.
    repo    -  Find repositories via various criteria (100 results per page max).
    topic   -  Find topics via various criteria (100 results per page max).
    user    -  Find users via various criteria (100 results per page max).
"""

QUERY_HELP = """
QUERY: Accepts Githubv3 API query.
       Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
       Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
       Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'
"""

SORT_CHOICES = ['stars', 'forks', 'help-wanted-issues', 'updated', 'best-match']

INTERESTED_ITEMS = {
    'name': 'none',
    'description': 'none',
    'html_url': 'none',
    'clone_url': 'none',
    'language': 'none',
    'fork': 'none',
    'size': 'none',
    'stargazers_count': 'none',
    'watchers_count': 'none',
    'open_issues_count': 'none',
    'forks': 'none',
    'created_at': 'none',
    'updated_at': 'none'
}

