"""Command-line interface for PyFuncScribe."""

import argparse
import sys
from pathlib import Path

from .extractor import FunctionExtractor
from .reporter import MarkdownReporter


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="pyfuncscribe",
        description="Generate comprehensive markdown reports of Python functions in a codebase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pyfuncscribe                          # Scan current directory, output to stdout
  pyfuncscribe -r /path/to/project      # Scan specific directory
  pyfuncscribe -o report.md             # Save report to file
  pyfuncscribe -r src -o docs/api.md    # Scan src directory, save to docs/api.md
  pyfuncscribe --brief                  # Include only docstring summaries
        """,
    )

    parser.add_argument(
        "-r",
        "--root",
        default=".",
        help="Root directory to start the search from (default: current directory)",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Output file path for the markdown report (default: stdout)",
    )

    parser.add_argument(
        "-b",
        "--brief",
        action="store_true",
        help="Include only the first line of docstrings (brief summary)",
    )

    parser.add_argument(
        "-c",
        "--include-commented",
        action="store_true",
        help="Include functions that are commented out (default: ignore commented code)",
    )

    parser.add_argument(
        "-d",
        "--add-description",
        action="store_true",
        help="Add an LLM-generated description to the report using Claude API (requires ANTHROPIC_API_KEY environment variable)",
    )

    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.0.1")

    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI tool."""
    args = parse_args()

    # Validate root directory
    root_path = Path(args.root)
    if not root_path.exists():
        print(f"Error: Directory '{args.root}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not root_path.is_dir():
        print(f"Error: '{args.root}' is not a directory", file=sys.stderr)
        sys.exit(1)

    # Extract functions
    try:
        extractor = FunctionExtractor(
            root_dir=args.root, include_commented=args.include_commented
        )
        functions = extractor.extract_all_functions()

        if not functions:
            print(f"Warning: No functions found in '{args.root}'", file=sys.stderr)

        # Generate report
        reporter = MarkdownReporter(brief_docstring=args.brief)
        report = reporter.generate_report(
            functions, add_description=args.add_description
        )

        # Output report
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Report generated successfully: {args.output}", file=sys.stderr)
        else:
            print(report)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
