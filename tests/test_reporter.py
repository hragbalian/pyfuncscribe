"""Tests for the MarkdownReporter class."""

from pyfuncscribe.extractor import FunctionInfo
from pyfuncscribe.reporter import MarkdownReporter


class TestMarkdownReporterBasics:
    """Test basic report generation functionality."""

    def test_generate_report_with_functions(self, sample_functions):
        """Test that report is generated with functions."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "# Python Functions Report" in report
        assert "Total functions found: **2**" in report
        assert "test_function_1" in report
        assert "test_function_2" in report

    def test_generate_report_empty_functions(self):
        """Test report generation with no functions."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report([], add_description=False)

        assert "# Python Functions Report" in report
        assert "Total functions found: **0**" in report

    def test_brief_docstring_mode(self, sample_functions):
        """Test that brief mode only shows first line of docstring."""
        reporter = MarkdownReporter(brief_docstring=True)
        report = reporter.generate_report(sample_functions, add_description=False)

        # Brief mode should have > in the docstring lines (blockquote format)
        assert "> This is a test function." in report
        assert "> Another test function." in report

    def test_full_docstring_mode(self, sample_functions):
        """Test that full mode shows complete docstring."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        # Full mode should have code block for docstrings
        assert "```" in report
        assert "This is a test function." in report

    def test_table_of_contents_generation(self, sample_functions):
        """Test that table of contents is generated."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "## Table of Contents" in report
        assert "test_function_1" in report
        assert "test_function_2" in report

    def test_include_description_parameter(self, sample_functions):
        """Test include_description parameter."""
        reporter = MarkdownReporter(brief_docstring=False)

        report_with_desc = reporter.generate_report(
            sample_functions, add_description=False, include_description=True
        )
        report_without_desc = reporter.generate_report(
            sample_functions, add_description=False, include_description=False
        )

        # Both should be similar in length and content (no description was added)
        assert "test_function_1" in report_with_desc
        assert "test_function_1" in report_without_desc


class TestDiffDetection:
    """Test the _has_content_changed method."""

    def test_identical_reports_no_change(self, sample_functions):
        """Test that identical reports are detected as no change."""
        reporter = MarkdownReporter(brief_docstring=True)
        report1 = reporter.generate_report(sample_functions, add_description=False)
        report2 = reporter.generate_report(sample_functions, add_description=False)

        has_changed = reporter._has_content_changed(report1, report2)
        assert has_changed is False

    def test_different_function_count_detected(self, sample_functions):
        """Test that different function counts are detected."""
        reporter = MarkdownReporter(brief_docstring=True)
        report_2_funcs = reporter.generate_report(
            sample_functions, add_description=False
        )
        report_1_func = reporter.generate_report(
            sample_functions[:1], add_description=False
        )

        has_changed = reporter._has_content_changed(report_2_funcs, report_1_func)
        assert has_changed is True

    def test_report_with_description_vs_without(self, sample_functions):
        """Test that description is ignored in comparison."""
        reporter = MarkdownReporter(brief_docstring=True)
        base_report = reporter.generate_report(
            sample_functions, add_description=False, include_description=False
        )

        # Create a report with a fake description
        fake_description = """## Description

This is a fake LLM-generated description.

---

"""
        lines = base_report.split("\n")
        report_with_desc = (
            "\n".join(lines[:2]) + "\n\n" + fake_description + "\n".join(lines[2:])
        )

        # These should be detected as having NO changes (description ignored)
        has_changed = reporter._has_content_changed(report_with_desc, base_report)
        assert has_changed is False

    def test_different_content_detected(self, sample_functions):
        """Test that actual content changes are detected."""
        reporter = MarkdownReporter(brief_docstring=True)
        report = reporter.generate_report(sample_functions, add_description=False)

        # Modify the function count
        modified_report = report.replace("**2**", "**3**")

        has_changed = reporter._has_content_changed(report, modified_report)
        assert has_changed is True

    def test_different_function_name_detected(self, sample_functions):
        """Test that different function names are detected."""
        reporter = MarkdownReporter(brief_docstring=True)
        report = reporter.generate_report(sample_functions, add_description=False)

        # Change function name in table of contents
        modified_report = report.replace("test_function_1", "modified_function")

        has_changed = reporter._has_content_changed(report, modified_report)
        assert has_changed is True

    def test_whitespace_normalization(self):
        """Test that whitespace differences are normalized."""
        reporter = MarkdownReporter(brief_docstring=False)

        report1 = """# Python Functions Report

Total functions found: **2**

---

## Table of Contents
- test_function_1
"""

        # Same content but with extra whitespace
        report2 = """# Python Functions Report

Total functions found: **2**

---

## Table of Contents

- test_function_1
"""

        has_changed = reporter._has_content_changed(report1, report2)
        # Should be False since normalized whitespace is the same
        assert has_changed is False


class TestFunctionFormatting:
    """Test function formatting in reports."""

    def test_function_signature_included(self, sample_functions):
        """Test that function signatures are included."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "def test_function_1(x: int) -> str:" in report
        assert "async def test_function_2() -> None:" in report

    def test_decorators_displayed(self, sample_functions):
        """Test that decorators are displayed."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "@property" in report

    def test_async_flag_displayed(self, sample_functions):
        """Test that async flag is displayed."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "**Type:** Async function" in report

    def test_arguments_listed(self, sample_functions):
        """Test that function arguments are listed."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "**Arguments:**" in report
        assert "- `self`" in report
        assert "- `x: int`" in report

    def test_return_type_displayed(self, sample_functions):
        """Test that return types are displayed."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "**Returns:** `str`" in report
        assert "**Returns:** `None`" in report

    def test_file_location_displayed(self, sample_functions):
        """Test that file locations are displayed."""
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(sample_functions, add_description=False)

        assert "**File:** `test_file.py:10`" in report
        assert "**File:** `test_file.py:20`" in report


class TestGroupingByDirectory:
    """Test function grouping by directory."""

    def test_functions_grouped_by_directory(self):
        """Test that functions are grouped by directory."""
        functions = [
            FunctionInfo(
                name="func_root",
                docstring="Root function",
                file_path="root.py",
                directory=".",
                signature="def func_root():",
                line_number=1,
                arguments=[],
                return_annotation=None,
                decorators=[],
                is_async=False,
            ),
            FunctionInfo(
                name="func_sub",
                docstring="Sub function",
                file_path="subdir/sub.py",
                directory="subdir",
                signature="def func_sub():",
                line_number=1,
                arguments=[],
                return_annotation=None,
                decorators=[],
                is_async=False,
            ),
        ]

        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(functions, add_description=False)

        assert "## Directory: `(root)`" in report or "## Directory: `.`" in report
        assert "## Directory: `subdir`" in report
        assert "func_root" in report
        assert "func_sub" in report

    def test_functions_sorted_within_directory(self):
        """Test that functions are sorted alphabetically within directories."""
        functions = [
            FunctionInfo(
                name="zebra_func",
                docstring="Z function",
                file_path="test.py",
                directory=".",
                signature="def zebra_func():",
                line_number=1,
                arguments=[],
                return_annotation=None,
                decorators=[],
                is_async=False,
            ),
            FunctionInfo(
                name="alpha_func",
                docstring="A function",
                file_path="test.py",
                directory=".",
                signature="def alpha_func():",
                line_number=2,
                arguments=[],
                return_annotation=None,
                decorators=[],
                is_async=False,
            ),
        ]

        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(functions, add_description=False)

        # Find positions of function names
        pos_alpha = report.find("alpha_func")
        pos_zebra = report.find("zebra_func")

        # alpha should come before zebra
        assert pos_alpha < pos_zebra
