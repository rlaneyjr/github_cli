#!/usr/bin/env python

import click
import requests

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

