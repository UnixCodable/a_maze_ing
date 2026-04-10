.PHONY: install run debug clean lint lint-strict build

# Install project dependencies
install:
	python3 -m  pip install --upgrade pip
	python3 -m pip install -r requirements.txt
	python3 -m pip install -e .

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
	flake8 . --exclude=venv,__pycache__
	mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Lint strict (optional)
lint-strict:
	flake8 . --exclude=venv,__pycache__
	mypy . --strict

# Build the pip package
build:
	python3 -m pip install build
	python3 -m build
