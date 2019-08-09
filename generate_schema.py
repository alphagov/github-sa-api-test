import os
from classes.github.github_api_client_v4 import GithubApiClientV4


client = GithubApiClientV4()
schema = client.get()
f = open("github_schema.json", "w")
f.write(schema)
f.close()
os.system("sgqlc-codegen github_schema.json github_schema.py")