# Artisanc CLI - Test Suite

Comprehensive test suite for the artisanc command-line tool for managing Artisan Roaster Scope log files.

## Test Structure

```
.
├── artisanc_cli.py          # Main CLI tool
├── test_artisanc.py         # Unit tests (pytest)
├── test_integration.sh      # Integration tests
├── run_tests.sh             # Test runner script
├── Makefile                 # Test automation
└── TEST_README.md           # This file
```

## Quick Start

### 1. Install Dependencies

```bash
make install-deps
```

Or manually:
```bash
pip install pytest pytest-cov pytest-html
```

### 2. Run Tests

**Quick test run:**
```bash
make test
```

**All unit tests:**
```bash
make test-unit
```

**Integration tests:**
```bash
make test-integration
```

**Everything:**
```bash
make test-all
```

## Test Types

### Unit Tests (`test_artisanc.py`)

Pytest-based unit tests covering:

- **AlogParser class**
  - File loading (valid, invalid, nonexistent)
  - Metrics extraction with/without computed data
  - Event extraction (CHARGE, TP, DE, FCs, FCe, SCs, DROP)
  - Notes management (read, update, append, overwrite)
  - Time and temperature formatting
  - File saving

- **OutputFormatter class**
  - Text formatting
  - JSON formatting
  - Markdown formatting
  - Notes formatting

- **CLI functionality**
  - Command-line argument parsing
  - Output format switching
  - Update operations via stdin
  - Error handling

**Run specific test:**
```bash
./run_tests.sh -t test_load_valid_file
```

**Run with coverage:**
```bash
make coverage
```

**Generate HTML coverage report:**
```bash
make coverage-html
```

### Integration Tests (`test_integration.sh`)

Shell-based integration tests that test the actual CLI:

1. Default metrics display
2. Explicit metrics flag
3. Roasting notes display
4. Cupping notes display
5. JSON output format
6. Markdown output format
7. Text output format
8. Append mode updates
9. Overwrite mode updates
10. Nonexistent file handling
11. Invalid file format handling
12. Event extraction verification
13. Phase metrics display
14. Weight loss calculation
15. Multiple format switches
16. Special characters in notes
17. Empty notes handling
18. Help message display

**Run integration tests:**
```bash
./test_integration.sh
```

Or:
```bash
make test-integration
```

## Using the Test Runner

The `run_tests.sh` script provides flexible test execution:

```bash
# Verbose output
./run_tests.sh -v

# With coverage
./run_tests.sh -c

# Generate HTML report
./run_tests.sh -h

# Run tests matching pattern
./run_tests.sh -t "test_format"

# Quick run (default)
./run_tests.sh --quick

# Full run with coverage
./run_tests.sh --full

# Show help
./run_tests.sh --help
```

## Using Make Targets

```bash
make help              # Show all available targets
make test              # Quick unit tests
make test-unit         # All unit tests
make test-integration  # Integration tests only
make test-all          # Everything
make coverage          # Tests with coverage report
make coverage-html     # Coverage with HTML output
make clean             # Remove test artifacts
```

## Test Coverage Goals

Current coverage targets:
- Overall: >90%
- Core parsing logic: >95%
- CLI interface: >85%
- Output formatting: >90%

## Writing New Tests

### Adding Unit Tests

Add to `test_artisanc.py`:

```python
def test_new_feature(self, temp_alog_file):
    """Test description"""
    parser = AlogParser(temp_alog_file)
    result = parser.new_method()
    assert result == expected_value
```

### Adding Integration Tests

Add to `test_integration.sh`:

```bash
run_test "Test description"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --new-flag 2>&1)
if echo "$OUTPUT" | grep -q "expected"; then
    pass "Test passed"
else
    fail "Test failed" "$OUTPUT"
fi
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
# In your CI script
make install-deps
make test-all
```

Example GitHub Actions workflow:

```yaml
- name: Run tests
  run: |
    make install-deps
    make coverage
```

## Debugging Failed Tests

**Verbose pytest output:**
```bash
pytest test_artisanc.py -vv -s
```

**Show full tracebacks:**
```bash
pytest test_artisanc.py --tb=long
```

**Run last failed tests:**
```bash
pytest test_artisanc.py --lf
```

**Drop into debugger on failure:**
```bash
pytest test_artisanc.py --pdb
```

## Test Data

Test files use sample alog data in Python dict format:

```python
SAMPLE_ALOG_DATA = {
    'roastUUID': 'test-uuid',
    'roastdate': 'Sat Sep 28 2025',
    'beans': 'Test Beans',
    'weight': [150.0, 128.0, 'g'],
    'timeindex': [16, 188, 343, 0, 0, 0, 446, 0],
    # ... more data
}
```

## Troubleshooting

**Tests not finding artisanc_cli.py:**
- Ensure script is in same directory as tests
- Check file permissions

**Import errors:**
- Install pytest: `pip install pytest`
- Check Python path

**Integration tests fail:**
- Make scripts executable: `chmod +x *.sh`
- Check shebang lines are correct

**Coverage not generating:**
- Install pytest-cov: `pip install pytest-cov`

## Contributing

When adding new features to artisanc:

1. Write unit tests first (TDD approach)
2. Add integration test for CLI behavior
3. Ensure coverage stays above 90%
4. Run `make test-all` before committing
5. Update this README if needed

## License

Same as parent project.
