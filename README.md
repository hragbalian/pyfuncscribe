# PyFuncScribe

A simple, efficient Python CLI tool that generates comprehensive markdown reports of Python functions found in a codebase.

## Features

- Recursively traverses directories to find all Python files
- **Automatically ignores commented-out code** with option to include it
- **Optional LLM-generated codebase descriptions** using Claude API
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
- **Automated semantic versioning** via GitHub Actions

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

### Include Commented-Out Code

By default, commented-out functions are ignored. To include them:

```bash
pyfuncscribe --include-commented
# or
pyfuncscribe -c
```

### Add LLM-Generated Description

Generate a description of your codebase using Claude AI (requires `ANTHROPIC_API_KEY` environment variable):

```bash
export ANTHROPIC_API_KEY="your-api-key"
pyfuncscribe --add-description -o report.md
# or
pyfuncscribe -d -o report.md
```

### Create Empty Reports

By default, if no functions are found, no report file is created and a message is printed. To create a report even when no functions are found:

```bash
pyfuncscribe --include-empty
# or
pyfuncscribe --include-empty -o report.md
```

This is useful for CI/CD pipelines or documentation systems that expect a report file to always exist.

### Combined Options

Scan a specific directory, include commented code, add AI description, use brief docstrings, and save to file:

```bash
pyfuncscribe -r src -c -d -b -o docs/api_reference.md
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--root` | `-r` | Root directory to start the search from | Current directory (`.`) |
| `--output` | `-o` | Output file path for the markdown report | stdout |
| `--brief` | `-b` | Include only the first line of docstrings | Full docstrings |
| `--include-commented` | `-c` | Include functions that are commented out | Ignore commented code |
| `--add-description` | `-d` | Add LLM-generated description (requires `ANTHROPIC_API_KEY`) | No description |
| `--include-empty` | - | Create a report even if no functions are found | Don't create report if empty |
| `--recursive` | - | Recursively search subdirectories for Python files | Enabled by default |
| `--no-recursive` | - | Only search the specified directory (no subdirectories) | - |
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
- `anthropic` package (optional, only required for `--add-description` feature)

### Installing Optional Dependencies

For LLM-generated descriptions:

```bash
pip install anthropic
```

Or install with optional dependencies:

```bash
pip install pyfuncscribe[ai]
```

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
- The `--add-description` feature provides a high-level overview perfect for README files or project documentation
- By default, commented-out code is ignored to keep reports clean and focused on active code
- Use `--include-empty` when integrating with CI/CD pipelines that expect a report file to always be generated
- Use `--no-recursive` to generate reports for a single directory without traversing subdirectories

## Semantic Versioning

This project uses semantic versioning with automated releases via GitHub Actions. Version bumps are determined by commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `BREAKING CHANGE:` - Breaking change (major version bump)
- `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `chore:` - No version bump

Example commit messages:
```bash
git commit -m "feat: add support for async generators"
git commit -m "fix: handle empty docstrings correctly"
git commit -m "docs: update installation instructions"
```
