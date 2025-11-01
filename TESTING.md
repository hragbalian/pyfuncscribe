# PyFuncScribe Testing Guide

## Quick Start

### Install Test Dependencies

```bash
pip install pytest
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suite

```bash
# Reporter tests
pytest tests/test_reporter.py -v

# CLI tests
pytest tests/test_cli.py -v

# Extractor tests
pytest tests/test_extractor.py -v
```

## Test Suite Overview

The test suite covers all major components of PyFuncScribe with 80+ tests across 4 files:

### Test Files

1. **`tests/conftest.py`**
   - Pytest configuration
   - Shared fixtures for all tests
   - 3 fixtures: `temp_dir`, `temp_file`, `sample_functions`

2. **`tests/test_reporter.py`** (23 tests)
   - MarkdownReporter functionality
   - Report generation
   - Diff detection (the critical bug fix)
   - Function formatting
   - Directory grouping

3. **`tests/test_cli.py`** (20 tests)
   - CLI argument parsing
   - File I/O operations
   - **File preservation** (critical feature) ⭐
   - Change detection workflow
   - Error handling

4. **`tests/test_extractor.py`** (25 tests)
   - Function extraction
   - Python file discovery
   - Metadata extraction
   - Error handling
   - Edge cases (async, decorators, etc.)

## Critical Tests

### File Preservation Tests ⭐

These tests ensure the critical bug fix works correctly:

```bash
pytest tests/test_cli.py::TestFilePreservation -v
```

**What they test:**
- When `--add-description` flag is used and no code changes detected
- Existing file should NOT be modified
- LLM-generated description should be preserved
- No unnecessary API calls should be made

**Key tests:**
- `test_file_preserved_when_no_changes`
- `test_file_overwritten_without_add_description_flag`

### Change Detection Tests

```bash
pytest tests/test_reporter.py::TestDiffDetection -v
pytest tests/test_cli.py::TestChangeDetection -v
```

**What they test:**
- Changes in function count detected
- Changes in function signatures detected
- Identical code detected as no change
- Description sections properly ignored

## Test Coverage

### Reporter Module (`src/pyfuncscribe/reporter.py`)
- ✓ Report generation with various options
- ✓ Diff detection algorithm (`_has_content_changed`)
- ✓ Function formatting and sorting
- ✓ Directory grouping

### Extractor Module (`src/pyfuncscribe/extractor.py`)
- ✓ Python file discovery
- ✓ Function extraction from AST
- ✓ Metadata extraction (signatures, docstrings, decorators)
- ✓ Error handling for malformed files

### CLI Module (`src/pyfuncscribe/cli.py`)
- ✓ Argument parsing
- ✓ File I/O operations
- ✓ Error handling
- ✓ File preservation logic
- ✓ Change detection workflow

## Running Tests with Coverage

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage report
pytest tests/ --cov=src/pyfuncscribe --cov-report=html

# View coverage in browser
open htmlcov/index.html
```

## Test Markers

Tests can be run by marker:

```bash
# Run unit tests only
pytest -m unit

# Run integration tests only
pytest -m integration

# Run CLI tests
pytest -m cli

# Run reporter tests
pytest -m reporter
```

Available markers (defined in `pytest.ini`):
- `unit`: Unit tests for individual components
- `integration`: Integration tests
- `cli`: CLI functionality tests
- `reporter`: Reporter functionality tests
- `extractor`: Extractor functionality tests
- `slow`: Slow running tests

## Test Organization

```
tests/
├── __init__.py                 # Package marker
├── conftest.py                 # Pytest fixtures and config
├── test_reporter.py            # Reporter tests (23 tests)
├── test_cli.py                 # CLI tests (20 tests)
├── test_extractor.py           # Extractor tests (25 tests)
├── README.md                   # Detailed test documentation
└── TEST_INVENTORY.md           # Complete test inventory
```

## Key Features Tested

### 1. Report Generation
- Basic report with functions
- Empty function lists
- Brief vs. full docstrings
- Table of contents generation
- Directory grouping
- Function sorting

### 2. Diff Detection ⭐⭐⭐
- Identical reports
- Different function counts
- Different function details
- Description sections ignored
- Whitespace normalization
- Edge cases

### 3. File Preservation ⭐⭐⭐
- File NOT modified when no changes + `--add-description`
- File modified when `--add-description` NOT used
- File modified when changes detected
- LLM description preservation

### 4. CLI Operations
- Argument parsing (all flags)
- Output to stdout
- Output to file
- Directory creation
- Error handling
- Message output

### 5. Function Extraction
- File discovery
- Function extraction
- Metadata extraction
- Async functions
- Decorators
- Type annotations
- Default values

## Test Statistics

- **Total test files**: 4
- **Total test classes**: 20+
- **Total test functions**: 80+
- **Lines of test code**: 1,500+
- **Execution time**: ~5-7 seconds

## Fixtures

### Provided Fixtures

All fixtures are defined in `conftest.py`:

```python
@pytest.fixture
def temp_dir():
    """Temporary directory that auto-cleans up."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def temp_file(temp_dir):
    """Temporary file path (file not created)."""
    return temp_dir / "test_report.md"

@pytest.fixture
def sample_functions():
    """Sample FunctionInfo objects for testing."""
    return [
        FunctionInfo(...),
        FunctionInfo(...),
    ]
```

### Using Fixtures

```python
def test_something(temp_dir, temp_file, sample_functions):
    # Use fixtures in test
    pass
```

## Common Test Patterns

### Testing Report Generation

```python
def test_report_contains_function(sample_functions):
    reporter = MarkdownReporter()
    report = reporter.generate_report(sample_functions)
    assert "function_name" in report
```

### Testing File Operations

```python
def test_file_operations(temp_file):
    content = "test content"
    temp_file.write_text(content)
    assert temp_file.exists()
    assert temp_file.read_text() == content
```

### Testing CLI

```python
def test_cli_with_args(temp_file):
    from unittest.mock import patch
    with patch('sys.argv', ['pyfuncscribe', '-o', str(temp_file)]):
        main()
    assert temp_file.exists()
```

## Debugging Tests

### Run with detailed output

```bash
pytest tests/ -vv  # Very verbose
pytest tests/ -s   # Show print statements
pytest tests/ -x   # Stop on first failure
```

### Run single test

```bash
pytest tests/test_reporter.py::TestDiffDetection::test_identical_reports_no_change -v
```

### Run tests matching pattern

```bash
pytest -k "file_preservation" -v
```

### Show test collection

```bash
pytest --collect-only tests/
```

## Continuous Integration

### Basic CI setup

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install pytest
      - run: pytest tests/ -v
```

## Troubleshooting

### Import errors

```bash
# Ensure running from project root
cd /path/to/pyfuncscribe

# Add src to path if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Install package in development mode
pip install -e .
```

### pytest not found

```bash
# Install pytest
pip install pytest

# Or run with module syntax
python3 -m pytest tests/ -v
```

### Tests fail with path errors

```bash
# Ensure absolute paths are used
# Or run from project root
cd /Users/hragbalian/git/pyfuncscribe
pytest tests/ -v
```

## Adding New Tests

1. Identify the module being tested
2. Add test to appropriate file:
   - Reporter functionality → `test_reporter.py`
   - CLI functionality → `test_cli.py`
   - Extraction functionality → `test_extractor.py`

3. Use naming convention: `test_<feature>_<scenario>`

4. Example:
```python
def test_new_feature_with_valid_input(sample_functions):
    """Test that new feature handles valid input correctly."""
    reporter = MarkdownReporter()
    result = reporter.generate_report(sample_functions)
    assert "expected" in result
```

5. Run the new test:
```bash
pytest tests/test_file.py::test_new_feature_with_valid_input -v
```

## Test Quality Standards

- ✓ Tests are independent and order-agnostic
- ✓ Descriptive test names
- ✓ Clear docstrings
- ✓ Proper setup/teardown (using fixtures)
- ✓ Both success and failure cases
- ✓ No hardcoded file paths
- ✓ Resource cleanup
- ✓ Clear assertions

## Related Files

- `tests/README.md` - Detailed test documentation
- `tests/TEST_INVENTORY.md` - Complete test inventory
- `pytest.ini` - Pytest configuration
- `src/pyfuncscribe/reporter.py` - Code being tested
- `src/pyfuncscribe/extractor.py` - Code being tested
- `src/pyfuncscribe/cli.py` - Code being tested

## Summary

The PyFuncScribe test suite provides comprehensive coverage of all major functionality including:

1. **Core Features**: Report generation, function extraction, CLI operations
2. **Critical Bug Fix**: File preservation when no changes detected
3. **Change Detection**: Identifying code changes for LLM regeneration
4. **Edge Cases**: Async functions, decorators, type annotations, error handling

Run `pytest tests/ -v` to execute all tests and ensure everything works correctly!
