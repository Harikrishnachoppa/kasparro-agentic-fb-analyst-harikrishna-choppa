# Makefile for Kasparro Agentic FB Analyst
# Version: 1.0.0
# Production-ready multi-agent agentic system for Facebook Ads analysis

.PHONY: help install run test clean lint format validate

# Default target
help:
	@echo "Kasparro Agentic FB Analyst v1.0 - Makefile Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the analysis with default query"
	@echo "  make test       - Run all tests"
	@echo "  make validate   - Validate code and tests"
	@echo "  make clean      - Clean generated files"
	@echo "  make lint       - Run linter"
	@echo "  make format     - Format code"
	@echo ""

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

# Run with default query
run:
	@echo "Running analysis..."
	python run.py "Analyze ROAS drop in last 30 days"

# Run with custom query
run-custom:
	@echo "Enter your query:"
	@read query; python run.py "$$query"

# Run tests
test:
	@echo "Running tests..."
	python -m pytest tests/ -v
	@echo "✓ Tests complete"

# Validate code quality and run tests
validate:
	@echo "Validating project..."
	@echo "1. Checking structure..."
	@test -f README.md && echo "  ✓ README.md" || (echo "  ✗ README.md missing"; exit 1)
	@test -f requirements.txt && echo "  ✓ requirements.txt" || (echo "  ✗ requirements.txt missing"; exit 1)
	@test -d src/agents && echo "  ✓ src/agents/" || (echo "  ✗ src/agents/ missing"; exit 1)
	@test -d tests && echo "  ✓ tests/" || (echo "  ✗ tests/ missing"; exit 1)
	@echo "2. Running tests..."
	python -m pytest tests/ -v --tb=short
	@echo "✓ Validation complete - project is production-ready"

# Run evaluator tests
test-evaluator:
	@echo "Running evaluator tests..."
	python -m pytest tests/test_evaluator.py -v

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf reports/*.json reports/*.md logs/*.json
	rm -rf __pycache__ src/__pycache__ src/*/__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc src/*.pyc src/*/*.pyc
	@echo "✓ Cleanup complete"

# Lint code
lint:
	@echo "Running linter..."
	pylint src/
	@echo "✓ Linting complete"

# Format code
format:
	@echo "Formatting code..."
	black src/
	@echo "✓ Formatting complete"

# Create directories
setup-dirs:
	@echo "Creating directories..."
	mkdir -p data reports logs tests
	@echo "✓ Directories created"

# Run example queries
examples:
	@echo "Running example queries..."
	@echo "\n1. Analyzing ROAS drop..."
	python run.py "Analyze ROAS drop in last 30 days"
	@echo "\n2. Analyzing CTR decline..."
	python run.py "Why is my CTR declining?"
	@echo "\n3. General optimization..."
	python run.py "How can I improve my Facebook ads?"
	@echo "✓ Examples complete"

# Check setup
check:
	@echo "Checking setup..."
	@echo "Python version:"
	python --version
	@echo "\nInstalled packages:"
	pip list | grep -E "pandas|numpy|pyyaml"
	@echo "\nProject structure:"
	tree -L 2 || ls -R
	@echo "✓ Setup check complete"
