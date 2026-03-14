import json
from pathlib import Path

from sudoku_solver import solve, Sudoku


def test_solve_api_returns_dict():
    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    result = solve(board)
    assert "board" in result
    assert "status" in result
    assert isinstance(result["board"], list)
    assert len(result["board"]) == 9
    assert result["status"] == "Unique Solution"


def test_solve_api_unique_solution():
    board = "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
    result = solve(board)
    flat = [c for row in result["board"] for c in row]
    assert 0 not in flat
    assert sorted(set(flat)) == list(range(1, 10))


def test_test_cases_match_expected():
    cases_path = Path(__file__).resolve().parent / "test_cases.json"
    if not cases_path.exists():
        return
    with open(cases_path) as f:
        puzzles = json.load(f)
    for p in puzzles[:5]:
        result = solve(p["board"])
        assert result["status"] == p["result"]


def test_solve_silent_no_print():
    s = Sudoku("000010080302607000070000003080070500004000600003050010200000050000705108060040000")
    status = s.solve(verbose=False)
    assert status == "Unique Solution"
