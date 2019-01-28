#!/usr/bin/env python

import click
import requests
#import json

REPOSITORY_SEARCH_URL = "https://api.github.com/search/repositories?q=",
TOPIC_SEARCH_URL = "https://api.github.com/search/topics?q=",
USER_SEARCH_URL = "https://api.github.com/search/users?q="
USER_REPOSITORIES_URL = "https://api.github.com/users/",

HEADERS = { "Accept": "application/vnd.github.v3+json" }
TOPIC_HEADERS = { "Accept": "application/vnd.github.mercy-preview+json" }
# Example using curl: curl https://api.github.com/search/repositories?q=tetris+language:assembly&sort=stars&order=desc
'''
Note: The topics property for repositories on GitHub is currently available for
developers to preview. To view the topics property in calls that return
repository results, you must provide a custom media type in the Accept header:
application/vnd.github.mercy-preview+json
'''

USAGE = """
github_search --search_type [SEARCH_TYPE] [OPTIONS]
           OR github_search [SEARCH_TYPE] [OPTIONS]

SEARCH_TYPE --search_type(not required) int(1-4):
    1) Find repositories via various criteria (100 results per page max).
    2) Find topics via various criteria (100 results per page max).
    3) Find users via various criteria (100 results per page max).
    4) List public repositories for the specified user.

OPTIONS:
    --query (Required in all searches except user list [4]) Accepts Githubv3 API query.
        Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
        Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
        Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'

    --user (Required only for listing user's repos [4]) Github username.

    --sort (Optional in all searches) Sort by stars, forks, help-wanted-issues,
        or updated (default=best-match).

    --order (Optional in all searches except user list [4]) Order-by desc or asc
        (default=desc)
"""

SEARCH_TYPE_HELP = """
    Identify the type of search you wish to perform.

    1) Find repositories via various criteria (100 results per page max).
    2) Find topics via various criteria (100 results per page max).
    3) Find users via various criteria (100 results per page max).
    4) List public repositories for the specified user.

"""

QUERY_HELP = """
--query (Required in all searches except user list [4]) Accepts Githubv3 API query.
    Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
    Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
    Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'
"""


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(USAGE)
    else:
        pass


@click.option("--query", help=QUERY_HELP, required=True)
@click.option("--order", help="Order-by desc or asc (default=desc)")
@click.option("--sort", help="Sort by stars, forks, help-wanted-issues, or \
        updated (default=best-match)")
def get_search_args():
    pass


@click.option("--user", help="Github username", required=True)
@click.option("--sort", help="Sort by stars, forks, help-wanted-issues, or \
        updated (default=best-match)")
def get_user_list_args():
    pass


def search_github(url, given_args):
    if url == USER_REPOSITORIES_URL and given_args.user:
        headers = HEADERS
        url = f"{url}{args.user}/repos"
        if given_args.sort:
            url = f"{url}?{args.sort}"

    elif url == USER_SEARCH_URL and given_args.query:
        headers = HEADERS
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    elif url == TOPIC_SEARCH_URL and given_args.query:
        headers = TOPIC_HEADERS
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    elif url == REPOSITORY_SEARCH_URL and given_args.query:
        headers = HEADERS
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    else:
        return USAGE

    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if(result.ok):
        repo_info = result.json()
        for key, value in repo_info.iteritems():
            if key in ['name', 'full_name', 'html_url']:
                return value
    else:
         return "No result found!"


@cli.command(invoke_without_command=True)
@click.argument("--search_type", nargs=1, type=click.IntRange(1, 4), default=1,
                required=True)
def get_search_type(search_type):
    if search_type == 1:
        url = REPOSITORY_SEARCH_URL
        headers = HEADERS
        click.echo("Github Find repositories via various criteria (100 results per page max).")
        given_args = get_search_args()
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    elif search_type == 2:
        url = TOPIC_SEARCH_URL
        headers = TOPIC_HEADERS
        click.echo("Github Find topics via various criteria (100 results per page max).")
        given_args = get_search_args()
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    elif search_type == 3:
        url = USER_SEARCH_URL
        headers = HEADERS
        click.echo("Github Find users via various criteria (100 results per page max).")
        given_args = get_search_args()
        url = f"{url}{args.query}"
        if given_args.sort and given_args.order:
            url = f"{url}&{args.sort}&{args.order}"
        elif given_args.sort:
            url = f"{url}&{args.sort}"
        elif given_args.order:
            url = f"{url}&{args.order}"

    elif search_type == 4:
        url = USER_REPOSITORIES_URL
        headers = HEADERS
        click.echo("Github List public repositories for the specified user.")
        given_args = get_user_list_args()
        url = f"{url}{args.user}/repos"
        if given_args.sort:
            url = f"{url}?{args.sort}"

    else:
        #if isinstance(search_type, str):
        #    search_type.convert(search_type, int)
        click.echo(USAGE)
        message = (f"Invalid 'search_type' reference: {search_type}")
        raise click.ClickException(message)

    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if(result.ok):
        repo_info = result.json()
        for key, value in repo_info.iteritems():
            if key in ['name', 'full_name', 'html_url']:
                return value
    else:
        return "No result found!"

if __name__ == '__main__':
    cli()
    # search_type = get_search_type()
    # url, args = get_args(search_type)
    # results = search_github(url, args)
    # print(results)


'''
"current_user_url": "https://api.github.com/user",
"current_user_authorizations_html_url": "https://github.com/settings/connections/applications{/client_id}",
"authorizations_url": "https://api.github.com/authorizations",
"code_search_url": "https://api.github.com/search/code?q={query}{&page,per_page,sort,order}",
"commit_search_url": "https://api.github.com/search/commits?q={query}{&page,per_page,sort,order}",
"emails_url": "https://api.github.com/user/emails",
"emojis_url": "https://api.github.com/emojis",
"events_url": "https://api.github.com/events",
"feeds_url": "https://api.github.com/feeds",
"followers_url": "https://api.github.com/user/followers",
"following_url": "https://api.github.com/user/following{/target}",
"gists_url": "https://api.github.com/gists{/gist_id}",
"hub_url": "https://api.github.com/hub",
"issue_search_url": "https://api.github.com/search/issues?q={query}{&page,per_page,sort,order}",
"issues_url": "https://api.github.com/issues",
"keys_url": "https://api.github.com/user/keys",
"notifications_url": "https://api.github.com/notifications",
"organization_repositories_url": "https://api.github.com/orgs/{org}/repos{?type,page,per_page,sort}",
"organization_url": "https://api.github.com/orgs/{org}",
"public_gists_url": "https://api.github.com/gists/public",
"rate_limit_url": "https://api.github.com/rate_limit",
"repository_url": "https://api.github.com/repos/{owner}/{repo}",
"repository_search_url": "https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}",
"current_user_repositories_url": "https://api.github.com/user/repos{?type,page,per_page,sort}",
"starred_url": "https://api.github.com/user/starred{/owner}{/repo}",
"starred_gists_url": "https://api.github.com/gists/starred",
"team_url": "https://api.github.com/teams",
"user_url": "https://api.github.com/users/{user}",
"user_organizations_url": "https://api.github.com/user/orgs",
"user_repositories_url": "https://api.github.com/users/{user}/repos{?type,page,per_page,sort}",
"user_search_url": "https://api.github.com/search/users?q={query}{&page,per_page,sort,order}"

    result = search_repository(given_args.user, given_args.repo,
                               given_args.query)
    if isinstance(result, dict):
        print("Got result for '{}'...".format(given_args.query))
        for key, value in result.iteritems():
            print("{} => {}".format(key, value))
    else:
        print("Got result for {}: {}".format(given_args.query, result))
'''
