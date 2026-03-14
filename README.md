# Sudoku Solver

[![Tests](https://github.com/wsabol/sudoku_solver/actions/workflows/ci.yml/badge.svg)](https://github.com/wsabol/sudoku_solver/actions/workflows/ci.yml)

A command-line Sudoku solver with support for string, list, and numpy board formats. Test cases and error handling from [Sudopedia](http://sudopedia.enjoysudoku.com/Test_Cases.html).

## Install

```bash
pip install -e .
# or
pip install -r requirements.txt
```

## CLI Usage

```bash
# Solve a board (81-char string)
sudoku-solve --board 000010080302607000070000003080070500004000600003050010200000050000705108060040000
sudoku-solve -b 000010080302607000070000003080070500004000600003050010200000050000705108060040000

# Get next hint only (single move, does not solve the puzzle)
sudoku-solve --board 000010080302607000070000003080070500004000600003050010200000050000705108060040000 --hint
sudoku-solve -b 000010080... -n --json   # hint with JSON output
```

### Board formats

- **81-char string**: `00001008...` or `...6.2....` (blanks as `0` or `.`)
- **2D list**: `[[5,8,6,0,...], ...]`

### Python usage

```python
from sudoku_solver import Sudoku

# Solve a puzzle
s = Sudoku("000010080302607000070000003080070500004000600003050010200000050000705108060040000")
s.solve()
s.display()

# Get the next move (hint) without solving
s2 = Sudoku("000010080302607000070000003080070500004000600003050010200000050000705108060040000")
move = s2.get_next_move()  # (row, col, value) or None
if move:
    row, col, value = move
    s2.set_square_value(row, col, value)
```

## Tests

Unit tests use `tests/test_cases.json` (from Sudopedia).

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Project layout

```
sudoku_solver/
├── pyproject.toml
├── requirements.txt
├── README.md
├── .gitignore
├── solver.py          # demo script
├── sudoku_solver/     # package
│   ├── __init__.py
│   ├── sudoku.py      # solver logic
│   └── cli.py         # sudoku-solve entry point
└── tests/
    ├── test_cases.json    # unit test data
    └── test_solve.py
```

## License

MIT - see [LICENSE](LICENSE).
