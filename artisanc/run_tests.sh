#!/bin/bash
#
# Test runner script for artisanc CLI tool
# Runs pytest with various options and configurations
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Artisanc CLI Test Suite${NC}"
echo -e "${BLUE}================================${NC}"
echo

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest is not installed${NC}"
    echo "Install it with: pip install pytest pytest-cov"
    exit 1
fi

# Check if the main script exists
if [ ! -f "$SCRIPT_DIR/artisanc_cli.py" ]; then
    echo -e "${RED}Error: artisanc_cli.py not found in $SCRIPT_DIR${NC}"
    exit 1
fi

# Parse command line arguments
VERBOSE=""
COVERAGE=""
MARKERS=""
SPECIFIC_TEST=""
HTML_REPORT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -c|--coverage)
            COVERAGE="--cov=artisanc_cli --cov-report=term-missing"
            shift
            ;;
        -h|--html)
            HTML_REPORT="--html=test_report.html --self-contained-html"
            shift
            ;;
        -m|--marker)
            MARKERS="-m $2"
            shift 2
            ;;
        -t|--test)
            SPECIFIC_TEST="-k $2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo
            echo "Options:"
            echo "  -v, --verbose       Verbose output"
            echo "  -c, --coverage      Generate coverage report"
            echo "  -h, --html          Generate HTML test report"
            echo "  -m, --marker MARK   Run tests with specific marker"
            echo "  -t, --test PATTERN  Run tests matching pattern"
            echo "  --quick             Run quick tests only"
            echo "  --full              Run all tests with coverage"
            echo "  --help              Show this help message"
            exit 0
            ;;
        --quick)
            echo -e "${YELLOW}Running quick test suite...${NC}"
            pytest "$SCRIPT_DIR/test_artisanc.py" -v --tb=short
            exit $?
            ;;
        --full)
            echo -e "${YELLOW}Running full test suite with coverage...${NC}"
            pytest "$SCRIPT_DIR/test_artisanc.py" -v --cov=artisanc_cli --cov-report=term-missing --cov-report=html
            exit $?
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Default test run if no specific options
if [ -z "$VERBOSE" ] && [ -z "$COVERAGE" ] && [ -z "$MARKERS" ] && [ -z "$SPECIFIC_TEST" ] && [ -z "$HTML_REPORT" ]; then
    VERBOSE="-v"
fi

# Build pytest command
PYTEST_CMD="pytest $SCRIPT_DIR/test_artisanc.py $VERBOSE $COVERAGE $MARKERS $SPECIFIC_TEST $HTML_REPORT"

echo -e "${BLUE}Running tests...${NC}"
echo "Command: $PYTEST_CMD"
echo

# Run the tests
if $PYTEST_CMD; then
    echo
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}All tests passed! ✓${NC}"
    echo -e "${GREEN}================================${NC}"
    
    # Show coverage report location if generated
    if [ -n "$COVERAGE" ]; then
        if [ -d "htmlcov" ]; then
            echo
            echo -e "${BLUE}Coverage report generated: htmlcov/index.html${NC}"
        fi
    fi
    
    # Show HTML report location if generated
    if [ -n "$HTML_REPORT" ]; then
        if [ -f "test_report.html" ]; then
            echo -e "${BLUE}Test report generated: test_report.html${NC}"
        fi
    fi
    
    exit 0
else
    echo
    echo -e "${RED}================================${NC}"
    echo -e "${RED}Some tests failed! ✗${NC}"
    echo -e "${RED}================================${NC}"
    exit 1
fi
