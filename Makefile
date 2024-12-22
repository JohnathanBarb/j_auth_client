test:
	uv run pytest

tests: test

lint:
	uv run ruff check

force-lint:
	uv run ruff check --fix

format:
	uv run ruff format
