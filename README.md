# Sudoku Solver

[![CI](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/ci.yml)

A command-line Sudoku solver with support for string, list, and numpy board formats. Test cases and error handling from [Sudopedia](http://sudopedia.enjoysudoku.com/Test_Cases.html).

## Install

```bash
pip install -e .
# or
pip install -r requirements.txt
```

## CLI Usage

```bash
# Solve a single board (81-char string)
sudoku-solve "000010080302607000070000003080070500004000600003050010200000050000705108060040000"
```

### Board formats

- **81-char string**: `"00001008..."` or `"...6.2...."` (blanks as `0` or `.`)
- **2D list**: `[[5,8,6,0,...], ...]`

### Python usage

```python
from sudoku_solver import Sudoku

s = Sudoku("000010080302607000070000003080070500004000600003050010200000050000705108060040000")
s.solve()
s.display()
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
