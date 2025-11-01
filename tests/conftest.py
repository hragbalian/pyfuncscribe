"""Pytest configuration and shared fixtures for pyfuncscribe tests."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    import shutil

    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_file(temp_dir):
    """Create a temporary file path (file not created)."""
    return temp_dir / "test_report.md"


@pytest.fixture
def sample_functions():
    """Provide sample FunctionInfo objects for testing."""
    from pyfuncscribe.extractor import FunctionInfo

    return [
        FunctionInfo(
            name="test_function_1",
            docstring="This is a test function.",
            file_path="test_file.py",
            directory=".",
            signature="def test_function_1(x: int) -> str:",
            line_number=10,
            arguments=["self", "x: int"],
            return_annotation="str",
            decorators=[],
            is_async=False,
        ),
        FunctionInfo(
            name="test_function_2",
            docstring="Another test function.",
            file_path="test_file.py",
            directory=".",
            signature="async def test_function_2() -> None:",
            line_number=20,
            arguments=["self"],
            return_annotation="None",
            decorators=["property"],
            is_async=True,
        ),
    ]
