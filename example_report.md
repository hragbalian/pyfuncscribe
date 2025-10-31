# Python Functions Report

Total functions found: **16**

---

## Table of Contents

- [pyfuncscribe](#directory-pyfuncscribe)
  - [__init__](#__init__)
  - [__init__](#__init__)
  - [_build_signature](#_build_signature)
  - [_extract_arguments](#_extract_arguments)
  - [_extract_function_info](#_extract_function_info)
  - [_format_function_section](#_format_function_section)
  - [_generate_description_with_llm](#_generate_description_with_llm)
  - [_get_docstring_summary](#_get_docstring_summary)
  - [_group_functions_by_directory](#_group_functions_by_directory)
  - [_is_function_commented](#_is_function_commented)
  - [extract_all_functions](#extract_all_functions)
  - [extract_functions_from_file](#extract_functions_from_file)
  - [find_python_files](#find_python_files)
  - [generate_report](#generate_report)
  - [main](#main)
  - [parse_args](#parse_args)

---

## Directory: `pyfuncscribe`

Functions in this directory: **16**

### `__init__`

**File:** `pyfuncscribe/extractor.py:29`

**Signature:**
```python
def __init__(self, root_dir: str, include_commented: bool)
```

**Arguments:**
- `self`
- `root_dir: str`
- `include_commented: bool`

**Documentation:**
> Initialize the function extractor.

---

### `__init__`

**File:** `pyfuncscribe/reporter.py:14`

**Signature:**
```python
def __init__(self, brief_docstring: bool)
```

**Arguments:**
- `self`
- `brief_docstring: bool`

**Documentation:**
> Initialize the markdown reporter.

---

### `_build_signature`

**File:** `pyfuncscribe/extractor.py:202`

**Signature:**
```python
def _build_signature(self, node: ast.FunctionDef) -> str
```

**Arguments:**
- `self`
- `node: ast.FunctionDef`

**Returns:** `str`

**Documentation:**
> Build a complete function signature string.

---

### `_extract_arguments`

**File:** `pyfuncscribe/extractor.py:160`

**Signature:**
```python
def _extract_arguments(self, args: ast.arguments) -> List[str]
```

**Arguments:**
- `self`
- `args: ast.arguments`

**Returns:** `List[str]`

**Documentation:**
> Extract argument names and annotations from function arguments.

---

### `_extract_function_info`

**File:** `pyfuncscribe/extractor.py:107`

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
> Extract detailed information from a function AST node.

---

### `_format_function_section`

**File:** `pyfuncscribe/reporter.py:124`

**Signature:**
```python
def _format_function_section(self, func: FunctionInfo) -> str
```

**Arguments:**
- `self`
- `func: FunctionInfo`

**Returns:** `str`

**Documentation:**
> Format a single function as a markdown section.

---

### `_generate_description_with_llm`

**File:** `pyfuncscribe/reporter.py:23`

**Signature:**
```python
def _generate_description_with_llm(self, functions: List[FunctionInfo]) -> Optional[str]
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`

**Returns:** `Optional[str]`

**Documentation:**
> Generate a description of the codebase using Claude API.

---

### `_get_docstring_summary`

**File:** `pyfuncscribe/reporter.py:82`

**Signature:**
```python
def _get_docstring_summary(self, docstring: str) -> str
```

**Arguments:**
- `self`
- `docstring: str`

**Returns:** `str`

**Documentation:**
> Extract the first line (summary) from a docstring.

---

### `_group_functions_by_directory`

**File:** `pyfuncscribe/reporter.py:102`

**Signature:**
```python
def _group_functions_by_directory(self, functions: List[FunctionInfo]) -> Dict[str, List[FunctionInfo]]
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`

**Returns:** `Dict[str, List[FunctionInfo]]`

**Documentation:**
> Group functions by their directory path.

---

### `_is_function_commented`

**File:** `pyfuncscribe/extractor.py:54`

**Signature:**
```python
def _is_function_commented(self, content: str, line_number: int) -> bool
```

**Arguments:**
- `self`
- `content: str`
- `line_number: int`

**Returns:** `bool`

**Documentation:**
> Check if a function definition is commented out.

---

### `extract_all_functions`

**File:** `pyfuncscribe/extractor.py:224`

**Signature:**
```python
def extract_all_functions(self) -> List[FunctionInfo]
```

**Arguments:**
- `self`

**Returns:** `List[FunctionInfo]`

**Documentation:**
> Extract all functions from all Python files in the root directory.

---

### `extract_functions_from_file`

**File:** `pyfuncscribe/extractor.py:73`

**Signature:**
```python
def extract_functions_from_file(self, file_path: Path) -> List[FunctionInfo]
```

**Arguments:**
- `self`
- `file_path: Path`

**Returns:** `List[FunctionInfo]`

**Documentation:**
> Extract all function definitions from a Python file.

---

### `find_python_files`

**File:** `pyfuncscribe/extractor.py:40`

**Signature:**
```python
def find_python_files(self) -> List[Path]
```

**Arguments:**
- `self`

**Returns:** `List[Path]`

**Documentation:**
> Recursively find all Python files in the root directory.

---

### `generate_report`

**File:** `pyfuncscribe/reporter.py:195`

**Signature:**
```python
def generate_report(self, functions: List[FunctionInfo], add_description: bool) -> str
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`
- `add_description: bool`

**Returns:** `str`

**Documentation:**
> Generate a complete markdown report from function information.

---

### `main`

**File:** `pyfuncscribe/cli.py:71`

**Signature:**
```python
def main() -> None
```

**Returns:** `None`

**Documentation:**
> Main entry point for the CLI tool.

---

### `parse_args`

**File:** `pyfuncscribe/cli.py:11`

**Signature:**
```python
def parse_args() -> argparse.Namespace
```

**Returns:** `argparse.Namespace`

**Documentation:**
> Parse command-line arguments.

---
