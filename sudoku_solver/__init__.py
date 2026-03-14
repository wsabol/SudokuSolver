"""
Sudoku solver package.

Board formats supported:
- String of 81 chars (blanks: '0', '.', or any non-1-9)
- List of 9 lists of 9 ints (0 for blank)
- 2D numpy array
"""

from __future__ import annotations

from typing import Any, Dict, List, Union

from sudoku_solver.sudoku import Sudoku

__all__ = ["Sudoku", "solve"]


def solve(board: Union[str, List[List[int]], Any]) -> Dict[str, Any]:
    """
    Main library API: solve a Sudoku puzzle and return structured data.

    Does not print; use Sudoku.solve() for interactive output.

    Args:
        board: 81-char string, list of 9 lists, or 2D array. Blanks as 0, '.', etc.

    Returns:
        Dict with keys:
            - board: 9x9 list of ints (solved puzzle)
            - status: "Unique Solution" | "Invalid Puzzle (...)"
    """
    s = Sudoku(board)
    status = s._solve()
    return {
        "board": s.board.astype(int).tolist(),
        "status": status,
    }
