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
        "--hint",
        "-n",
        action="store_true",
        help="Get next solved cell only",
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
    if not s.is_valid():
        err = 'Invalid Puzzle ("no solution")'
        if args.json:
            print(json.dumps({"status": err, "board": s.board.astype(int).tolist()}, indent=2, ensure_ascii=False))
        else:
            print(err, file=sys.stderr)
        sys.exit(1)

    if args.hint:
        move = s.get_next_move()

        if move is not None:
            s.set_square_value(move[0], move[1], move[2])
            message = f"place {move[2]} in row {move[0]} column {move[1]}"
        else:
            message = "No more moves"

        if args.json:
            payload = {
                "status": "Complete" if s.is_complete() else "In progress",
                "move": {"row": move[0], "column": move[1], "value": move[2]} if move is not None else None,
                "message": message,
                "board": s.board.astype(int).tolist(),
            }
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(message)

        sys.exit(0)
    
    status = s.solve()

    if args.json:
        print(json.dumps({"status": status, "board": s.board.astype(int).tolist()}, indent=2, ensure_ascii=False))
    else:
        s.display()


if __name__ == "__main__":
    main()
