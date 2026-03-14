import argparse
import sys
import json

from sudoku_solver import Sudoku


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Solve a Sudoku puzzle. Provide an 81-char board string."
    )
    parser.add_argument(
        "--board",
        "-b",
        required=True,
        help="81-char board string (0 or . for blanks)",
    )
    parser.add_argument(
        "--json",
        "-j",
        action="store_true",
        help="Output as json with status messages",
    )
    args = parser.parse_args()

    board = args.board.strip()
    if len(board) != 81:
        print(f"Error: board must be 81 characters, got {len(board)}", file=sys.stderr)
        sys.exit(1)

    s = Sudoku(board)
    status = s.solve()

    if args.json:
        print(json.dumps({"status": status, "board": s.board.astype(int).tolist()}, indent=2, ensure_ascii=False))
    else:
        s.display()


if __name__ == "__main__":
    main()
