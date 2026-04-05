.PHONY: install run debug clean lint lint-strict build

# Install project dependencies
install:
	pip install flake8 mypy pydantic
	pip install -e .

# Run the main program
run:
	python3 a_maze_ing.py config.txt

# Debug mode
debug:
	python3 -m pdb a_maze_ing.py config.txt

# Clean temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name *.egg-info -exec rm -rf {} +
	find . -type d -name build -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +

# Lint (mandatory flags from subject)
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Lint strict (optional)
lint-strict:
	flake8 .
	mypy . --strict

# Build the pip package
build:
	pip install build
	python -m build