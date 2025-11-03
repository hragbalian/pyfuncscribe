"""Tests for the MarkdownReporter class."""

from pyfuncscribe.extractor import DataclassInfo, FunctionInfo
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


class TestDataclassReporting:
    """Test dataclass reporting functionality."""

    def test_generate_report_with_dataclasses(self):
        """Test that report is generated with dataclasses."""
        dataclasses = [
            DataclassInfo(
                name="Person",
                docstring="A person record.",
                file_path="models.py",
                directory=".",
                signature="class Person()",
                line_number=5,
                fields=["name: str", "age: int"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "# Python Functions Report" in report
        assert "Total dataclasses found: **1**" in report
        assert "Person" in report
        assert "name: str" in report
        assert "age: int" in report

    def test_generate_report_with_functions_and_dataclasses(self, sample_functions):
        """Test report with both functions and dataclasses."""
        dataclasses = [
            DataclassInfo(
                name="Address",
                docstring="An address.",
                file_path="models.py",
                directory=".",
                signature="class Address()",
                line_number=10,
                fields=["street: str", "city: str"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            sample_functions, add_description=False, dataclasses=dataclasses
        )

        assert "Total functions found: **2**" in report
        assert "Total dataclasses found: **1**" in report
        assert "test_function_1" in report
        assert "Address" in report

    def test_dataclass_fields_displayed(self):
        """Test that dataclass fields are displayed."""
        dataclasses = [
            DataclassInfo(
                name="Product",
                docstring="A product.",
                file_path="models.py",
                directory=".",
                signature="class Product()",
                line_number=1,
                fields=["name: str", "price: float", "quantity: int"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "**Fields:**" in report
        assert "- `name: str`" in report
        assert "- `price: float`" in report
        assert "- `quantity: int`" in report

    def test_dataclass_in_table_of_contents(self):
        """Test that dataclasses appear in table of contents."""
        dataclasses = [
            DataclassInfo(
                name="User",
                docstring="A user.",
                file_path="models.py",
                directory=".",
                signature="class User()",
                line_number=1,
                fields=["id: int", "name: str"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "## Table of Contents" in report
        assert "[User]" in report
        assert "#user" in report.lower()

    def test_dataclass_signature_included(self):
        """Test that dataclass signatures are included."""
        dataclasses = [
            DataclassInfo(
                name="Config",
                docstring="Configuration.",
                file_path="config.py",
                directory=".",
                signature="class Config()",
                line_number=1,
                fields=["debug: bool"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "class Config()" in report

    def test_dataclass_decorators_displayed(self):
        """Test that dataclass decorators are displayed."""
        dataclasses = [
            DataclassInfo(
                name="Settings",
                docstring="Settings.",
                file_path="settings.py",
                directory=".",
                signature="class Settings()",
                line_number=1,
                fields=["timeout: int"],
                decorators=["@dataclass", "@frozen"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "**Decorators:**" in report
        assert "@dataclass" in report
        assert "@frozen" in report

    def test_dataclass_file_location_displayed(self):
        """Test that dataclass file locations are displayed."""
        dataclasses = [
            DataclassInfo(
                name="Schema",
                docstring="Schema.",
                file_path="schema.py",
                directory=".",
                signature="class Schema()",
                line_number=42,
                fields=["version: str"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "**File:** `schema.py:42`" in report

    def test_dataclass_docstring_displayed(self):
        """Test that dataclass docstrings are displayed."""
        dataclasses = [
            DataclassInfo(
                name="Status",
                docstring="Status information.",
                file_path="status.py",
                directory=".",
                signature="class Status()",
                line_number=1,
                fields=["code: int"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "**Documentation:**" in report
        assert "Status information." in report

    def test_dataclasses_grouped_by_directory(self):
        """Test that dataclasses are grouped by directory."""
        dataclasses = [
            DataclassInfo(
                name="Root",
                docstring="Root.",
                file_path="root.py",
                directory=".",
                signature="class Root()",
                line_number=1,
                fields=["x: int"],
                decorators=["@dataclass"],
            ),
            DataclassInfo(
                name="Sub",
                docstring="Sub.",
                file_path="subdir/sub.py",
                directory="subdir",
                signature="class Sub()",
                line_number=1,
                fields=["y: int"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        assert "## Directory: `(root)`" in report or "## Directory: `.`" in report
        assert "## Directory: `subdir`" in report
        assert "Root" in report
        assert "Sub" in report

    def test_dataclasses_sorted_within_directory(self):
        """Test that dataclasses are sorted alphabetically."""
        dataclasses = [
            DataclassInfo(
                name="Zebra",
                docstring="Z.",
                file_path="test.py",
                directory=".",
                signature="class Zebra()",
                line_number=1,
                fields=["x: int"],
                decorators=["@dataclass"],
            ),
            DataclassInfo(
                name="Alpha",
                docstring="A.",
                file_path="test.py",
                directory=".",
                signature="class Alpha()",
                line_number=5,
                fields=["y: int"],
                decorators=["@dataclass"],
            ),
        ]
        reporter = MarkdownReporter(brief_docstring=False)
        report = reporter.generate_report(
            [], add_description=False, dataclasses=dataclasses
        )

        # Find positions of dataclass names
        pos_alpha = report.find("Alpha")
        pos_zebra = report.find("Zebra")

        # alpha should come before zebra
        assert pos_alpha < pos_zebra
