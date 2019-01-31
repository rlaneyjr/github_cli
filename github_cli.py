#!/usr/bin/env python

import click
import requests
#import json

REPOSITORY_SEARCH_URL = "https://api.github.com/search/repositories?q="
TOPIC_SEARCH_URL = "https://api.github.com/search/topics?q="
USER_SEARCH_URL = "https://api.github.com/search/users?q="
USER_REPOSITORIES_URL = "https://api.github.com/users/"

HEADERS = { "Accept": "application/vnd.github.v3+json" }
TOPIC_HEADERS = { "Accept": "application/vnd.github.mercy-preview+json" }
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


def search_user(url, headers=HEADERS):
    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if(result.ok):
        repo_info = result.json()
        for item in repo_info:
            for k, v in item.items():
                click.echo(click.style(f"{k} => {v}", fg='cyan'))


def search_github(url, headers=HEADERS):
    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if(result.ok):
        repo_info = result.json()
        if isinstance(repo_info, dict):
            print_item({'total': repo_info['total_count']})
            print_item({'incomplete_results': repo_info['incomplete_results']})
            with click.progressbar(repo_info['items'], label='Items') as r_items:
                for item in r_items:
                    print_keeper(item)
        elif isinstance(repo_info, list):
            with click.progressbar(repo_info, label='Items') as r_items:
                for item in r_items:
                    print_keeper(item)
        else:
            click.echo(click.style("No result found!", fg='red'))
    else:
        click.echo(click.style(result.raise_for_status(), fg='red'))


def print_keeper(stuff):
    keeper = INTERESTED_ITEMS
    click.echo(click.style(("=" * 20), fg='cyan'))
    for k,v in stuff.items():
        if k in keeper.keys():
            click.echo(click.style(f"{k} => {v}", fg='cyan'))


def print_item(item):
    for k, v in item.items():
        click.echo(click.style(f"{k} => {v}", fg='cyan'))


def process_query_url(url, query, sort, order, count):
    if not url or not query:
        msg = f"You must provide both the URL and a QUERY!\n{USAGE_FIND}"
        raise click.exceptions.ClickException(click.style(msg, fg='white',
                                              bg='red'))
    url = f"{url}{query}&per_page={count}"
    if sort and order:
        url = f"{url}&{sort}&{order}"
    elif sort:
        url = f"{url}&{sort}"
    elif order:
        url = f"{url}&{order}"
    return url


@click.group()
def cli():
    """Main manager group
    """


@cli.group('gh_find', invoke_without_command=True)
@click.pass_context
def gh_find(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(USAGE_FIND)
    else:
        pass


@gh_find.command('repo', short_help="Find github repos.", help=SEARCH_TYPE_HELP)
@click.argument("query")
@click.option("-s", "--sort", type=click.Choice(SORT_CHOICES),
              help="Sort by stars, forks, help-wanted-issues, or updated \
                   (default=best-match)")
@click.option("-o", "--order", type=click.Choice(['asc', 'desc']),
              help="Order-by desc or asc (default=desc)")
@click.option("-c", "--count", type=click.IntRange(1, 100), default=100,
              help="Number of items to return (default=100)")
def find_repo(query, sort, order, count):
    url = process_query_url(REPOSITORY_SEARCH_URL, query, sort, order, count)
    click.echo("Find repositories via various criteria (100 results per page max).")
    return search_github(url)


@gh_find.command('topic', short_help="Find github topics.", help=SEARCH_TYPE_HELP)
@click.argument("query")
@click.option("-s", "--sort", type=click.Choice(SORT_CHOICES),
              help="Sort by stars, forks, help-wanted-issues, or updated \
                   (default=best-match)")
@click.option("-o", "--order", type=click.Choice(['asc', 'desc']),
              help="Order-by desc or asc (default=desc)")
@click.option("-c", "--count", type=click.IntRange(1, 100), default=100,
              help="Number of items to return (default=100)")
def find_topic(query, sort, order, count):
    url = process_query_url(TOPIC_SEARCH_URL, query, sort, order, count)
    headers = TOPIC_HEADERS
    click.echo("Find topics via various criteria (100 results per page max).")
    return search_github(url, headers=headers)


@gh_find.command('user', short_help="Find github users.", help=SEARCH_TYPE_HELP)
@click.argument("query")
@click.option("-s", "--sort", type=click.Choice(SORT_CHOICES),
              help="Sort by stars, forks, help-wanted-issues, or updated \
                   (default=best-match)")
@click.option("-o", "--order", type=click.Choice(['asc', 'desc']),
              help="Order-by desc or asc (default=desc)")
@click.option("-c", "--count", type=click.IntRange(1, 100), default=100,
              help="Number of items to return (default=100)")
def find_user(query, sort, order, count):
    url = process_query_url(USER_SEARCH_URL, query, sort, order, count)
    click.echo("Find users via various criteria (100 results per page max).")
    return search_github(url)


@cli.command('gh_list', short_help="List users repos.", help=USAGE_LIST)
@click.argument("username")
@click.option("-s", "--sort", help="Sort by stars, forks, help-wanted-issues, or \
              updated (default=best-match)")
@click.option("-c", "--count", type=click.IntRange(1, 100), default=100,
              help="Number of items to return (default=100)")
def gh_list(username, sort, count):
    url = USER_REPOSITORIES_URL
    click.echo("List public repositories for the specified user.")
    url = f"{url}{username}/repos?per_page={count}"
    if sort:
        url = f"{url}?{sort}"
    return search_github(url)


'''
❯❯❯ curl -i https://api.github.com/search/repositories?q=netbox
HTTP/1.1 200 OK
Server: GitHub.com
Date: Tue, 29 Jan 2019 12:55:41 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 182679
Status: 200 OK
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1548766600
Cache-Control: no-cache
X-GitHub-Media-Type: github.v3; format=json
Link: <https://api.github.com/search/repositories?q=netbox&page=2>; rel="next", <https://api.github.com/search/repositories?q=netbox&page=8>; rel="last"
Access-Control-Expose-Headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type
Access-Control-Allow-Origin: *
Strict-Transport-Security: max-age=31536000; includeSubdomains; preload
X-Frame-Options: deny
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: origin-when-cross-origin, strict-origin-when-cross-origin
Content-Security-Policy: default-src 'none'
X-GitHub-Request-Id: C531:1A5F:38F218:73FA5A:5C504D4C

{
  "total_count": 229,
  "incomplete_results": false,
  "items": [
    {
      "id": 52796596,
      "node_id": "MDEwOlJlcG9zaXRvcnk1Mjc5NjU5Ng==",
      "name": "netbox",
      "full_name": "digitalocean/netbox",
      "private": false,
      "owner": {
        "login": "digitalocean",
        "id": 4650108,
        "node_id": "MDEyOk9yZ2FuaXphdGlvbjQ2NTAxMDg=",
        "avatar_url": "https://avatars0.githubusercontent.com/u/4650108?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/digitalocean",
        "html_url": "https://github.com/digitalocean",
        "followers_url": "https://api.github.com/users/digitalocean/followers",
        "following_url": "https://api.github.com/users/digitalocean/following{/other_user}",
        "gists_url": "https://api.github.com/users/digitalocean/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/digitalocean/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/digitalocean/subscriptions",
        "organizations_url": "https://api.github.com/users/digitalocean/orgs",
        "repos_url": "https://api.github.com/users/digitalocean/repos",
        "events_url": "https://api.github.com/users/digitalocean/events{/privacy}",
        "received_events_url": "https://api.github.com/users/digitalocean/received_events",
        "type": "Organization",
        "site_admin": false
      },
      "html_url": "https://github.com/digitalocean/netbox",
      "description": "IP address management (IPAM) and data center infrastructure management (DCIM) tool.",
      "fork": false,
      "url": "https://api.github.com/repos/digitalocean/netbox",
      "forks_url": "https://api.github.com/repos/digitalocean/netbox/forks",
      "keys_url": "https://api.github.com/repos/digitalocean/netbox/keys{/key_id}",
      "collaborators_url": "https://api.github.com/repos/digitalocean/netbox/collaborators{/collaborator}",
      "teams_url": "https://api.github.com/repos/digitalocean/netbox/teams",
      "hooks_url": "https://api.github.com/repos/digitalocean/netbox/hooks",
      "issue_events_url": "https://api.github.com/repos/digitalocean/netbox/issues/events{/number}",
      "events_url": "https://api.github.com/repos/digitalocean/netbox/events",
      "assignees_url": "https://api.github.com/repos/digitalocean/netbox/assignees{/user}",
      "branches_url": "https://api.github.com/repos/digitalocean/netbox/branches{/branch}",
      "tags_url": "https://api.github.com/repos/digitalocean/netbox/tags",
      "blobs_url": "https://api.github.com/repos/digitalocean/netbox/git/blobs{/sha}",
      "git_tags_url": "https://api.github.com/repos/digitalocean/netbox/git/tags{/sha}",
      "git_refs_url": "https://api.github.com/repos/digitalocean/netbox/git/refs{/sha}",
      "trees_url": "https://api.github.com/repos/digitalocean/netbox/git/trees{/sha}",
      "statuses_url": "https://api.github.com/repos/digitalocean/netbox/statuses/{sha}",
      "languages_url": "https://api.github.com/repos/digitalocean/netbox/languages",
      "stargazers_url": "https://api.github.com/repos/digitalocean/netbox/stargazers",
      "contributors_url": "https://api.github.com/repos/digitalocean/netbox/contributors",
      "subscribers_url": "https://api.github.com/repos/digitalocean/netbox/subscribers",
      "subscription_url": "https://api.github.com/repos/digitalocean/netbox/subscription",
      "commits_url": "https://api.github.com/repos/digitalocean/netbox/commits{/sha}",
      "git_commits_url": "https://api.github.com/repos/digitalocean/netbox/git/commits{/sha}",
      "comments_url": "https://api.github.com/repos/digitalocean/netbox/comments{/number}",
      "issue_comment_url": "https://api.github.com/repos/digitalocean/netbox/issues/comments{/number}",
      "contents_url": "https://api.github.com/repos/digitalocean/netbox/contents/{+path}",
      "compare_url": "https://api.github.com/repos/digitalocean/netbox/compare/{base}...{head}",
      "merges_url": "https://api.github.com/repos/digitalocean/netbox/merges",
      "archive_url": "https://api.github.com/repos/digitalocean/netbox/{archive_format}{/ref}",
      "downloads_url": "https://api.github.com/repos/digitalocean/netbox/downloads",
      "issues_url": "https://api.github.com/repos/digitalocean/netbox/issues{/number}",
      "pulls_url": "https://api.github.com/repos/digitalocean/netbox/pulls{/number}",
      "milestones_url": "https://api.github.com/repos/digitalocean/netbox/milestones{/number}",
      "notifications_url": "https://api.github.com/repos/digitalocean/netbox/notifications{?since,all,participating}",
      "labels_url": "https://api.github.com/repos/digitalocean/netbox/labels{/name}",
      "releases_url": "https://api.github.com/repos/digitalocean/netbox/releases{/id}",
      "deployments_url": "https://api.github.com/repos/digitalocean/netbox/deployments",
      "created_at": "2016-02-29T14:15:46Z",
      "updated_at": "2019-01-29T05:48:58Z",
      "pushed_at": "2019-01-29T05:48:55Z",
      "git_url": "git://github.com/digitalocean/netbox.git",
      "ssh_url": "git@github.com:digitalocean/netbox.git",
      "clone_url": "https://github.com/digitalocean/netbox.git",
      "svn_url": "https://github.com/digitalocean/netbox",
      "homepage": "",
      "size": 8777,
      "stargazers_count": 4783,
      "watchers_count": 4783,
      "language": "Python",
      "has_issues": true,
      "has_projects": false,
      "has_downloads": true,
      "has_wiki": true,
      "has_pages": false,
      "forks_count": 886,
      "mirror_url": null,
      "archived": false,
      "open_issues_count": 132,
      "license": {
        "key": "apache-2.0",
        "name": "Apache License 2.0",
        "spdx_id": "Apache-2.0",
        "url": "https://api.github.com/licenses/apache-2.0",
        "node_id": "MDc6TGljZW5zZTI="
      },
      "forks": 886,
      "open_issues": 132,
      "watchers": 4783,
      "default_branch": "develop",
      "score": 170.0116
    }
'''
