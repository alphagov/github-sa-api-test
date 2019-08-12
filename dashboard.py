import json
from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from classes.github.github_api_client_v4 import GithubApiClientV4
from classes.github.github_api_client_v3 import GithubApiClientV3

url = "https://api.github.com/graphql"
with open("query.graphql") as query_file:
    query_data = query_file.read()


v4client = GithubApiClientV4()
v3client = GithubApiClientV3()
org = "alphagov"

print("Test get repos query")
repositories = v4client.get_full_repository_list(org)
print(len(repositories))

repositories_by_status = {"ACTIVE": [], "PRIVATE": [], "ARCHIVED": [], "DISABLED": []}


def get_status(org, repo):
    status = None
    if repo.isArchived:
        status = "ARCHIVED"
    elif repo.isDisabled:
        status = "DISABLED"
    elif repo.isPrivate:
        status = "PRIVATE"
    else:
        status = "ACTIVE"

    repositories_by_status[status].append(repo)

    return f"{repo.name}: {status}"


repository_names = [get_status(org, repo) for repo in repositories]

# print(repository_names)

active_count = len(repositories_by_status["ACTIVE"])
private_count = len(repositories_by_status["PRIVATE"])
disabled_count = len(repositories_by_status["DISABLED"])
archived_count = len(repositories_by_status["ARCHIVED"])

print(
    f"ACTIVE: {active_count}\nPRIVATE: {private_count}\n"
    f"DISABLED: {disabled_count}\nARCHIVED: {archived_count}"
)

print(f"VULNERABLE: {len(v4client.get_active_vulnerable(org))}")
