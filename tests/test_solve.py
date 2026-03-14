from __future__ import annotations

import json
import sys
from io import StringIO
from pathlib import Path

import pytest

from sudoku_solver import solve, Sudoku


# --- solve() API tests ---


def test_solve_api_returns_dict() -> None:
    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    result = solve(board)
    assert "board" in result
    assert "status" in result
    assert isinstance(result["board"], list)
    assert len(result["board"]) == 9
    assert result["status"] == "Unique Solution"


def test_solve_api_unique_solution() -> None:
    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    result = solve(board)
    flat = [c for row in result["board"] for c in row]
    assert 0 not in flat
    assert sorted(set(flat)) == list(range(1, 10))


def test_solve_accepts_list_input() -> None:
    board = [
        [5, 8, 6, 0, 7, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 1, 6, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 0, 0, 0, 0, 0],
        [9, 0, 2, 0, 1, 0, 3, 0, 5],
        [0, 0, 5, 0, 9, 0, 0, 0, 0],
        [0, 9, 0, 0, 4, 0, 0, 0, 8],
        [0, 0, 3, 5, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 2, 0, 4, 7, 0],
    ]
    result = solve(board)
    assert result["status"] == "Unique Solution"
    flat = [c for row in result["board"] for c in row]
    assert 0 not in flat


def test_solve_accepts_dots_string() -> None:
    board = "...6.2.....1.9.2..3..5.4..76.97.35.12.......6...........4...6...1.2.6.8..62...93."
    result = solve(board)
    assert result["status"] == "Unique Solution"


# --- test_cases.json: all cases ---


def _load_test_cases() -> list:
    path = Path(__file__).resolve().parent / "test_cases.json"
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


@pytest.mark.parametrize("case", _load_test_cases(), ids=lambda c: c["title"])
def test_all_cases_match_expected(case: dict) -> None:
    result = solve(case["board"])
    assert result["status"] == case["result"]


# --- Invalid status branches ---


def test_invalid_no_solution() -> None:
    board = "..9.7...5..21..9..1...28....7...5..1..851.....5....3.......3..68........21.....87"
    result = solve(board)
    assert result["status"] == 'Invalid Puzzle ("no solution")'


def test_invalid_not_enough_givens() -> None:
    board = "........................................1........................................"
    result = solve(board)
    assert "not enough givens" in result["status"] or "multiple solutions" in result["status"]


def test_invalid_no_unique_solution() -> None:
    board = ".39...12....9.7...8..4.1..6.42...79...........91...54.5..1.9..3...8.5....14...87."
    result = solve(board)
    assert result["status"] == 'Invalid Puzzle ("no unique solution")'


# --- Sudoku class / display ---


def test_display_output() -> None:
    s = Sudoku("000010080302607000070000003080070500004000600003050010200000050000705108060040000")
    s.solve()
    out = StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        s.display()
    finally:
        sys.stdout = old_stdout
    lines = out.getvalue().strip().split("\n")
    assert len(lines) >= 9
    assert "4" in lines[0]  # first row has digits


# --- CLI ---


def test_cli_board_length_error(capsys: pytest.CaptureFixture[str]) -> None:
    from sudoku_solver.cli import main

    sys.argv = ["sudoku-solve", "--board", "x" * 80]
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "81" in captured.err


def test_cli_solves_board(capsys: pytest.CaptureFixture[str]) -> None:
    from sudoku_solver.cli import main
    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    sys.argv = ["sudoku-solve", "--board", board]
    main()
    captured = capsys.readouterr()
    assert "4" in captured.out  # solved digits


def test_cli_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    from sudoku_solver.cli import main

    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    sys.argv = ["sudoku-solve", "--board", board, "--json"]
    main()
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "status" in data
    assert "board" in data
    assert data["status"] == "Unique Solution"
    assert len(data["board"]) == 9
    flat = [c for row in data["board"] for c in row]
    assert 0 not in flat
