# PyFuncScribe

A simple, efficient Python CLI tool that generates comprehensive markdown reports of Python functions found in a codebase.

## Features

- Recursively traverses directories to find all Python files
- Extracts detailed function information including:
  - Function name and signature
  - Complete or brief docstrings
  - File location and line numbers
  - Function arguments with type annotations
  - Return type hints
  - Decorators
  - Async function detection
- Generates well-organized markdown reports grouped by directory
- Efficient and minimal design for regular use
- Flexible output options (stdout or file)

## Installation

### From Source

1. Clone or download this repository
2. Navigate to the project directory
3. Install using pip:

```bash
pip install .
```

### Development Installation

For development with editable installation:

```bash
pip install -e .
```

### From GitHub

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/hragbalian/pyfuncscribe.git
```

## Usage

### Basic Usage

Generate a report for the current directory and print to stdout:

```bash
pyfuncscribe
```

### Specify Root Directory

Scan a specific directory:

```bash
pyfuncscribe --root /path/to/your/project
# or
pyfuncscribe -r /path/to/your/project
```

### Save to File

Output the report to a markdown file:

```bash
pyfuncscribe --output report.md
# or
pyfuncscribe -o report.md
```

### Brief Docstrings

Include only the first line (summary) of docstrings:

```bash
pyfuncscribe --brief
# or
pyfuncscribe -b
```

### Combined Options

Scan a specific directory, use brief docstrings, and save to file:

```bash
pyfuncscribe -r src -b -o docs/api_reference.md
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--root` | `-r` | Root directory to start the search from | Current directory (`.`) |
| `--output` | `-o` | Output file path for the markdown report | stdout |
| `--brief` | `-b` | Include only the first line of docstrings | Full docstrings |
| `--version` | `-v` | Show version information | - |
| `--help` | `-h` | Show help message | - |

## Output Format

The generated markdown report includes:

1. **Header**: Total count of functions found
2. **Table of Contents**: Organized by directory structure
3. **Function Details**: For each function:
   - Function name (as heading)
   - File path and line number
   - Full signature with type hints
   - List of decorators (if any)
   - List of arguments with type annotations
   - Return type annotation (if present)
   - Async function indicator (if applicable)
   - Documentation (full or brief docstring)

### Example Output Structure

```markdown
# Python Functions Report

Total functions found: **15**

## Table of Contents

- [src/pyfuncscribe](#directory-srcpyfuncscribe)
  - [extract_functions](#extract_functions)
  - [generate_report](#generate_report)

## Directory: `src/pyfuncscribe`

### `extract_functions`

**File:** `src/pyfuncscribe/extractor.py:42`

**Signature:**
```python
def extract_functions(file_path: str) -> List[FunctionInfo]
```

**Arguments:**
- `file_path: str`

**Returns:** `List[FunctionInfo]`

**Documentation:**
> Extract all functions from a Python file.
```

## Use Cases

- Generate API documentation for your Python projects
- Create function inventories for code reviews
- Document legacy codebases
- Track function changes over time (by regularly regenerating reports)
- Onboard new team members with comprehensive function overviews

## Requirements

- Python 3.8 or higher
- No external dependencies (uses only Python standard library)

## Project Structure

```
pyfuncscribe/
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
└── src/
    └── pyfuncscribe/
        ├── __init__.py     # Package initialization
        ├── cli.py          # Command-line interface
        ├── extractor.py    # Function extraction logic
        └── reporter.py     # Markdown report generation
```

## How It Works

1. **Discovery**: The tool recursively walks through the specified directory tree to find all `.py` files
2. **Parsing**: Each Python file is parsed using Python's `ast` (Abstract Syntax Tree) module
3. **Extraction**: Function definitions are identified and detailed metadata is extracted
4. **Grouping**: Functions are organized by their directory structure
5. **Formatting**: The information is formatted into a clean, readable markdown document
6. **Output**: The report is either written to a file or printed to stdout

## License

MIT License

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## Tips

- Run `pyfuncscribe` regularly to keep your function documentation up to date
- Use the `--brief` flag for quick overviews and full docstrings for detailed documentation
- Combine with version control to track how your codebase functions evolve over time
- Use output redirection or the `-o` flag to save reports for future reference
