.PHONY: install lint test intake records index site clean

install:
	uv sync --extra dev

lint:
	uv run ruff check src tests

test:
	uv run pytest

intake:
	uv run python -m atlas.intake.drive_sync

records:
	uv run python -m atlas.intake.extract

index:
	uv run python -m atlas.build.index

site:
	cd atlas && quarto render

clean:
	rm -rf .pytest_cache **/__pycache__
