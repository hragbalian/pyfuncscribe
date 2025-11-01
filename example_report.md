# Python Functions Report

Total functions found: **17**

---

## Table of Contents

- [(root)](#directory-)
  - [__init__](#__init__)
  - [__init__](#__init__)
  - [_build_signature](#_build_signature)
  - [_extract_arguments](#_extract_arguments)
  - [_extract_function_info](#_extract_function_info)
  - [_format_function_section](#_format_function_section)
  - [_generate_description_with_llm](#_generate_description_with_llm)
  - [_get_docstring_summary](#_get_docstring_summary)
  - [_group_functions_by_directory](#_group_functions_by_directory)
  - [_has_content_changed](#_has_content_changed)
  - [_is_function_commented](#_is_function_commented)
  - [extract_all_functions](#extract_all_functions)
  - [extract_functions_from_file](#extract_functions_from_file)
  - [find_python_files](#find_python_files)
  - [generate_report](#generate_report)
  - [main](#main)
  - [parse_args](#parse_args)

---

## Directory: `(root)`

Functions in this directory: **17**

### `__init__`

**File:** `extractor.py:29`

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

**File:** `reporter.py:14`

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

**File:** `extractor.py:202`

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

**File:** `extractor.py:160`

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

**File:** `extractor.py:107`

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

**File:** `reporter.py:166`

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

**File:** `reporter.py:65`

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

**File:** `reporter.py:124`

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

**File:** `reporter.py:144`

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

### `_has_content_changed`

**File:** `reporter.py:23`

**Signature:**
```python
def _has_content_changed(self, existing_content: str, new_content_without_description: str) -> bool
```

**Arguments:**
- `self`
- `existing_content: str`
- `new_content_without_description: str`

**Returns:** `bool`

**Documentation:**
> Check if the report content has changed by comparing non-description sections.

---

### `_is_function_commented`

**File:** `extractor.py:54`

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

**File:** `extractor.py:224`

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

**File:** `extractor.py:73`

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

**File:** `extractor.py:40`

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

**File:** `reporter.py:237`

**Signature:**
```python
def generate_report(self, functions: List[FunctionInfo], add_description: bool, include_description: bool) -> str
```

**Arguments:**
- `self`
- `functions: List[FunctionInfo]`
- `add_description: bool`
- `include_description: bool`

**Returns:** `str`

**Documentation:**
> Generate a complete markdown report from function information.

---

### `main`

**File:** `cli.py:71`

**Signature:**
```python
def main() -> None
```

**Returns:** `None`

**Documentation:**
> Main entry point for the CLI tool.

---

### `parse_args`

**File:** `cli.py:11`

**Signature:**
```python
def parse_args() -> argparse.Namespace
```

**Returns:** `argparse.Namespace`

**Documentation:**
> Parse command-line arguments.

---
