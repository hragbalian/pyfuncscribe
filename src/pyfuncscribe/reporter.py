"""Module for generating markdown reports from function information."""

import os
import sys
from collections import defaultdict
from typing import Dict, List, Optional

from .extractor import DataclassInfo, FunctionInfo


class MarkdownReporter:
    """Generate markdown reports from extracted function information."""

    def __init__(self, brief_docstring: bool = False):
        """
        Initialize the markdown reporter.

        Args:
            brief_docstring: If True, include only first line of docstring
        """
        self.brief_docstring = brief_docstring

    def _has_content_changed(
        self, existing_content: str, new_content_without_description: str
    ) -> bool:
        """
        Check if the report content has changed by comparing non-description sections.

        Args:
            existing_content: The existing report file content
            new_content_without_description: The newly generated report without LLM description

        Returns:
            True if content has changed, False otherwise
        """
        # Extract the comparable parts by removing headers and descriptions
        # We want to compare from "Total functions found" onwards to catch all changes
        existing_lines = existing_content.strip().split("\n")
        new_lines = new_content_without_description.strip().split("\n")

        # Find the start of actual content (at "Total functions found")
        # This works for both files with and without LLM description
        existing_content_start = 0
        for i, line in enumerate(existing_lines):
            if "Total functions found:" in line:
                existing_content_start = i
                break

        new_content_start = 0
        for i, line in enumerate(new_lines):
            if "Total functions found:" in line:
                new_content_start = i
                break

        # Extract the content from "Total functions found" onwards
        existing_comparable = "\n".join(existing_lines[existing_content_start:])
        new_comparable = "\n".join(new_lines[new_content_start:])

        # Normalize whitespace for comparison
        existing_normalized = " ".join(existing_comparable.split())
        new_normalized = " ".join(new_comparable.split())

        return existing_normalized != new_normalized

    def _generate_description_with_llm(self, items: List) -> Optional[str]:
        """
        Generate a description of the codebase using Claude API.

        Args:
            functions: List of FunctionInfo objects

        Returns:
            Generated description or None if API key is not available
        """
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print(
                "Warning: ANTHROPIC_API_KEY environment variable not set. Skipping description generation.",
                file=sys.stderr,
            )
            return None

        try:
            from anthropic import Anthropic

            client = Anthropic(api_key=api_key)

            # Create a summary of functions and dataclasses for the LLM
            item_summary = []
            for item in items[:50]:  # Limit to first 50 items to manage token usage
                item_type = (
                    "function" if isinstance(item, FunctionInfo) else "dataclass"
                )
                item_summary.append(
                    f"- {item_type} {item.name} in {item.file_path}: {item.docstring[:100] if item.docstring else 'No docstring'}"
                )

            prompt = f"""Based on the following Python functions and dataclasses found in a codebase, write a brief 2-3 sentence description of what this codebase does. Focus on the main purpose and functionality.

Items found ({len(items)} total, showing first 50):
{chr(10).join(item_summary)}

Provide only the description, no additional commentary."""

            message = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=20000,
                messages=[{"role": "user", "content": prompt}],
            )

            return message.content[0].text.strip()

        except ImportError:
            print(
                "Warning: anthropic package not installed. Install with: pip install anthropic",
                file=sys.stderr,
            )
            return None
        except Exception as e:
            print(f"Warning: Failed to generate description: {e}", file=sys.stderr)
            return None

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

    def _group_dataclasses_by_directory(
        self, dataclasses: List[DataclassInfo]
    ) -> Dict[str, List[DataclassInfo]]:
        """
        Group dataclasses by their directory path.

        Args:
            dataclasses: List of DataclassInfo objects

        Returns:
            Dictionary mapping directory paths to lists of dataclasses
        """
        grouped = defaultdict(list)
        for dc in dataclasses:
            grouped[dc.directory].append(dc)

        # Sort dataclasses within each directory by name
        for directory in grouped:
            grouped[directory].sort(key=lambda d: d.name)

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

    def _format_dataclass_section(self, dataclass: DataclassInfo) -> str:
        """
        Format a single dataclass as a markdown section.

        Args:
            dataclass: DataclassInfo object

        Returns:
            Markdown formatted string for the dataclass
        """
        lines = []

        # Dataclass header
        lines.append(f"### `{dataclass.name}`")
        lines.append("")

        # File location
        lines.append(f"**File:** `{dataclass.file_path}:{dataclass.line_number}`")
        lines.append("")

        # Signature
        lines.append("**Signature:**")
        lines.append("```python")
        lines.append(dataclass.signature)
        lines.append("```")
        lines.append("")

        # Decorators
        if dataclass.decorators:
            lines.append("**Decorators:**")
            for decorator in dataclass.decorators:
                lines.append(f"- `@{decorator}`")
            lines.append("")

        # Fields
        if dataclass.fields:
            lines.append("**Fields:**")
            for field in dataclass.fields:
                lines.append(f"- `{field}`")
            lines.append("")

        # Docstring
        if dataclass.docstring:
            lines.append("**Documentation:**")
            if self.brief_docstring:
                summary = self._get_docstring_summary(dataclass.docstring)
                lines.append(f"> {summary}")
            else:
                lines.append("```")
                lines.append(dataclass.docstring)
                lines.append("```")
            lines.append("")
        else:
            lines.append("**Documentation:** No docstring provided")
            lines.append("")

        lines.append("---")
        lines.append("")

        return "\n".join(lines)

    def generate_report(
        self,
        functions: List[FunctionInfo],
        add_description: bool = False,
        include_description: bool = True,
        dataclasses: Optional[List[DataclassInfo]] = None,
    ) -> str:
        """
        Generate a complete markdown report from function information.

        Args:
            functions: List of FunctionInfo objects
            add_description: If True, add an LLM-generated description
            include_description: If False, skip adding the description (used for content comparison)
            dataclasses: Optional list of DataclassInfo objects

        Returns:
            Complete markdown report as a string
        """
        if dataclasses is None:
            dataclasses = []

        lines = []

        # Report header
        lines.append("# Python Functions Report")
        lines.append("")

        # Add LLM-generated description if requested
        if add_description and include_description:
            description = self._generate_description_with_llm(functions + dataclasses)
            if description:
                lines.append("## Description")
                lines.append("")
                lines.append(description)
                lines.append("")
                lines.append("---")
                lines.append("")

        # Count and report
        lines.append(f"Total functions found: **{len(functions)}**")
        if dataclasses:
            lines.append(f"Total dataclasses found: **{len(dataclasses)}**")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Group functions by directory
        grouped = self._group_functions_by_directory(functions)

        # Group dataclasses by directory
        grouped_dataclasses = self._group_dataclasses_by_directory(dataclasses)

        # Sort directories alphabetically
        sorted_dirs = sorted(
            set(list(grouped.keys()) + list(grouped_dataclasses.keys()))
        )

        # Generate table of contents
        lines.append("## Table of Contents")
        lines.append("")
        for directory in sorted_dirs:
            funcs = grouped.get(directory, [])
            dcs = grouped_dataclasses.get(directory, [])
            dir_display = directory if directory != "." else "(root)"
            lines.append(
                f"- [{dir_display}](#directory-{directory.replace('/', '').replace('.', '')})"
            )
            for func in funcs:
                lines.append(f"  - [{func.name}](#{func.name.lower()})")
            for dc in dcs:
                lines.append(f"  - [{dc.name}](#{dc.name.lower()})")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Generate sections for each directory
        for directory in sorted_dirs:
            funcs = grouped.get(directory, [])
            dcs = grouped_dataclasses.get(directory, [])
            dir_display = directory if directory != "." else "(root)"

            # Directory header
            lines.append(f"## Directory: `{dir_display}`")
            lines.append("")
            lines.append(f"Functions in this directory: **{len(funcs)}**")
            if dcs:
                lines.append(f"Dataclasses in this directory: **{len(dcs)}**")
            lines.append("")

            # Function sections
            for func in funcs:
                lines.append(self._format_function_section(func))

            # Dataclass sections
            for dc in dcs:
                lines.append(self._format_dataclass_section(dc))

        return "\n".join(lines)
