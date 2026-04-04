# Variables
PYTHON = python3
SCRIPT = a_maze_ing.py
CONFIG = config.txt

install:
	$(PYTHON) -m pip install .

run:
	$(PYTHON) $(SCRIPT) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(SCRIPT) $(CONFIG)

clean:
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf .mypy_cache
	rm -rf build/ dist/ *.egg-info

# Mandatory lint flags 
lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		 --disallow-untyped-defs --check-untyped-defs .

# Optional strict checking [cite: 95]
lint-strict:
	flake8 .
	mypy --strict .

# Build the reusable package for evaluation 
package:
	$(PYTHON) -m build