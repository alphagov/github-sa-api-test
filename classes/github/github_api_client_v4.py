import requests
import json
from addict import Dict
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from .github_api_client import GithubApiClient
from sgqlc.operation import Operation
from github_schema import github_schema as schema


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

    def get(self):
        headers = self.get_headers()
        url = self.root_url

        response = requests.get(url, headers=headers)
        return response.text

    def get_full_repository_list(self, org):
        # query {
        #   organization(login: "alphagov") {
        #     repositories(first: 100) {
        #       nodes {
        #         name
        #         isArchived
        #         isDisabled
        #         isPrivate
        #         licenseInfo {
        #           name
        #         }
        #       }
        #       pageInfo {
        #         hasNextPage
        #         endCursor
        #       }
        #     }
        #   }
        # }
        cursor = None
        last = False
        repository_list = []
        while not last:
            op = Operation(schema.Query)  # note 'schema.'

            if cursor:
                repositories = op.organization(login=org).repositories(first=100, after=cursor)
            else:
                repositories = op.organization(login=org).repositories(first=100)

            repositories.nodes.name()
            repositories.nodes.is_archived()
            repositories.nodes.is_disabled()
            repositories.nodes.is_private()
            repositories.nodes.license_info.__fields__('name')
            repositories.page_info.__fields__('has_next_page')
            repositories.page_info.__fields__(end_cursor=True)
            query = op.__to_graphql__()
            print(query)
            page_results = self.post(query)
            print(type(page_results))
            # print(json.dumps(page_results))
            page = page_results.organization.repositories.nodes
            repository_list.extend(page)
            last = not page_results.organization.repositories.pageInfo.hasNextPage
            cursor = page_results.organization.repositories.pageInfo.endCursor
            print(f"Cursor: {cursor}")

        return repository_list

    def get_active_vulnerable(self, org):
        # query {
        #   organization(login: "alphagov") {
        #     repositories(first: 100) {
        #       nodes {
        #         name
        #         vulnerabilityAlerts(first:100) {
        #           edges {
        #               node {
        #                   id
        #                   packageName
        #                   vulnerableManifestPath
        #                   vulnerableRequirements
        #                   dismissReason
        #                   dismissedAt
        #                   securityAdvisory {
        #                       id
        #                       summary
        #                       vulnerabilities(first:10) {
        #                       edges {
        #                           node {
        #                           package {
        #                               name
        #                           }
        #                           advisory {
        #                               description
        #                           }
        #                           severity
        #                           firstPatchedVersion{
        #                               identifier
        #                           }
        #                        }
        #                   }
        #                   pageInfo {
        #                   hasNextPage
        #                   endCursor
        #                   }
        #                  }
        #                 }
        # }
        cursor = None
        last = False
        repository_list = []
        while not last:
            op = Operation(schema.Query)  # note 'schema.'

            if cursor:
                repositories = op.organization(login=org).repositories(first=100, after=cursor)
            else:
                repositories = op.organization(login=org).repositories(first=100)

            repositories.nodes.name()
            repositories.nodes.vulnerability_alerts.edges.node.__fields__('id')
            print(op)
            last = True
            exit


            '''
        results = v4client.post(query_data) # change to populate dynamically
        vulnerable_nodes = [
             node
             for node
             in results.organization.repositories.nodes
             if node.vulnerabilityAlerts.edges]

        print(json.dumps(vulnerable_nodes, indent=4))'''
