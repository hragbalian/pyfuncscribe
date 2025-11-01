# PyFuncScribe Test Suite

This directory contains the comprehensive test suite for PyFuncScribe, including unit tests for all major components and integration tests for the full CLI workflow.

## Test Organization

```
tests/
├── __init__.py              # Test package marker
├── conftest.py              # Pytest configuration and shared fixtures
├── test_reporter.py         # Tests for MarkdownReporter class
├── test_cli.py              # Tests for CLI functionality
├── test_extractor.py        # Tests for FunctionExtractor class
└── README.md                # This file
```

## Test Coverage

### Reporter Tests (`test_reporter.py`)

Tests for the `MarkdownReporter` class covering:

- **Basic Functionality**
  - Report generation with functions
  - Report generation with empty function list
  - Brief vs. full docstring modes
  - Table of contents generation

- **Diff Detection** (`_has_content_changed` method)
  - Identical reports detected correctly
  - Different function counts detected
  - Description sections properly ignored
  - Whitespace normalization
  - Modified content detection

- **Function Formatting**
  - Function signatures included
  - Decorators displayed
  - Async functions marked
  - Arguments listed
  - Return types shown
  - File locations displayed

- **Function Grouping**
  - Functions grouped by directory
  - Functions sorted alphabetically

**Test Classes:**
- `TestMarkdownReporterBasics`
- `TestDiffDetection`
- `TestFunctionFormatting`
- `TestGroupingByDirectory`

### CLI Tests (`test_cli.py`)

Tests for command-line interface functionality:

- **Argument Parsing**
  - Default arguments
  - Custom root directory
  - Output file
  - Brief mode flag
  - Add description flag
  - Include commented flag

- **Main Functionality**
  - Error handling for invalid directories
  - Error handling for file as root
  - Output to stdout
  - Output to file
  - Parent directory creation

- **Report Generation**
  - Report generation through CLI
  - Correct content in generated reports
  - Proper directory structure creation

- **File Preservation** (Critical Feature)
  - File NOT overwritten when no changes detected with `--add-description`
  - File IS overwritten without `--add-description` flag
  - Existing descriptions preserved
  - File size consistency

- **Change Detection**
  - Changes detected when functions added
  - No changes detected for identical code
  - Correct LLM description regeneration

- **CLI Messages**
  - Success message on file update
  - "Up-to-date" message when no changes
  - Informational messages

**Test Classes:**
- `TestParseArgs`
- `TestMainFunctionality`
- `TestReportGeneration`
- `TestFilePreservation`
- `TestChangeDetection`
- `TestCLIMessages`

### Extractor Tests (`test_extractor.py`)

Tests for the `FunctionExtractor` class:

- **Initialization**
  - Default initialization
  - Custom root directory
  - Include commented flag

- **Python File Discovery**
  - Finding Python files
  - Finding files in nested directories
  - Proper file filtering

- **Function Extraction**
  - Extracting functions from single file
  - Extracting functions from multiple files
  - Function info has required fields
  - Docstring extraction
  - Return annotation extraction
  - Argument extraction

- **Commented Functions**
  - Excluded by default
  - Included when flag is set

- **Async Functions**
  - Properly detected
  - Marked in extracted info

- **Function Signatures**
  - Simple function signatures
  - Type annotations
  - Default values

- **Decorators**
  - Single decorator extraction
  - Multiple decorators extraction

- **Relative Paths**
  - Proper relative path generation

- **Error Handling**
  - Invalid Python files skipped
  - Graceful error handling in batch extraction

**Test Classes:**
- `TestFunctionExtractorInitialization`
- `TestPythonFileFinding`
- `TestFunctionExtraction`
- `TestCommentedFunctionHandling`
- `TestAsyncFunctionHandling`
- `TestFunctionSignatureBuilding`
- `TestDecoratorExtraction`
- `TestRelativePathGeneration`
- `TestErrorHandling`

## Running Tests

### With pytest (Recommended)

```bash
# Install pytest
pip install pytest

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_reporter.py

# Run specific test class
pytest tests/test_reporter.py::TestDiffDetection

# Run specific test
pytest tests/test_reporter.py::TestDiffDetection::test_identical_reports_no_change

# Run tests matching pattern
pytest -k "file_preservation"

# Run tests with coverage report
pytest --cov=src/pyfuncscribe
```

### Manual Test Runner

If pytest is not available, run the manual test runner:

```bash
python3 tests/manual_test_runner.py
```

This will execute all major test scenarios and verify core functionality.

## Test Fixtures

### Provided Fixtures (in `conftest.py`)

- **`temp_dir`**: Temporary directory that's automatically cleaned up
- **`temp_file`**: Temporary file path (file not created)
- **`sample_functions`**: List of sample `FunctionInfo` objects for testing

Usage:
```python
def test_something(temp_dir, sample_functions):
    # temp_dir is a Path object
    # sample_functions is a list of FunctionInfo objects
    pass
```

## Key Features Tested

### 1. File Preservation (Critical)
When running with `--add-description` flag and no code changes are detected:
- ✓ Existing file is NOT modified
- ✓ File modification time remains unchanged
- ✓ Precious LLM-generated descriptions are preserved
- ✓ No unnecessary API calls are made

### 2. Change Detection
- ✓ Detects new/removed functions
- ✓ Detects function signature changes
- ✓ Ignores description-only changes
- ✓ Handles whitespace normalization

### 3. Report Generation
- ✓ Generates valid Markdown
- ✓ Includes all function metadata
- ✓ Organizes functions by directory
- ✓ Provides table of contents

### 4. CLI Functionality
- ✓ Correct argument parsing
- ✓ Proper error handling
- ✓ File I/O operations
- ✓ Directory creation

## Configuration Files

### `pytest.ini`

Contains pytest configuration:
- Test discovery patterns
- Output verbosity settings
- Test path specifications
- Custom markers for test categorization

### `conftest.py`

Contains:
- Shared pytest fixtures
- Test data generators
- Setup/teardown logic

## Test Metrics

- **Total Test Cases**: 80+
- **Test Files**: 4
- **Test Classes**: 20+
- **Lines of Test Code**: 1,500+

## Continuous Integration

To integrate with CI/CD:

```bash
# Run tests and generate coverage
pytest --cov=src/pyfuncscribe --cov-report=html

# Run with specific Python versions
pytest --python 3.8 3.9 3.10 3.11 3.12 3.13

# Run with xfail markers for expected failures
pytest -v
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. You're running from the project root: `cd /path/to/pyfuncscribe`
2. The `src` directory is in Python path (handled by pytest automatically)
3. Dependencies are installed: `pip install -e .`

### Module Not Found Errors

```bash
# Ensure the module is installed in development mode
pip install -e .

# Add src to PYTHONPATH if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### pytest Not Found

```bash
# Install pytest
pip install pytest

# Or use Python module syntax
python3 -m pytest
```

## Adding New Tests

1. Create test functions with `test_` prefix in appropriate file
2. Use provided fixtures from `conftest.py`
3. Follow naming convention: `test_<feature>_<scenario>`
4. Add docstring explaining what's being tested
5. Run tests to verify: `pytest -v`

Example:
```python
def test_new_feature_with_valid_input(sample_functions):
    """Test that new feature handles valid input correctly."""
    # Setup
    reporter = MarkdownReporter()
    
    # Execute
    result = reporter.generate_report(sample_functions)
    
    # Assert
    assert "expected content" in result
```

## Test Quality Standards

- All tests should be independent
- Use descriptive test names
- Include docstrings explaining test purpose
- Clean up resources (temp files, etc.)
- Use fixtures for setup/teardown
- Test both success and error cases
- Avoid hardcoding file paths

## Related Documentation

- [Main README](../README.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [CLI Documentation](../docs/CLI.md)
