#!/usr/bin/env python

import click
import requests
import json

REPOSITORY_SEARCH_URL = "https://api.github.com/search/repositories?q="
TOPIC_SEARCH_URL = "https://api.github.com/search/topics?q="
USER_SEARCH_URL = "https://api.github.com/search/users?q="
USER_REPOSITORIES_URL = "https://api.github.com/users/"

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
gh-find [SEARCH_TYPE] [OPTIONS]

SEARCH_TYPE:
    repo - Find repositories via various criteria (100 results per page max).
    topic -  Find topics via various criteria (100 results per page max).
    user -  Find users via various criteria (100 results per page max).
    list -  List public repositories for the specified user.

OPTIONS:
    --query (Required in all search types except 'list') Accepts Githubv3 API query.
        Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
        Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
        Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'

    --user (Required only for search type 'list') Github username.

    --sort (Optional in all search types) Sort by stars, forks, help-wanted-issues,
        or updated (default=best-match).

    --order (Optional in all search types except 'list') Order-by desc or asc
        (default=desc)
"""

SEARCH_TYPE_HELP = """
    Identify the type of search you wish to perform.

SEARCH_TYPE:
    find-repo - Find repositories via various criteria (100 results per page max).
    find-topic -  Find topics via various criteria (100 results per page max).
    find-user -  Find users via various criteria (100 results per page max).
    list-user -  List public repositories for the specified user.

"""

QUERY_HELP = """
--query (Required in all search types except 'list') Accepts Githubv3 API query.
    Format: 'SEARCH_KEYWORD_1+SEARCH_KEYWORD_N+QUALIFIER_1+QUALIFIER_N'
    Examples: 'GitHub+Octocat+in:readme+user:defunkt' or 'tetris+language:assembly'
    Details: 'https://developer.github.com/v3/search/#constructing-a-search-query'
"""

CONTEXT_SETTINGS = dict(token_normalize_func=lambda x: x.lower())


def search_github(url, headers=None):
    result = requests.get(url, headers=headers)
    print(f"Searching URL: {url}")
    if(result.ok):
        keep_list = []
        repo_info = result.json()
        for item in repo_info['items']:
            keep_list.append(item)
            #for key, value in item.items():
            #    if key in ['name', 'full_name', 'html_url']:
            #        keep_list.append(dict((key, item)))
        return keep_list
    else:
        return "No result found!"


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo(USAGE)
    else:
        pass


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("query", required=True)
@click.option("--sort", help="Sort by stars, forks, help-wanted-issues, or \
              updated (default=best-match)")
@click.option("--order", help="Order-by desc or asc (default=desc)")
def find_repo(query, sort, order):
    url = REPOSITORY_SEARCH_URL
    click.echo("Github Find repositories via various criteria (100 results per page max).")
    url = f"{url}{query}"
    if sort and order:
        url = f"{url}&{sort}&{order}"
    elif sort:
        url = f"{url}&{sort}"
    elif order:
        url = f"{url}&{order}"
    results = json.loads(search_github(url))
    return print(results)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("query", required=True)
@click.option("--sort", help="Sort by stars, forks, help-wanted-issues, or \
              updated (default=best-match)")
@click.option("--order", help="Order-by desc or asc (default=desc)")
def find_topic(query, sort, order):
    url = TOPIC_SEARCH_URL
    headers = TOPIC_HEADERS
    click.echo("Github Find topics via various criteria (100 results per page max).")
    url = f"{url}{query}"
    if sort and order:
        url = f"{url}&{sort}&{order}"
    elif sort:
        url = f"{url}&{sort}"
    elif order:
        url = f"{url}&{order}"
    return search_github(url, headers=headers)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("query", required=True)
@click.option("--sort", help="Sort by stars, forks, help-wanted-issues, or \
              updated (default=best-match)")
@click.option("--order", help="Order-by desc or asc (default=desc)")
def find_user(query, sort, order):
    url = USER_SEARCH_URL
    click.echo("Github Find users via various criteria (100 results per page max).")
    url = f"{url}{query}"
    if sort and order:
        url = f"{url}&{sort}&{order}"
    elif sort:
        url = f"{url}&{sort}"
    elif order:
        url = f"{url}&{order}"
    return search_github(url)


@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument("username", required=True)
@click.option("-s", "--sort", help="Sort by stars, forks, help-wanted-issues, or \
              updated (default=best-match)")
def list_user(username, sort):
    url = USER_REPOSITORIES_URL
    click.echo("Github List public repositories for the specified user.")
    url = f"{url}{username}/repos"
    if sort:
        url = f"{url}?{sort}"
    return search_github(url)


if __name__ == '__main__':
    cli()


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
