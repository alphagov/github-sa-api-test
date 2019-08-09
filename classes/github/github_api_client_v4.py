from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .github_api_client import GithubApiClient


class GithubApiClientV4(GithubApiClient):
    root_url = "https://api.github.com/graphql"
    accept_header = "application/vnd.github.vixen-preview+json"
    token = ""
    def __init__(self):
        # super(GithubApiClientV4, self).__init__()
        self.load_token()

        self._transport = RequestsHTTPTransport(
            url=self.root_url,
            use_json=True,
            headers=self.get_headers()
        )

        self.client = Client(
            transport=self._transport,
            fetch_schema_from_transport=True,
        )

    def post(self, body):
        query = gql(body)
        from pprint import pprint
        results = Dict(self.client.execute(query))
        return results
