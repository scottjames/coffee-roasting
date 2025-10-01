.PHONY: help test test-unit test-integration test-all coverage clean install-deps

# Default target
help:
	@echo "Artisanc CLI - Test Automation"
	@echo "================================"
	@echo ""
	@echo "Available targets:"
	@echo "  make test              - Run quick unit tests"
	@echo "  make test-unit         - Run all unit tests with verbose output"
	@echo "  make test-integration  - Run integration tests"
	@echo "  make test-all          - Run all tests (unit + integration)"
	@echo "  make coverage          - Run tests with coverage report"
	@echo "  make coverage-html     - Generate HTML coverage report"
	@echo "  make install-deps      - Install test dependencies"
	@echo "  make clean             - Clean test artifacts"
	@echo ""

# Quick unit tests
test:
	@echo "Running quick unit tests..."
	@chmod +x run_tests.sh
	@./run_tests.sh --quick

# Full unit tests with verbose output
test-unit:
	@echo "Running all unit tests..."
	@chmod +x run_tests.sh
	@./run_tests.sh -v

# Integration tests
test-integration:
	@echo "Running integration tests..."
	@chmod +x test_integration.sh
	@chmod +x artisanc_cli.py
	@./test_integration.sh

# All tests
test-all: test-unit test-integration
	@echo ""
	@echo "================================"
	@echo "All test suites completed!"
	@echo "================================"

# Coverage report (terminal)
coverage:
	@echo "Running tests with coverage..."
	@chmod +x run_tests.sh
	@./run_tests.sh --full

# Coverage report (HTML)
coverage-html: coverage
	@echo ""
	@echo "Opening coverage report..."
	@if [ -f htmlcov/index.html ]; then \
		python3 -m webbrowser htmlcov/index.html 2>/dev/null || \
		xdg-open htmlcov/index.html 2>/dev/null || \
		open htmlcov/index.html 2>/dev/null || \
		echo "Coverage report generated at: htmlcov/index.html"; \
	fi

# Install test dependencies
install-deps:
	@echo "Installing test dependencies..."
	@pip install pytest pytest-cov pytest-html

# Clean test artifacts
clean:
	@echo "Cleaning test artifacts..."
	@rm -rf __pycache__ .pytest_cache htmlcov .coverage
	@rm -f test_report.html
	@rm -rf test_*.pyc
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

# Run specific test by name
test-specific:
	@if [ -z "$(TEST)" ]; then \
		echo "Error: Please specify TEST=<test_name>"; \
		echo "Example: make test-specific TEST=test_load_valid_file"; \
		exit 1; \
	fi
	@chmod +x run_tests.sh
	@./run_tests.sh -t "$(TEST)"

# Watch mode (requires pytest-watch)
watch:
	@if ! command -v ptw &> /dev/null; then \
		echo "pytest-watch not installed. Install with: pip install pytest-watch"; \
		exit 1; \
	fi
	@ptw -- test_artisanc.py -v
