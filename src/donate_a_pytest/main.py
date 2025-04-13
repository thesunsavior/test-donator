import os
import argparse
import logging
import sys
import pytest
from pathlib import Path

logger = logging.getLogger(__name__)


def run_donated_tests(
    directory: str = None,
    verbose: bool = False,
    output_format: str = "summary",
    failfast: bool = False,
) -> dict:
    """
    Run all tests marked with @pytest.mark.donate

    Args:
        directory: Directory to search for tests (default: current directory)
        verbose: Whether to show verbose output
        output_format: Format for results output ("summary", "detailed")
        failfast: Whether to stop at first failure

    Returns:
        dict: Test results summary
    """
    logger.info("Running tests with @pytest.mark.donate marker")

    # Prepare pytest arguments
    pytest_args = ["-v"] if verbose else []

    # Add directory if specified
    if directory:
        directory_path = Path(directory)
        if not directory_path.exists():
            logger.error(f"Directory {directory} does not exist")
            return {"success": False, "error": f"Directory {directory} does not exist"}
        pytest_args.append(str(directory_path))
    else:
        pytest_args.append(os.getcwd())

    # Add marker filter
    pytest_args.extend(["-m", "donate"])

    # Add fail fast if requested
    if failfast:
        pytest_args.append("--exitfirst")

    # Run pytest
    logger.info(f"Running pytest with arguments: {pytest_args}")
    result = pytest.main(pytest_args)

    # Process results
    success = result == pytest.ExitCode.OK

    result_summary = {
        "success": success,
        "exit_code": result,
        "exit_code_name": result.name if hasattr(result, "name") else str(result),
    }

    if output_format == "detailed":
        # In a real implementation, you might capture and process the test output
        # This would require more complex pytest configuration
        pass

    return result_summary


def setup_logging(verbose: bool = False):
    """
    Set up logging configuration

    Args:
        verbose: Whether to use verbose logging
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )


def main():
    """CLI entry point for donate-a-pytest"""
    parser = argparse.ArgumentParser(
        description="Run tests with @pytest.mark.donate marker"
    )

    parser.add_argument(
        "-d",
        "--directory",
        help="Directory to search for tests (default: current directory)",
        default=None,
    )

    parser.add_argument(
        "-v", "--verbose", help="Show verbose output", action="store_true"
    )

    parser.add_argument(
        "-o",
        "--output-format",
        help="Format for results output",
        choices=["summary", "detailed"],
        default="summary",
    )

    parser.add_argument(
        "-f", "--failfast", help="Stop at first failure", action="store_true"
    )

    args = parser.parse_args()

    # Set up logging
    setup_logging(args.verbose)

    try:
        # Run tests
        result = run_donated_tests(
            directory=args.directory,
            verbose=args.verbose,
            output_format=args.output_format,
            failfast=args.failfast,
        )

        # Output results
        if args.output_format == "summary":
            print(f"Test run {'succeeded' if result['success'] else 'failed'}")
            print(f"Exit code: {result['exit_code']} ({result['exit_code_name']})")

        # Set exit code based on test results
        sys.exit(0 if result["success"] else 1)

    except Exception as e:
        logger.error(f"Error running tests: {e}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()
