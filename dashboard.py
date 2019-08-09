import json
from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from classes.github.github_api_client_v4 import GithubApiClientV4
from classes.github.github_api_client_v3 import GithubApiClientV3

url = 'https://api.github.com/graphql'
with open('query.graphql') as query_file:
    query_data = query_file.read()

# with open('token') as token_file:
#     api_token = token_file.read().replace("\n", "")
#
# _transport = RequestsHTTPTransport(
#     url=url,
#     use_json=True,
#     headers={
#         'Authorization': 'token %s' % api_token,
#         'Accept': "application/vnd.github.vixen-preview+json"
#     }
# )
#
# client = Client(
#     transport=_transport,
#     fetch_schema_from_transport=True,
# )
# query = gql(query_data)
# from pprint import pprint
# results = Dict(client.execute(query))



v4client = GithubApiClientV4()
# results = v4client.post(query_data)
#
# vulnerable_nodes = [
#     node
#     for node
#     in results.organization.repositories.nodes
#     if node.vulnerabilityAlerts.edges]
#
# print(json.dumps(vulnerable_nodes, indent=4))
#
#
v3client = GithubApiClientV3()
org = "alphagov"
# repo = "csw-backend"
#
# repo_info = f"/repos/{org}/{repo}"
# alert_status = f"/repos/{org}/{repo}/vulnerability-alerts"
#
# response = v3client.get(repo_info)
# print(response.json())
#
# response_alerts = v3client.get(alert_status)
# print(response_alerts.status_code)

print ("Test get repos query")
repositories = v4client.get_full_repository_list(org)
print(len(repositories))

repositories_by_status = {
    "ACTIVE": [],
    "PRIVATE": [],
    "ARCHIVED": [],
    "DISABLED": []
}

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

repository_names = [
    get_status(org, repo)
    for repo
    in repositories]

print(repository_names)

active_count = len(repositories_by_status["ACTIVE"])
private_count = len(repositories_by_status["PRIVATE"])
disabled_count = len(repositories_by_status["DISABLED"])
archived_count = len(repositories_by_status["ARCHIVED"])

print(f'ACTIVE: {active_count}\nPRIVATE: {private_count}\n'
        f'DISABLED: {disabled_count}\nARCHIVED: {archived_count}')
