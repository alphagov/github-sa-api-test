# Test implementation of GitHub GraphQL and REST API

## Setup

On first run:

0. Create a file called `token` containing a personal access token
string.
0. rename `github_schema.json.bak` to `github_schema.json`

You can use a venv or docker to run this project. If docker, just run `make`.

If in a python 3 virtual env:

```
pip install -r requirements.txt
python generate_schema.py
```

## Run

So far this just runs a bunch of API calls and generates a GQL
query from variables.

```
python dashboard.py
```

Or `make`
