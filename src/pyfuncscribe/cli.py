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

    parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        dest="recursive",
        help="Recursively search subdirectories for Python files (default: True)",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_false",
        dest="recursive",
        help="Do not recursively search subdirectories (only search the specified directory)",
    )

    parser.add_argument(
        "--include-empty",
        action="store_true",
        default=False,
        help="Create a report even if no functions are found (default: do not create report if empty)",
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
            root_dir=args.root,
            include_commented=args.include_commented,
            recursive=args.recursive,
        )
        functions = extractor.extract_all_functions()

        if not functions:
            if not args.include_empty:
                print(f"No functions found in '{args.root}'", file=sys.stderr)
                sys.exit(0)
            # If --include-empty is set, continue to generate report with empty list

        # Generate report
        reporter = MarkdownReporter(brief_docstring=args.brief)

        # Check if output file exists and if we should skip LLM description generation
        should_add_description = args.add_description
        output_path = Path(args.output) if args.output else None
        should_write_file = True

        if output_path and output_path.exists() and should_add_description:
            # File exists and user wants description - check if content has changed
            existing_content = output_path.read_text(encoding="utf-8")

            # Generate report without description to check if anything changed
            report_without_description = reporter.generate_report(
                functions, add_description=False, include_description=False
            )

            # Check if content has changed
            if not reporter._has_content_changed(
                existing_content, report_without_description
            ):
                print(
                    "Info: No changes detected in codebase. Skipping update.",
                    file=sys.stderr,
                )
                should_add_description = False
                should_write_file = False

        # Only generate and write report if there are changes or it's a new file
        if should_write_file:
            # Generate final report with or without description based on detection
            report = reporter.generate_report(
                functions, add_description=should_add_description
            )

            # Output report
            if output_path:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(report)
                print(f"Report generated successfully: {args.output}", file=sys.stderr)
            else:
                print(report)
        else:
            # No changes detected and output file exists - don't write anything
            if output_path:
                print(f"Report already up-to-date: {args.output}", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
