from classes.github.github_api_client_v4 import GithubApiClientV4


schema = GithubApiClientV4().get()
f = open("github_schema.json", "w")
f.write(schema)
f.close()
