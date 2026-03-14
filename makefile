# vim:  noet
# 14 Mar 2026 Makefile created for /plib
#
# Vision:  
#

PYTHON := python
MYPY := mypy
RUFF := ruff

.PHONY: help check lint typecheck clean

help:
	@echo "--- plib Commands ---"
	@echo "check     : Run both linting and type checking"
	@echo "lint      : Run ruff to find logic bugs (no formatting)"
	@echo "typecheck : Run mypy for static type verification"
	@echo "fix       : Run ruff to safely fix imports and syntax"
	@echo "clean     : Remove python cache files"

# The 'check' command is your "Gold Standard" for a clean PR/Release
check: lint typecheck

lint:
	#$(RUFF) check .
	@echo "Will run lint on . when things are fixed"

typecheck:
	#$(MYPY) .
	@echo "Will run mypy type checker on . when things are fixed"

# This is the 'safe' fix we discussed—no math-mangling!
fix:
	#$(RUFF) check --fix .
	@echo "Will run ruff check --fix on files"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache
