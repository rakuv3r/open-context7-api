.DEFAULT_GOAL := help

.PHONY: help
help: ## Show available commands
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install dependencies and setup
	uv sync --dev
	uv run pre-commit install
	chmod +x scripts/start.sh
	@echo ""
	@echo "================================"
	@echo "Setup complete!"
	@echo "================================"
	@echo ""
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env.dev (or .env.beta, .env.prod)"
	@echo "2. Configure your API keys and settings"
	@echo "3. Run 'make dev', 'make beta', or 'make prod' to start server"
	@echo ""

.PHONY: lint
lint: ## Run code formatting, linting and type checks
	uv run pre-commit run --all-files

.PHONY: dev
dev: ## Start dev server
	ENVFLAG=dev ./scripts/start.sh

.PHONY: beta
beta: ## Start beta server
	ENVFLAG=beta ./scripts/start.sh

.PHONY: prod
prod: ## Start prod server
	ENVFLAG=prod ./scripts/start.sh
