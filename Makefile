init:
	pip install -r requirements.txt
	pre-commit install

format:
	black src
	isort src

lint:
	flake8 src

test:
	python3 -m pytest

run:
	python3 src/run.py