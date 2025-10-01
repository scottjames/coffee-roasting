#!/bin/bash
#
# Integration tests for artisanc CLI
# Tests the actual command-line interface
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARTISANC="$SCRIPT_DIR/artisanc_cli.py"
TEST_DIR=$(mktemp -d)
TEST_FILE="$TEST_DIR/test_roast.alog"

# Test counter
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Cleanup function
cleanup() {
    rm -rf "$TEST_DIR"
}
trap cleanup EXIT

# Helper functions
pass() {
    echo -e "${GREEN}✓ PASS${NC}: $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}✗ FAIL${NC}: $1"
    echo "  $2"
    ((TESTS_FAILED++))
}

run_test() {
    ((TESTS_RUN++))
    echo -e "${BLUE}Test $TESTS_RUN:${NC} $1"
}

# Create test data file
create_test_file() {
    cat > "$TEST_FILE" << 'EOF'
{'roastUUID': 'test-integration-uuid', 'roastdate': 'Sat Sep 28 2025', 'beans': 'Integration Test Beans\n150g', 'weight': [150.0, 128.0, 'g'], 'ground_color': 55, 'timeindex': [16, 188, 343, 0, 0, 0, 446, 0], 'timex': [0.0, 10.0, 20.0, 30.0, 188.0, 343.0, 446.0], 'temp1': [90.0, 91.0, 92.0, 93.0, 118.0, 122.0, 126.0], 'temp2': [130.0, 125.0, 135.0, 145.0, 165.0, 173.0, 181.0], 'roastingnotes': 'Test roasting notes', 'cuppingnotes': 'Test cupping notes', 'computed': {'CHARGE_ET': 90.0, 'CHARGE_BT': 130.0, 'TP_idx': 1, 'TP_time': 10.0, 'TP_ET': 91.0, 'TP_BT': 125.0, 'DRY_time': 16.0, 'DRY_ET': 92.0, 'DRY_BT': 135.0, 'FCs_time': 188.0, 'FCs_ET': 118.0, 'FCs_BT': 165.0, 'fcs_ror': 6.9, 'DROP_time': 446.0, 'DROP_ET': 126.0, 'DROP_BT': 181.0, 'totaltime': 446.0, 'dryphasetime': 172.0, 'midphasetime': 155.0, 'finishphasetime': 119.0, 'dry_phase_ror': 8.9, 'mid_phase_ror': 6.5, 'finish_phase_ror': 5.8, 'total_ror': 7.1, 'weight_loss': 15}}
EOF
}

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Artisanc Integration Tests${NC}"
echo -e "${BLUE}================================${NC}"
echo

# Check if script exists
if [ ! -f "$ARTISANC" ]; then
    echo -e "${RED}Error: $ARTISANC not found${NC}"
    exit 1
fi

# Make script executable
chmod +x "$ARTISANC"

# Create test file
create_test_file

# Test 1: Display metrics (default)
run_test "Display metrics (default behavior)"
OUTPUT=$("$ARTISANC" "$TEST_FILE" 2>&1)
if echo "$OUTPUT" | grep -q "ROAST PROFILE METRICS"; then
    pass "Metrics displayed"
else
    fail "Metrics not displayed" "$OUTPUT"
fi

# Test 2: Display metrics explicitly
run_test "Display metrics with --metrics flag"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "test-integration-uuid" && echo "$OUTPUT" | grep -q "CHARGE"; then
    pass "Metrics with events displayed"
else
    fail "Metrics incomplete" "$OUTPUT"
fi

# Test 3: Display roasting notes
run_test "Display roasting notes"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --roast 2>&1)
if echo "$OUTPUT" | grep -q "Test roasting notes"; then
    pass "Roasting notes displayed"
else
    fail "Roasting notes not displayed" "$OUTPUT"
fi

# Test 4: Display cupping notes
run_test "Display cupping notes"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --cup 2>&1)
if echo "$OUTPUT" | grep -q "Test cupping notes"; then
    pass "Cupping notes displayed"
else
    fail "Cupping notes not displayed" "$OUTPUT"
fi

# Test 5: JSON output format
run_test "JSON output format"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics -o json 2>&1)
if echo "$OUTPUT" | python3 -m json.tool > /dev/null 2>&1; then
    pass "Valid JSON output"
else
    fail "Invalid JSON output" "$OUTPUT"
fi

# Test 6: Markdown output format
run_test "Markdown output format"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics -o md 2>&1)
if echo "$OUTPUT" | grep -q "# Roast Profile Metrics"; then
    pass "Markdown output formatted correctly"
else
    fail "Markdown output incorrect" "$OUTPUT"
fi

# Test 7: Text output format (explicit)
run_test "Text output format (explicit)"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics -o text 2>&1)
if echo "$OUTPUT" | grep -q "ROAST PROFILE METRICS"; then
    pass "Text output formatted correctly"
else
    fail "Text output incorrect" "$OUTPUT"
fi

# Test 8: Update roasting notes (append mode)
run_test "Update roasting notes (append mode)"
echo "Additional roast notes" | "$ARTISANC" "$TEST_FILE" --roast --update > /dev/null 2>&1
OUTPUT=$("$ARTISANC" "$TEST_FILE" --roast 2>&1)
if echo "$OUTPUT" | grep -q "Test roasting notes" && echo "$OUTPUT" | grep -q "Additional roast notes"; then
    pass "Roasting notes appended"
else
    fail "Roasting notes not appended" "$OUTPUT"
fi

# Test 9: Update cupping notes (overwrite mode)
run_test "Update cupping notes (overwrite mode)"
echo "New cupping notes" | "$ARTISANC" "$TEST_FILE" --cup --update --overwrite > /dev/null 2>&1
OUTPUT=$("$ARTISANC" "$TEST_FILE" --cup 2>&1)
if echo "$OUTPUT" | grep -q "New cupping notes" && ! echo "$OUTPUT" | grep -q "Test cupping notes"; then
    pass "Cupping notes overwritten"
else
    fail "Cupping notes not overwritten correctly" "$OUTPUT"
fi

# Test 10: Nonexistent file error
run_test "Error handling for nonexistent file"
if "$ARTISANC" "/nonexistent/file.alog" --metrics > /dev/null 2>&1; then
    fail "Should have failed for nonexistent file"
else
    pass "Correctly handled nonexistent file"
fi

# Test 11: Invalid format file
run_test "Error handling for invalid file format"
INVALID_FILE="$TEST_DIR/invalid.alog"
echo "invalid { data format" > "$INVALID_FILE"
if "$ARTISANC" "$INVALID_FILE" --metrics > /dev/null 2>&1; then
    fail "Should have failed for invalid file format"
else
    pass "Correctly handled invalid file format"
fi

# Test 12: Event extraction (CHARGE)
run_test "Event extraction - CHARGE event"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "CHARGE.*0:00.*90.0.*130.0"; then
    pass "CHARGE event extracted correctly"
else
    fail "CHARGE event not extracted" "$OUTPUT"
fi

# Test 13: Event extraction (FCs)
run_test "Event extraction - FCs event"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "FCs.*3:08.*118.0.*165.0"; then
    pass "FCs event extracted correctly"
else
    fail "FCs event not extracted" "$OUTPUT"
fi

# Test 14: Event extraction (DROP)
run_test "Event extraction - DROP event"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "DROP.*7:26.*126.0.*181.0"; then
    pass "DROP event extracted correctly"
else
    fail "DROP event not extracted" "$OUTPUT"
fi

# Test 15: Phase metrics display
run_test "Phase metrics display"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "PHASE METRICS" && echo "$OUTPUT" | grep -q "Total Time"; then
    pass "Phase metrics displayed"
else
    fail "Phase metrics not displayed" "$OUTPUT"
fi

# Test 16: Weight loss calculation
run_test "Weight loss calculation"
OUTPUT=$("$ARTISANC" "$TEST_FILE" --metrics 2>&1)
if echo "$OUTPUT" | grep -q "Weight Loss.*15%"; then
    pass "Weight loss calculated correctly"
else
    fail "Weight loss calculation incorrect" "$OUTPUT"
fi

# Test 17: Multiple output formats in sequence
run_test "Multiple output format switches"
"$ARTISANC" "$TEST_FILE" --metrics -o text > "$TEST_DIR/out1.txt" 2>&1
"$ARTISANC" "$TEST_FILE" --metrics -o json > "$TEST_DIR/out2.json" 2>&1
"$ARTISANC" "$TEST_FILE" --metrics -o md > "$TEST_DIR/out3.md" 2>&1

if [ -s "$TEST_DIR/out1.txt" ] && [ -s "$TEST_DIR/out2.json" ] && [ -s "$TEST_DIR/out3.md" ]; then
    pass "Multiple format outputs work correctly"
else
    fail "Multiple format outputs failed"
fi

# Test 18: Roast notes with special characters
run_test "Update notes with special characters"
echo "Notes with 'quotes' and \"double quotes\" and \$pecial chars" | "$ARTISANC" "$TEST_FILE" --roast --update --overwrite > /dev/null 2>&1
OUTPUT=$("$ARTISANC" "$TEST_FILE" --roast 2>&1)
if echo "$OUTPUT" | grep -q "quotes"; then
    pass "Special characters handled correctly"
else
    fail "Special characters not handled" "$OUTPUT"
fi

# Test 19: Empty notes update
run_test "Update with empty notes"
echo "" | "$ARTISANC" "$TEST_FILE" --cup --update --overwrite > /dev/null 2>&1
OUTPUT=$("$ARTISANC" "$TEST_FILE" --cup 2>&1)
if [ -z "$(echo "$OUTPUT" | grep -v "Cupping Notes" | grep -v "=" | tr -d '[:space:]')" ]; then
    pass "Empty notes handled correctly"
else
    fail "Empty notes not handled correctly" "$OUTPUT"
fi

# Test 20: Help message
run_test "Help message display"
OUTPUT=$("$ARTISANC" --help 2>&1)
if echo "$OUTPUT" | grep -q "usage:" && echo "$OUTPUT" | grep -q "metrics"; then
    pass "Help message displayed"
else
    fail "Help message not displayed correctly" "$OUTPUT"
fi

# Summary
echo
echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}================================${NC}"
echo "Tests run:    $TESTS_RUN"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo
    echo -e "${GREEN}All integration tests passed!${NC}"
    exit 0
else
    echo
    echo -e "${RED}Some integration tests failed!${NC}"
    exit 1
fi