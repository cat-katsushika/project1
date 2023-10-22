.PHONY: dev-env
dev-env:
	cp .env.dev .env

.PHONY: dev-build
dev-build:
	docker compose -f docker-compose-dev.yml build

.PHONY: dev-build--no-cache
dev-build--no-cache:
	docker compose -f docker-compose-dev.yml build --no-cache

.PHONY: dev-up-d
dev-up-d:
	docker compose -f docker-compose-dev.yml up -d

.PHONY: dev
dev:
	@make dev-build
	@make dev-up-d

.PHONY: down
down:
	docker compose -f docker-compose-dev.yml down

.PHONY: logs
logs:
	docker compose -f docker-compose-dev.yml logs -f

.PHONY: test
test:
	docker compose -f docker-compose-dev.yml exec django python manage.py test

.PHONY: black
black:
	docker compose -f docker-compose-dev.yml exec django black .

.PHONY: isort
isort:
	docker compose -f docker-compose-dev.yml exec django isort .

.PHONY: flake8
flake8:
	docker compose -f docker-compose-dev.yml exec django flake8 .

.PHONY: lint
lint:
	@make black
	@make isort
	@make flake8

.PHONY: rm-db
rm-db:
	sudo rm -rf db/

.PHONY: dev-full
dev-full:
	@make rm-db
	@make dev-build--no-cache
	@make dev-up-d


.PHONY: fixtures
fixtures:
	docker compose -f docker-compose-dev.yml exec django python manage.py loaddata --format yaml fixtures.yaml

.PHONY: fixtures--dump
fixtures--dump:
	@make fixtures
	docker compose -f docker-compose-dev.yml exec django python manage.py dumpdata --format yaml --output=fixtures.yaml
