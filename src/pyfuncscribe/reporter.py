"""Module for generating markdown reports from function information."""

from collections import defaultdict
from typing import Dict, List

from .extractor import FunctionInfo


class MarkdownReporter:
    """Generate markdown reports from extracted function information."""

    def __init__(self, brief_docstring: bool = False):
        """
        Initialize the markdown reporter.

        Args:
            brief_docstring: If True, include only first line of docstring
        """
        self.brief_docstring = brief_docstring

    def _get_docstring_summary(self, docstring: str) -> str:
        """
        Extract the first line (summary) from a docstring.

        Args:
            docstring: The full docstring

        Returns:
            First non-empty line of the docstring
        """
        if not docstring:
            return ""

        lines = docstring.strip().split("\n")
        for line in lines:
            stripped = line.strip()
            if stripped:
                return stripped
        return ""

    def _group_functions_by_directory(
        self, functions: List[FunctionInfo]
    ) -> Dict[str, List[FunctionInfo]]:
        """
        Group functions by their directory path.

        Args:
            functions: List of FunctionInfo objects

        Returns:
            Dictionary mapping directory paths to lists of functions
        """
        grouped = defaultdict(list)
        for func in functions:
            grouped[func.directory].append(func)

        # Sort functions within each directory by name
        for directory in grouped:
            grouped[directory].sort(key=lambda f: f.name)

        return dict(grouped)

    def _format_function_section(self, func: FunctionInfo) -> str:
        """
        Format a single function as a markdown section.

        Args:
            func: FunctionInfo object

        Returns:
            Markdown formatted string for the function
        """
        lines = []

        # Function header
        lines.append(f"### `{func.name}`")
        lines.append("")

        # File location
        lines.append(f"**File:** `{func.file_path}:{func.line_number}`")
        lines.append("")

        # Signature
        lines.append("**Signature:**")
        lines.append("```python")
        lines.append(func.signature)
        lines.append("```")
        lines.append("")

        # Decorators
        if func.decorators:
            lines.append("**Decorators:**")
            for decorator in func.decorators:
                lines.append(f"- `@{decorator}`")
            lines.append("")

        # Arguments
        if func.arguments:
            lines.append("**Arguments:**")
            for arg in func.arguments:
                lines.append(f"- `{arg}`")
            lines.append("")

        # Return type
        if func.return_annotation:
            lines.append(f"**Returns:** `{func.return_annotation}`")
            lines.append("")

        # Async flag
        if func.is_async:
            lines.append("**Type:** Async function")
            lines.append("")

        # Docstring
        if func.docstring:
            lines.append("**Documentation:**")
            if self.brief_docstring:
                summary = self._get_docstring_summary(func.docstring)
                lines.append(f"> {summary}")
            else:
                lines.append("```")
                lines.append(func.docstring)
                lines.append("```")
            lines.append("")
        else:
            lines.append("**Documentation:** No docstring provided")
            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def generate_report(self, functions: List[FunctionInfo]) -> str:
        """
        Generate a complete markdown report from function information.

        Args:
            functions: List of FunctionInfo objects

        Returns:
            Complete markdown report as a string
        """
        lines = []

        # Report header
        lines.append("# Python Functions Report")
        lines.append("")
        lines.append(f"Total functions found: **{len(functions)}**")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Group functions by directory
        grouped = self._group_functions_by_directory(functions)

        # Sort directories alphabetically
        sorted_dirs = sorted(grouped.keys())

        # Generate table of contents
        lines.append("## Table of Contents")
        lines.append("")
        for directory in sorted_dirs:
            funcs = grouped[directory]
            dir_display = directory if directory != "." else "(root)"
            lines.append(
                f"- [{dir_display}](#directory-{directory.replace('/', '').replace('.', '')})"
            )
            for func in funcs:
                lines.append(f"  - [{func.name}](#{func.name.lower()})")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Generate sections for each directory
        for directory in sorted_dirs:
            funcs = grouped[directory]
            dir_display = directory if directory != "." else "(root)"

            # Directory header
            lines.append(f"## Directory: `{dir_display}`")
            lines.append("")
            lines.append(f"Functions in this directory: **{len(funcs)}**")
            lines.append("")

            # Function sections
            for func in funcs:
                lines.append(self._format_function_section(func))

        return "\n".join(lines)
