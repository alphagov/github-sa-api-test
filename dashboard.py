from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

url = 'https://api.github.com/graphql'
with open('query.graphql') as query_file:
    query_data = query_file.read()

with open('token') as token_file:
    api_token = token_file.read().replace("\n", "")

_transport = RequestsHTTPTransport(
    url=url,
    use_json=True,
    headers={
        'Authorization': 'token %s' % api_token,
        'Accept': "application/vnd.github.vixen-preview+json"
    }
)

client = Client(
    transport=_transport,
    fetch_schema_from_transport=True,
)
query = gql(query_data)
from pprint import pprint
results = Dict(client.execute(query))

vulnerable_nodes = [
    node
    for node
    in results.organization.repositories.nodes
    if node.vulnerabilityAlerts.edges]

import json
print(json.dumps(vulnerable_nodes, indent=4))
