.PHONY: install lint test intake records index generate site clean

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
	uv run python -m atlas.intake.review

index:
	uv run python -m atlas.build.score
	uv run python -m atlas.viz.semaforo

generate:
	uv run python -m atlas.build.fichas
	uv run python -m atlas.build.anexos
	uv run python -m atlas.build.capitulos

site: generate
	uv run --with jupyter --with pyyaml bash -c 'cd atlas && QUARTO_PYTHON=$$(which python) quarto render --to html'

clean:
	rm -rf .pytest_cache **/__pycache__
