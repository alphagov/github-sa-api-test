import os


class GithubApiClient:
    accept_header = "application/json"
    token = ""
    def __init__(self):
        self.token = self.load_token()

    def load_token(self):
        # print(os.getcwd())
        with open('token') as token_file:
            self.token = token_file.read().replace("\n", "")
            # print(self.token)

    def get_headers(self):
        headers = {
            'Authorization': 'token %s' % self.token,
            'Accept': self.accept_header
        }
        return headers
