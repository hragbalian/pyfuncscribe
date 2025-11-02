"""Tests for the CLI module."""

from unittest.mock import patch

import pytest

from pyfuncscribe.cli import main, parse_args
from pyfuncscribe.extractor import FunctionExtractor
from pyfuncscribe.reporter import MarkdownReporter


class TestParseArgs:
    """Test argument parsing."""

    def test_parse_default_args(self):
        """Test parsing with default arguments."""
        with patch("sys.argv", ["pyfuncscribe"]):
            args = parse_args()
            assert args.root == "."
            assert args.output is None
            assert args.brief is False
            assert args.include_commented is False
            assert args.add_description is False

    def test_parse_root_directory(self):
        """Test parsing with custom root directory."""
        with patch("sys.argv", ["pyfuncscribe", "-r", "/tmp/test"]):
            args = parse_args()
            assert args.root == "/tmp/test"

    def test_parse_output_file(self):
        """Test parsing with output file."""
        with patch("sys.argv", ["pyfuncscribe", "-o", "report.md"]):
            args = parse_args()
            assert args.output == "report.md"

    def test_parse_brief_flag(self):
        """Test parsing brief flag."""
        with patch("sys.argv", ["pyfuncscribe", "--brief"]):
            args = parse_args()
            assert args.brief is True

    def test_parse_add_description_flag(self):
        """Test parsing add-description flag."""
        with patch("sys.argv", ["pyfuncscribe", "-d"]):
            args = parse_args()
            assert args.add_description is True

    def test_parse_include_commented_flag(self):
        """Test parsing include-commented flag."""
        with patch("sys.argv", ["pyfuncscribe", "-c"]):
            args = parse_args()
            assert args.include_commented is True

    def test_parse_recursive_flag_default(self):
        """Test that recursive flag defaults to True."""
        with patch("sys.argv", ["pyfuncscribe"]):
            args = parse_args()
            assert args.recursive is True

    def test_parse_no_recursive_flag(self):
        """Test parsing --no-recursive flag to disable recursive search."""
        with patch("sys.argv", ["pyfuncscribe", "--no-recursive"]):
            args = parse_args()
            assert args.recursive is False

    def test_parse_include_empty_flag_default(self):
        """Test that include-empty flag defaults to False."""
        with patch("sys.argv", ["pyfuncscribe"]):
            args = parse_args()
            assert args.include_empty is False

    def test_parse_include_empty_flag(self):
        """Test parsing --include-empty flag."""
        with patch("sys.argv", ["pyfuncscribe", "--include-empty"]):
            args = parse_args()
            assert args.include_empty is True


class TestMainFunctionality:
    """Test main CLI functionality."""

    def test_main_with_invalid_directory(self, capsys):
        """Test main with non-existent directory."""
        with patch("sys.argv", ["pyfuncscribe", "-r", "/nonexistent/path"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "does not exist" in captured.err

    def test_main_with_file_as_root(self, temp_file, capsys):
        """Test main when root is a file instead of directory."""
        temp_file.write_text("test content")
        with patch("sys.argv", ["pyfuncscribe", "-r", str(temp_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "is not a directory" in captured.err


class TestReportGeneration:
    """Test report generation through CLI."""

    def test_main_output_to_stdout(self, capsys):
        """Test main outputting to stdout."""
        with patch("sys.argv", ["pyfuncscribe", "-r", "src/pyfuncscribe"]):
            main()
        captured = capsys.readouterr()
        assert "# Python Functions Report" in captured.out
        assert "Total functions found:" in captured.out

    def test_main_output_to_file(self, temp_file):
        """Test main outputting to a file."""
        with patch(
            "sys.argv", ["pyfuncscribe", "-r", "src/pyfuncscribe", "-o", str(temp_file)]
        ):
            main()
        assert temp_file.exists()
        content = temp_file.read_text()
        assert "# Python Functions Report" in content
        assert "Total functions found:" in content

    def test_main_creates_parent_directories(self, temp_dir):
        """Test that main creates parent directories for output."""
        output_file = temp_dir / "subdir" / "nested" / "report.md"
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", "src/pyfuncscribe", "-o", str(output_file)],
        ):
            main()
        assert output_file.exists()


class TestFilePreservation:
    """Test file preservation when no changes detected."""

    def test_file_preserved_when_no_changes(self, temp_file, temp_dir):
        """Test that existing file is NOT overwritten when no changes detected."""
        # Create initial report with fake description
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        reporter = MarkdownReporter(brief_docstring=True)

        base_report = reporter.generate_report(
            functions, add_description=False, include_description=False
        )
        fake_description = """## Description

This is a valuable LLM-generated description.

---

"""
        lines = base_report.split("\n")
        report_with_desc = (
            "\n".join(lines[:2]) + "\n\n" + fake_description + "\n".join(lines[2:])
        )
        temp_file.write_text(report_with_desc)

        original_mtime = temp_file.stat().st_mtime
        original_size = temp_file.stat().st_size
        original_content = temp_file.read_text()

        import time

        time.sleep(0.1)

        # Run CLI with --add-description flag (should NOT overwrite)
        with patch(
            "sys.argv",
            [
                "pyfuncscribe",
                "-r",
                "src/pyfuncscribe",
                "-o",
                str(temp_file),
                "--brief",
                "--add-description",
            ],
        ):
            main()

        new_mtime = temp_file.stat().st_mtime
        new_size = temp_file.stat().st_size
        new_content = temp_file.read_text()

        # File should NOT be modified
        assert new_mtime == original_mtime, (
            "File was modified when it shouldn't have been"
        )
        assert new_size == original_size, "File size changed"
        assert new_content == original_content, "File content changed"
        assert "LLM-generated description" in new_content, "Description was lost"

    def test_file_overwritten_without_add_description_flag(self, temp_file):
        """Test that file IS overwritten without --add-description flag."""
        # Create initial report
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        reporter = MarkdownReporter(brief_docstring=True)

        base_report = reporter.generate_report(functions, add_description=False)
        temp_file.write_text(
            base_report + "\n\nSome extra content that shouldn't be here"
        )

        original_content = temp_file.read_text()
        original_size = temp_file.stat().st_size

        import time

        time.sleep(0.1)

        # Run CLI WITHOUT --add-description flag (should overwrite)
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", "src/pyfuncscribe", "-o", str(temp_file), "--brief"],
        ):
            main()

        new_content = temp_file.read_text()
        new_size = temp_file.stat().st_size

        # File should be overwritten
        assert new_size < original_size, "File size didn't decrease"
        assert "Some extra content" not in new_content, "Extra content still present"


class TestChangeDetection:
    """Test change detection logic."""

    def test_changes_detected_when_functions_added(self, temp_file, temp_dir):
        """Test that changes are detected when functions are added."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        reporter = MarkdownReporter(brief_docstring=True)

        # Create report with fewer functions (simulating old state)
        old_functions = functions[:10]
        old_report = reporter.generate_report(old_functions, add_description=False)
        fake_description = """## Description

Old description.

---

"""
        lines = old_report.split("\n")
        report_with_desc = (
            "\n".join(lines[:2]) + "\n\n" + fake_description + "\n".join(lines[2:])
        )
        temp_file.write_text(report_with_desc)

        # Generate new report with all functions
        new_report = reporter.generate_report(
            functions, add_description=False, include_description=False
        )

        # Check if changes are detected
        has_changed = reporter._has_content_changed(report_with_desc, new_report)
        assert has_changed is True, (
            "Changes should be detected when functions are added"
        )

    def test_no_changes_detected_for_identical_code(self, temp_file):
        """Test that no changes are detected for identical code."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        reporter = MarkdownReporter(brief_docstring=True)

        # Generate two identical reports
        report1 = reporter.generate_report(functions, add_description=False)
        report2 = reporter.generate_report(functions, add_description=False)

        has_changed = reporter._has_content_changed(report1, report2)
        assert has_changed is False, "No changes should be detected for identical code"


class TestRecursiveFlag:
    """Test recursive flag functionality in CLI."""

    def test_main_with_no_recursive_flag(self, temp_dir, capsys):
        """Test main with --no-recursive flag to only search root directory."""
        # Create a nested directory structure with Python files
        nested_dir = temp_dir / "nested"
        nested_dir.mkdir()

        root_file = temp_dir / "root_function.py"
        root_file.write_text("""
def root_func():
    '''A function in root directory.'''
    pass
""")

        nested_file = nested_dir / "nested_function.py"
        nested_file.write_text("""
def nested_func():
    '''A function in nested directory.'''
    pass
""")

        # Run with --no-recursive flag
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir), "--no-recursive"],
        ):
            main()

        captured = capsys.readouterr()
        # Should only find the root function
        assert "root_func" in captured.out
        assert "nested_func" not in captured.out

    def test_main_with_recursive_flag_default(self, temp_dir, capsys):
        """Test main with recursive search enabled by default."""
        # Create a nested directory structure
        nested_dir = temp_dir / "nested"
        nested_dir.mkdir()

        root_file = temp_dir / "root_function.py"
        root_file.write_text("""
def root_func():
    '''A function in root directory.'''
    pass
""")

        nested_file = nested_dir / "nested_function.py"
        nested_file.write_text("""
def nested_func():
    '''A function in nested directory.'''
    pass
""")

        # Run without --no-recursive flag (default is recursive)
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir)],
        ):
            main()

        captured = capsys.readouterr()
        # Should find both functions
        assert "root_func" in captured.out
        assert "nested_func" in captured.out


class TestIncludeEmptyFlag:
    """Test --include-empty flag behavior."""

    def test_main_with_empty_directory_without_flag(self, temp_dir, capsys):
        """Test that no report is created when directory is empty and --include-empty is not set."""
        # temp_dir is empty
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir)],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No functions found" in captured.err
        # Should not have generated a report
        assert "# Python Functions Report" not in captured.out

    def test_main_with_empty_directory_with_flag(self, temp_dir, capsys):
        """Test that report is created when directory is empty and --include-empty is set."""
        # temp_dir is empty
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir), "--include-empty"],
        ):
            main()
        captured = capsys.readouterr()
        # Should generate report even though no functions found
        assert "# Python Functions Report" in captured.out
        assert "Total functions found: **0**" in captured.out

    def test_main_with_empty_directory_without_flag_output_file(self, temp_dir, capsys):
        """Test that no file is created when directory is empty and --include-empty is not set."""
        output_file = temp_dir / "report.md"
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir), "-o", str(output_file)],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No functions found" in captured.err
        # File should not be created
        assert not output_file.exists()

    def test_main_with_empty_directory_with_flag_output_file(self, temp_dir, capsys):
        """Test that file is created when directory is empty and --include-empty is set."""
        output_file = temp_dir / "report.md"
        search_dir = temp_dir / "search"
        search_dir.mkdir()

        with patch(
            "sys.argv",
            [
                "pyfuncscribe",
                "-r",
                str(search_dir),
                "-o",
                str(output_file),
                "--include-empty",
            ],
        ):
            main()
        captured = capsys.readouterr()
        # File should be created
        assert output_file.exists()
        content = output_file.read_text()
        assert "# Python Functions Report" in content
        assert "Total functions found: **0**" in content
        assert "Report generated successfully" in captured.err

    def test_main_with_no_python_files_without_flag(self, temp_dir, capsys):
        """Test that no report is created when no Python files found and --include-empty is not set."""
        # Create non-Python files
        (temp_dir / "file.txt").write_text("Hello")
        (temp_dir / "script.sh").write_text("#!/bin/bash\necho hello")

        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir)],
        ):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "No functions found" in captured.err
        assert "# Python Functions Report" not in captured.out

    def test_main_with_no_python_files_with_flag(self, temp_dir, capsys):
        """Test that report is created when no Python files found but --include-empty is set."""
        # Create non-Python files
        (temp_dir / "file.txt").write_text("Hello")
        (temp_dir / "script.sh").write_text("#!/bin/bash\necho hello")

        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", str(temp_dir), "--include-empty"],
        ):
            main()
        captured = capsys.readouterr()
        assert "# Python Functions Report" in captured.out
        assert "Total functions found: **0**" in captured.out


class TestCLIMessages:
    """Test CLI output messages."""

    def test_success_message_when_file_updated(self, temp_file, capsys):
        """Test success message when file is updated."""
        with patch(
            "sys.argv",
            ["pyfuncscribe", "-r", "src/pyfuncscribe", "-o", str(temp_file), "--brief"],
        ):
            main()
        captured = capsys.readouterr()
        assert "Report generated successfully" in captured.err

    def test_up_to_date_message_when_no_changes(self, temp_file, capsys):
        """Test up-to-date message when no changes detected."""
        # Create initial report
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        reporter = MarkdownReporter(brief_docstring=True)

        base_report = reporter.generate_report(functions, add_description=False)
        fake_description = """## Description

Test description.

---

"""
        lines = base_report.split("\n")
        report_with_desc = (
            "\n".join(lines[:2]) + "\n\n" + fake_description + "\n".join(lines[2:])
        )
        temp_file.write_text(report_with_desc)

        # Run with --add-description flag
        with patch(
            "sys.argv",
            [
                "pyfuncscribe",
                "-r",
                "src/pyfuncscribe",
                "-o",
                str(temp_file),
                "--brief",
                "--add-description",
            ],
        ):
            main()

        captured = capsys.readouterr()
        assert "No changes detected" in captured.err
        assert "already up-to-date" in captured.err
