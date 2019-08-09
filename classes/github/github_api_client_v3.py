import requests
import json
from .github_api_client import GithubApiClient


class GithubApiClientV3(GithubApiClient):
    root_url = "https://api.github.com"
    accept_header = "application/vnd.github.dorian-preview+json"
    def __init__(self):
        # super(GithubApiClientV4, self).__init__()
        self.load_token()

    def get(self, path):
        headers = self.get_headers()
        url = self.root_url + path

        response = requests.get(url, headers=headers)
        return response

    def post(self, path, body):
        return False
