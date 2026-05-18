import argparse
from .pipeline import run_pipeline


def main() -> None:

    """Entry point for the function calling pipeline."""

    parser = argparse.ArgumentParser(
        description="Translate natural language prompts into function calls."
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json"
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json"
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json"
    )
    args = parser.parse_args()

    run_pipeline(
        args.functions_definition,
        args.input,
        args.output
    )



if __name__ == "__main__":
    main()
