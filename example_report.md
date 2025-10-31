# Python Functions Report

Total functions found: **14**

---

## Table of Contents

- [pyfuncscribe](#directory-pyfuncscribe)
  - [__init__](#__init__)
  - [__init__](#__init__)
  - [_build_signature](#_build_signature)
  - [_extract_arguments](#_extract_arguments)
  - [_extract_function_info](#_extract_function_info)
  - [_format_function_section](#_format_function_section)
  - [_get_docstring_summary](#_get_docstring_summary)
  - [_group_functions_by_directory](#_group_functions_by_directory)
  - [extract_all_functions](#extract_all_functions)
  - [extract_functions_from_file](#extract_functions_from_file)
  - [find_python_files](#find_python_files)
  - [generate_report](#generate_report)
  - [main](#main)
  - [parse_args](#parse_args)

---

## Directory: `pyfuncscribe`

Functions in this directory: **14**

### `__init__`

**File:** `pyfuncscribe/extractor.py:29`

**Signature:**
```python
def __init__(self, root_dir: str)
```

**Arguments:**
- `self`
- `root_dir: str`

**Documentation:**
```
Initialize the function extractor.

Args:
    root_dir: Root directory to start searching from
```

---

### `__init__`

**File:** `pyfuncscribe/reporter.py:12`

**Signature:**
```python
def __init__(self, brief_docstring: bool)
```

**Arguments:**
- `self`
- `brief_docstring: bool`

**Documentation:**
```
Initialize the markdown reporter.

Args:
    brief_docstring: If True, include only first line of docstring
```

---

### `_build_signature`

**File:** `pyfuncscribe/extractor.py:175`

**Signature:**
```python
def _build_signature(self, node: ast.FunctionDef) -> str
```

**Arguments:**
- `self`
- `node: ast.FunctionDef`

**Returns:** `str`

**Documentation:**
```
Build a complete function signature string.

Args:
    node: AST FunctionDef or AsyncFunctionDef node

Returns:
    Formatted function signature
```

---

### `_extract_arguments`

**File:** `pyfuncscribe/extractor.py:133`

**Signature:**
```python
def _extract_arguments(self, args: ast.arguments) -> List[str]
```

**Arguments:**
- `self`
- `args: ast.arguments`

**Returns:** `List[str]`

**Documentation:**
```
Extract argument names and annotations from function arguments.

Args:
    args: AST arguments node

Returns:
    List of formatted argument strings
```

---

### `_extract_function_info`

**File:** `pyfuncscribe/extractor.py:80`

**Signature:**
```python
def _extract_function_info(self, node: ast.FunctionDef, file_path: Path, content: str) -> Optional[FunctionInfo]
```

**Arguments:**
- `self`
- `node: ast.FunctionDef`
- `file_path: Path`
- `content: str`

**Returns:** `Optional[FunctionInfo]`

**Documentation:**
```
Extract detailed information from a function AST node.

Args:
    node: AST FunctionDef or AsyncFunctionDef node
    file_path: Path to the file containing the function
    content: Full file content for source extraction

Returns:
    FunctionInfo object or None if extraction fails
```

---

### `_format_function_section`

**File:** `pyfuncscribe/reporter.py:63`

**Signature:**
```python
def _format_function_section(self, func: FunctionInfo) -> str
```

**Arguments:**
- `self`
- `func: FunctionInfo`

**Returns:** `str`

**Documentation:**
```
Format a single function as a markdown section.

Args:
    func: FunctionInfo object

Returns:
    Markdown formatted string for the function
```

---

### `_get_docstring_summary`

**File:** `pyfuncscribe/reporter.py:21`

**Signature:**
```python
def _get_docstring_summary(self, docstring: str) -> str
```

**Arguments:**
- `self`
- `docstring: str`

**Returns:** `str`

**Documentation:**
```
Extract the first line (summary) from a docstring.

Args:
    docstring: The full docstring

Returns:
    First non-empty line of the docstring
```

---

### `_group_functions_by_directory`

**File:** `pyfuncscribe/reporter.py:41`

**Signature:**
```python
def _group_functions_by_directory(self, functions: List[FunctionInfo]) -> Dict[str, List[FunctionInfo]]
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`

**Returns:** `Dict[str, List[FunctionInfo]]`

**Documentation:**
```
Group functions by their directory path.

Args:
    functions: List of FunctionInfo objects

Returns:
    Dictionary mapping directory paths to lists of functions
```

---

### `extract_all_functions`

**File:** `pyfuncscribe/extractor.py:197`

**Signature:**
```python
def extract_all_functions(self) -> List[FunctionInfo]
```

**Arguments:**
- `self`

**Returns:** `List[FunctionInfo]`

**Documentation:**
```
Extract all functions from all Python files in the root directory.

Returns:
    List of all FunctionInfo objects found
```

---

### `extract_functions_from_file`

**File:** `pyfuncscribe/extractor.py:52`

**Signature:**
```python
def extract_functions_from_file(self, file_path: Path) -> List[FunctionInfo]
```

**Arguments:**
- `self`
- `file_path: Path`

**Returns:** `List[FunctionInfo]`

**Documentation:**
```
Extract all function definitions from a Python file.

Args:
    file_path: Path to the Python file

Returns:
    List of FunctionInfo objects
```

---

### `find_python_files`

**File:** `pyfuncscribe/extractor.py:38`

**Signature:**
```python
def find_python_files(self) -> List[Path]
```

**Arguments:**
- `self`

**Returns:** `List[Path]`

**Documentation:**
```
Recursively find all Python files in the root directory.

Returns:
    List of Path objects for Python files
```

---

### `generate_report`

**File:** `pyfuncscribe/reporter.py:134`

**Signature:**
```python
def generate_report(self, functions: List[FunctionInfo]) -> str
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`

**Returns:** `str`

**Documentation:**
```
Generate a complete markdown report from function information.

Args:
    functions: List of FunctionInfo objects

Returns:
    Complete markdown report as a string
```

---

### `main`

**File:** `pyfuncscribe/cli.py:57`

**Signature:**
```python
def main() -> None
```

**Returns:** `None`

**Documentation:**
```
Main entry point for the CLI tool.
```

---

### `parse_args`

**File:** `pyfuncscribe/cli.py:11`

**Signature:**
```python
def parse_args() -> argparse.Namespace
```

**Returns:** `argparse.Namespace`

**Documentation:**
```
Parse command-line arguments.

Returns:
    Parsed arguments namespace
```

---
