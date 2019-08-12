from string import Template

from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


url = "https://api.github.com/graphql"
with open("query/all.graphql") as query_file:
    query_data = query_file.read()

with open("token") as token_file:
    api_token = token_file.read().replace("\n", "")

_transport = RequestsHTTPTransport(
    url=url,
    use_json=True,
    headers={
        "Authorization": "token %s" % api_token,
        "Accept": "application/vnd.github.vixen-preview+json",
    },
)

client = Client(transport=_transport, fetch_schema_from_transport=True)
template_query = Template(query_data)


def query(**kwargs):
    query = gql(template_query.substitute(**kwargs))
    return Dict(client.execute(query))
