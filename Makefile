#!/usr/bin/env make

build:
	docker build -t pydns:latest .

run:
	docker compose up pydns mysql

run-bg:
	docker compose up -d pydns mysql

restart:
	docker compose down pydns && docker compose up -d pydns && make logs

stop:
	docker compose down

last?=1000
logs:
	docker compose logs -f pydns mysql --tail ${last}