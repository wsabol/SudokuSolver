import argparse
import json
import sys

from sudoku_solver import Sudoku


def main():
    parser = argparse.ArgumentParser(
        description="Solve Sudoku puzzles. Accepts JSON file with puzzles or raw board."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default=None,
        help="Path to JSON file with puzzles (array of {title, board, result}) or 81-char board string",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output the solved board, no status messages",
    )
    args = parser.parse_args()

    if args.input is None:
        parser.print_help()
        sys.exit(0)

    inp = args.input
    is_file = len(inp) != 81 or "/" in inp or "\\" in inp or inp.endswith(".json")

    if is_file:
        try:
            with open(inp) as f:
                puzzles = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        for p in puzzles:
            print(p["title"])
            print(p["result"])
            print("---")
            s = Sudoku(p["board"])
            s.solve(verbose=not args.quiet)
            s.display()
            print()
    else:
        s = Sudoku(inp)
        s.solve(verbose=not args.quiet)
        s.display()


if __name__ == "__main__":
    main()
