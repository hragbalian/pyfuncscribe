"""Core module for extracting function information from Python files."""

import ast
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class FunctionInfo:
    """Data class to hold information about a Python function."""

    name: str
    docstring: Optional[str]
    file_path: str
    directory: str
    signature: str
    line_number: int
    arguments: List[str]
    return_annotation: Optional[str]
    decorators: List[str]
    is_async: bool


class FunctionExtractor:
    """Extract function information from Python files."""

    def __init__(
        self,
        root_dir: str = ".",
        include_commented: bool = False,
        recursive: bool = True,
    ):
        """
        Initialize the function extractor.

        Args:
            root_dir: Root directory to start searching from
            include_commented: If True, include functions that are commented out
            recursive: If True, recursively search subdirectories; if False, only search root directory
        """
        self.root_dir = Path(root_dir).resolve()
        self.include_commented = include_commented
        self.recursive = recursive

    def find_python_files(self) -> List[Path]:
        """
        Find all Python files in the root directory.

        If recursive is True, searches recursively through subdirectories.
        If recursive is False, only searches the root directory.

        Returns:
            List of Path objects for Python files
        """
        python_files = []

        if self.recursive:
            # Recursively search all subdirectories
            for root, _, files in os.walk(self.root_dir):
                for file in files:
                    if file.endswith(".py"):
                        python_files.append(Path(root) / file)
        else:
            # Only search the root directory (non-recursive)
            for file in self.root_dir.iterdir():
                if file.is_file() and file.name.endswith(".py"):
                    python_files.append(file)

        return sorted(python_files)

    def _is_function_commented(self, content: str, line_number: int) -> bool:
        """
        Check if a function definition is commented out.

        Args:
            content: Full file content
            line_number: Line number where function starts (1-indexed)

        Returns:
            True if the function definition line is commented out
        """
        lines = content.split("\n")
        if line_number < 1 or line_number > len(lines):
            return False

        # Get the line (convert to 0-indexed)
        line = lines[line_number - 1].lstrip()
        return line.startswith("#")

    def extract_functions_from_file(self, file_path: Path) -> List[FunctionInfo]:
        """
        Extract all function definitions from a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            List of FunctionInfo objects
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Skip commented functions unless explicitly included
                    if not self.include_commented and self._is_function_commented(
                        content, node.lineno
                    ):
                        continue

                    func_info = self._extract_function_info(node, file_path, content)
                    if func_info:
                        functions.append(func_info)

            return functions
        except (SyntaxError, UnicodeDecodeError):
            # Skip files that can't be parsed
            return []

    def _extract_function_info(
        self, node: ast.FunctionDef, file_path: Path, content: str
    ) -> Optional[FunctionInfo]:
        """
        Extract detailed information from a function AST node.

        Args:
            node: AST FunctionDef or AsyncFunctionDef node
            file_path: Path to the file containing the function
            content: Full file content for source extraction

        Returns:
            FunctionInfo object or None if extraction fails
        """
        try:
            # Extract docstring
            docstring = ast.get_docstring(node)

            # Extract arguments
            arguments = self._extract_arguments(node.args)

            # Extract return annotation
            return_annotation = None
            if node.returns:
                return_annotation = ast.unparse(node.returns)

            # Extract decorators
            decorators = [ast.unparse(dec) for dec in node.decorator_list]

            # Build signature
            signature = self._build_signature(node)

            # Get relative path for cleaner output
            try:
                rel_path = file_path.relative_to(self.root_dir)
            except ValueError:
                rel_path = file_path

            return FunctionInfo(
                name=node.name,
                docstring=docstring,
                file_path=str(rel_path),
                directory=str(rel_path.parent),
                signature=signature,
                line_number=node.lineno,
                arguments=arguments,
                return_annotation=return_annotation,
                decorators=decorators,
                is_async=isinstance(node, ast.AsyncFunctionDef),
            )
        except Exception:
            return None

    def _extract_arguments(self, args: ast.arguments) -> List[str]:
        """
        Extract argument names and annotations from function arguments.

        Args:
            args: AST arguments node

        Returns:
            List of formatted argument strings
        """
        arg_strs = []

        # Regular arguments
        for arg in args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            arg_strs.append(arg_str)

        # *args
        if args.vararg:
            arg_str = f"*{args.vararg.arg}"
            if args.vararg.annotation:
                arg_str += f": {ast.unparse(args.vararg.annotation)}"
            arg_strs.append(arg_str)

        # Keyword-only arguments
        for arg in args.kwonlyargs:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            arg_strs.append(arg_str)

        # **kwargs
        if args.kwarg:
            arg_str = f"**{args.kwarg.arg}"
            if args.kwarg.annotation:
                arg_str += f": {ast.unparse(args.kwarg.annotation)}"
            arg_strs.append(arg_str)

        return arg_strs

    def _build_signature(self, node: ast.FunctionDef) -> str:
        """
        Build a complete function signature string.

        Args:
            node: AST FunctionDef or AsyncFunctionDef node

        Returns:
            Formatted function signature
        """
        async_prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""

        # Extract arguments
        args_str = ", ".join(self._extract_arguments(node.args))

        # Add return annotation if present
        return_str = ""
        if node.returns:
            return_str = f" -> {ast.unparse(node.returns)}"

        return f"{async_prefix}def {node.name}({args_str}){return_str}"

    def extract_all_functions(self) -> List[FunctionInfo]:
        """
        Extract all functions from all Python files in the root directory.

        Returns:
            List of all FunctionInfo objects found
        """
        all_functions = []
        python_files = self.find_python_files()

        for file_path in python_files:
            functions = self.extract_functions_from_file(file_path)
            all_functions.extend(functions)

        return all_functions
