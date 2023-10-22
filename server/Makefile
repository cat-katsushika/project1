.PHONY: dev-build
dev-build:
	docker compose -f docker-compose-dev.yml build

.PHONY: dev-up-d
dev-up-d:
	docker compose -f docker-compose-dev.yml up -d

.PHONY: dev
dev:
	@make dev-build
	@make dev-up-d

.PHONY: dev-down
dev-down:
	docker compose -f docker-compose-dev.yml down

.PHONY: dev-logs
dev-logs:
	docker compose -f docker-compose-dev.yml logs -f
