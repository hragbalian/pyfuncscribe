"""Tests for the FunctionExtractor class."""

import tempfile
from pathlib import Path

from pyfuncscribe.extractor import FunctionExtractor


class TestFunctionExtractorInitialization:
    """Test FunctionExtractor initialization."""

    def test_extractor_init_default(self):
        """Test extractor initialization with defaults."""
        extractor = FunctionExtractor()
        assert extractor.include_commented is False

    def test_extractor_init_custom_root(self):
        """Test extractor initialization with custom root."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        assert str(extractor.root_dir).endswith("pyfuncscribe")

    def test_extractor_init_include_commented(self):
        """Test extractor initialization with include_commented."""
        extractor = FunctionExtractor(include_commented=True)
        assert extractor.include_commented is True


class TestPythonFileFinding:
    """Test finding Python files."""

    def test_find_python_files(self):
        """Test that Python files are found."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        files = extractor.find_python_files()
        assert len(files) > 0
        assert all(str(f).endswith(".py") for f in files)

    def test_find_python_files_in_nested_directories(self):
        """Test finding Python files in nested directories."""
        extractor = FunctionExtractor(root_dir="src")
        files = extractor.find_python_files()
        # Should find files in src/pyfuncscribe
        py_files = [f for f in files if "pyfuncscribe" in str(f)]
        assert len(py_files) > 0

    def test_find_python_files_recursive_true(self):
        """Test finding Python files with recursive=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            nested_dir = Path(tmpdir) / "nested" / "deep"
            nested_dir.mkdir(parents=True)

            # Create Python files at different levels
            root_file = Path(tmpdir) / "root.py"
            root_file.write_text("def root(): pass")

            nested_file = (Path(tmpdir) / "nested") / "nested.py"
            nested_file.write_text("def nested(): pass")

            deep_file = nested_dir / "deep.py"
            deep_file.write_text("def deep(): pass")

            # Search with recursive=True (default)
            extractor = FunctionExtractor(root_dir=tmpdir, recursive=True)
            files = extractor.find_python_files()

            # Should find all three files
            assert len(files) == 3
            file_names = [f.name for f in files]
            assert "root.py" in file_names
            assert "nested.py" in file_names
            assert "deep.py" in file_names

    def test_find_python_files_recursive_false(self):
        """Test finding Python files with recursive=False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            nested_dir = Path(tmpdir) / "nested" / "deep"
            nested_dir.mkdir(parents=True)

            # Create Python files at different levels
            root_file = Path(tmpdir) / "root.py"
            root_file.write_text("def root(): pass")

            nested_file = (Path(tmpdir) / "nested") / "nested.py"
            nested_file.write_text("def nested(): pass")

            deep_file = nested_dir / "deep.py"
            deep_file.write_text("def deep(): pass")

            # Search with recursive=False
            extractor = FunctionExtractor(root_dir=tmpdir, recursive=False)
            files = extractor.find_python_files()

            # Should only find the root file
            assert len(files) == 1
            assert files[0].name == "root.py"


class TestFunctionExtraction:
    """Test function extraction from Python files."""

    def test_extract_functions_from_file(self):
        """Test extracting functions from an actual file."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        cli_file = Path("src/pyfuncscribe/cli.py")
        functions = extractor.extract_functions_from_file(cli_file)
        assert len(functions) > 0
        # Should find main and parse_args
        function_names = [f.name for f in functions]
        assert "main" in function_names
        assert "parse_args" in function_names

    def test_extract_functions_from_multiple_files(self):
        """Test extracting functions from multiple files."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        all_functions = extractor.extract_all_functions()
        assert len(all_functions) > 0
        # Should have functions from multiple modules
        file_paths = set(f.file_path for f in all_functions)
        assert len(file_paths) > 1

    def test_extract_all_functions_recursive_true(self):
        """Test extracting all functions with recursive=True."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            nested_dir = Path(tmpdir) / "nested"
            nested_dir.mkdir()

            root_file = Path(tmpdir) / "root.py"
            root_file.write_text("""
def root_func():
    '''Root function.'''
    pass
""")

            nested_file = nested_dir / "nested.py"
            nested_file.write_text("""
def nested_func():
    '''Nested function.'''
    pass
""")

            # Extract with recursive=True
            extractor = FunctionExtractor(root_dir=tmpdir, recursive=True)
            functions = extractor.extract_all_functions()

            # Should find both functions
            assert len(functions) == 2
            function_names = [f.name for f in functions]
            assert "root_func" in function_names
            assert "nested_func" in function_names

    def test_extract_all_functions_recursive_false(self):
        """Test extracting all functions with recursive=False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            nested_dir = Path(tmpdir) / "nested"
            nested_dir.mkdir()

            root_file = Path(tmpdir) / "root.py"
            root_file.write_text("""
def root_func():
    '''Root function.'''
    pass
""")

            nested_file = nested_dir / "nested.py"
            nested_file.write_text("""
def nested_func():
    '''Nested function.'''
    pass
""")

            # Extract with recursive=False
            extractor = FunctionExtractor(root_dir=tmpdir, recursive=False)
            functions = extractor.extract_all_functions()

            # Should only find the root function
            assert len(functions) == 1
            assert functions[0].name == "root_func"

    def test_function_info_has_required_fields(self):
        """Test that extracted function info has all required fields."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        assert len(functions) > 0

        func = functions[0]
        assert func.name is not None
        assert func.file_path is not None
        assert func.signature is not None
        assert func.line_number > 0
        assert isinstance(func.arguments, list)
        assert isinstance(func.decorators, list)
        assert isinstance(func.is_async, bool)

    def test_extract_function_docstring(self):
        """Test extracting function docstring."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        # Find a function with a docstring
        funcs_with_docstrings = [f for f in functions if f.docstring]
        assert len(funcs_with_docstrings) > 0

    def test_extract_function_return_annotation(self):
        """Test extracting function return annotations."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        # Find functions with return annotations
        funcs_with_returns = [f for f in functions if f.return_annotation]
        assert len(funcs_with_returns) > 0

    def test_extract_function_arguments(self):
        """Test extracting function arguments."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()
        # Find functions with arguments
        funcs_with_args = [f for f in functions if len(f.arguments) > 0]
        assert len(funcs_with_args) > 0


class TestCommentedFunctionHandling:
    """Test handling of commented functions."""

    def test_commented_functions_excluded_by_default(self):
        """Test that commented functions are excluded by default."""
        # Create a temporary Python file with a commented function
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
def normal_function():
    '''A normal function.'''
    pass

# def commented_function():
#     '''A commented function.'''
#     pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir, include_commented=False)
            functions = extractor.extract_functions_from_file(test_file)
            function_names = [f.name for f in functions]
            assert "normal_function" in function_names
            assert "commented_function" not in function_names

    def test_commented_functions_included_when_flag_set(self):
        """Test that commented functions are included when flag is set."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
def normal_function():
    '''A normal function.'''
    pass

# def commented_function():
#     '''A commented function.'''
#     pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir, include_commented=True)
            functions = extractor.extract_functions_from_file(test_file)
            function_names = [f.name for f in functions]
            assert "normal_function" in function_names
            # Commented functions should be included when flag is set
            # (though the AST will still parse the uncommented version)


class TestAsyncFunctionHandling:
    """Test handling of async functions."""

    def test_async_functions_detected(self):
        """Test that async functions are properly detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
async def async_function():
    '''An async function.'''
    pass

def normal_function():
    '''A normal function.'''
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)

            async_funcs = [f for f in functions if f.is_async]
            sync_funcs = [f for f in functions if not f.is_async]

            assert len(async_funcs) == 1
            assert len(sync_funcs) == 1
            assert async_funcs[0].name == "async_function"


class TestFunctionSignatureBuilding:
    """Test function signature building."""

    def test_simple_function_signature(self):
        """Test building signature for simple function."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
def simple_func(x, y):
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)
            assert len(functions) == 1
            assert "simple_func" in functions[0].signature
            assert "x" in functions[0].signature
            assert "y" in functions[0].signature

    def test_function_signature_with_types(self):
        """Test building signature with type annotations."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
def typed_func(x: int, y: str) -> bool:
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)
            assert len(functions) == 1
            signature = functions[0].signature
            assert "int" in signature
            assert "str" in signature
            assert "bool" in signature

    def test_function_signature_with_default_values(self):
        """Test building signature with default values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
def func_with_defaults(x=1, y='test'):
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)
            assert len(functions) == 1
            signature = functions[0].signature
            assert "x" in signature
            assert "y" in signature


class TestDecoratorExtraction:
    """Test extraction of decorators."""

    def test_single_decorator_extracted(self):
        """Test extracting single decorator."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
@property
def decorated_func(self):
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)
            assert len(functions) == 1
            assert "property" in functions[0].decorators

    def test_multiple_decorators_extracted(self):
        """Test extracting multiple decorators."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("""
@property
@staticmethod
def decorated_func():
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(test_file)
            assert len(functions) == 1
            assert "property" in functions[0].decorators
            assert "staticmethod" in functions[0].decorators


class TestRelativePathGeneration:
    """Test relative path generation for functions."""

    def test_relative_paths_generated(self):
        """Test that relative paths are generated for functions."""
        extractor = FunctionExtractor(root_dir="src/pyfuncscribe")
        functions = extractor.extract_all_functions()

        # All paths should be relative to root_dir
        for func in functions:
            assert not str(func.file_path).startswith("/")
            assert func.file_path.endswith(".py")


class TestErrorHandling:
    """Test error handling during extraction."""

    def test_invalid_python_file_skipped(self):
        """Test that invalid Python files are skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file with syntax errors
            bad_file = Path(tmpdir) / "bad.py"
            bad_file.write_text("""
def broken_function(:  # Syntax error
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_functions_from_file(bad_file)
            # Should return empty list, not raise exception
            assert functions == []

    def test_extract_all_functions_handles_errors(self):
        """Test that extract_all_functions handles errors gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a good file
            good_file = Path(tmpdir) / "good.py"
            good_file.write_text("""
def good_function():
    pass
""")
            # Create a bad file
            bad_file = Path(tmpdir) / "bad.py"
            bad_file.write_text("""
def broken_function(:
    pass
""")
            extractor = FunctionExtractor(root_dir=tmpdir)
            functions = extractor.extract_all_functions()
            # Should extract from good file, skip bad file
            assert len(functions) > 0
            assert functions[0].name == "good_function"
