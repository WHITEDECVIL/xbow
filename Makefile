"""
XBOW Makefile - Build and Development Commands
"""

.PHONY: help install install-dev test lint format run clean docs

help:
	@echo "XBOW - AI Penetration Testing Framework"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install XBOW"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make run          - Run XBOW CLI"
	@echo "  make docs         - Generate documentation"
	@echo "  make clean        - Clean build artifacts"

install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black pylint flake8 mypy

test:
	pytest tests/ -v --cov=src

lint:
	pylint src/
	flake8 src/
	mypy src/

format:
	black src/ tests/

run:
	python -m src.cli

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .coverage

docs:
	cd docs && make html

.DEFAULT_GOAL := help
