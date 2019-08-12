.PHONY: run

run: github_schema.py
	docker-compose up

github_schema.py:
	docker-compose run dashboard python download_json_schema.py
	docker-compose run dashboard sgqlc-codegen github_schema.json github_schema.py

shell:
	docker-compose run dashboard sh

rebuild:
	docker-compose build
