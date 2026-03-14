from __future__ import annotations

import math
from typing import Any, List, Union

import numpy as np
from numpy.typing import NDArray


class Sudoku:
    def __init__(self, board: Union[str, List[List[int]], NDArray[np.float64]]) -> None:
        """Initialize variables, assign input board to self.board"""
        self.list_possibles = [[np.array([]) for j in range(9)] for i in range(9)]
        self.complete = np.reshape(np.arange(1, 10), 9)
        self.board = np.zeros((9, 9))

        if isinstance(board, str):
            board = self.board_parse(board)

        self.num_givens = 0
        board = np.reshape(board, (9, 9))
        for i in range(9):
            for j in range(9):
                if board[i][j] in (1, 2, 3, 4, 5, 6, 7, 8, 9):
                    self.board[i][j] = board[i][j]
                    self.num_givens += 1

        self.calc_possibles()

    def board_parse(self, sboard: str) -> NDArray[np.float64]:
        """Parse string into 2d array"""
        board = np.zeros((9, 9))
        i = 0
        while i < 81 and i < len(sboard):
            irow = int(i / 9)
            icol = i % 9
            if sboard[i] in "123456789":
                board[irow, icol] = int(sboard[i])
            i += 1
        return board

    def display(self) -> None:
        """Display these values as a 2-D grid."""
        separator = "+ ".join(["- " * 3] * 3)
        for irow in range(9):
            line = ""
            for icol in range(9):
                line = (
                    line
                    + (
                        ". "
                        if self.board[irow, icol] == 0
                        else str(int(self.board[irow][icol])) + " "
                    )
                    + ("| " if icol in (2, 5) else "")
                )
            print(line)
            if irow in (2, 5):
                print(separator)
        print()

    def get_row(self, irow: int) -> NDArray[np.float64]:
        """Return 1d array for given row index"""
        return np.reshape(self.board[irow, :], 9)

    def get_column(self, icol: int) -> NDArray[np.float64]:
        """Return 1d array for given column index"""
        return np.reshape(self.board[:, icol], 9)

    def get_box(self, ibox: int) -> NDArray[np.float64]:
        """Return 1d array for given box index"""
        row = math.floor(float(ibox) / 3.0) * 3
        col = 3 * (ibox % 3)
        return np.reshape(self.board[row : row + 3, col : col + 3], 9)

    def box_index(self, irow: int, icol: int) -> int:
        """Return index[0,8] of the box for a given square"""
        sq_row = math.floor(float(irow) / 3.0)
        sq_col = math.floor(float(icol) / 3.0)
        return sq_row * 3 + sq_col

    def square_value(self, irow: int, icolumn: int) -> float:
        """Returns the value of a given square on the board"""
        return self.board[irow, icolumn]

    def values_missing(self, ar):
        """Returns the values missing from the given 1d array returned by get_row,get_column,get_box"""
        mask = np.isin(self.complete, ar, invert=True)
        return self.complete[mask]

    def possibles(self, irow: int, icol: int) -> NDArray[Any]:
        """Returns the list of possible values for given coordinates"""
        return self.list_possibles[irow][icol]

    def calc_possibles(self):
        """Recalculates all possible values, called after new value is set"""
        for i in range(9):
            for j in range(9):
                self.list_possibles[i][j] = self.calc_square_possibles(i, j)

    def calc_square_possibles(self, irow, icol):
        """Recalculates possible values for given coordinates"""
        if self.square_value(irow, icol) > 0:
            return np.array([])
        else:
            possible = self.values_missing(self.get_row(irow))
            col_possible = self.values_missing(self.get_column(icol))
            mask = np.isin(possible, col_possible)
            possible = possible[mask]
            ibox = self.box_index(irow, icol)
            box_possible = self.values_missing(self.get_box(ibox))
            mask = np.isin(possible, box_possible)
            possible = possible[mask]
            return possible

    def set_square_value(self, irow, icol, value):
        """Sets values at given coordinate, recalcuates possibles"""
        org = self.square_value(irow, icol)
        if value in self.possibles(irow, icol):
            self.board[irow][icol] = value
            if not self.is_valid():
                self.board[irow][icol] = org
            else:
                self.calc_possibles()

    def box_to_puzzle(self, ibox, i):
        """Given a box index and index from that 1d array, returns coordinates on the board"""
        irow = math.floor(float(ibox) / 3.0) * 3 + math.floor(float(i) / 3.0)
        icol = 3 * (ibox % 3) + (i % 3)
        return (irow, icol)

    def is_valid(self) -> bool:
        """Checks if board and possible values are valid."""
        for i in range(9):
            row = self.get_row(i)
            if row[row > 9].size > 0:
                return False
            row = row[row > 0]
            if row.size != np.unique(row).size:
                return False
        for i in range(9):
            col = self.get_column(i)
            if col[col > 9].size > 0:
                return False
            col = col[col > 0]
            if col.size != np.unique(col).size:
                return False
        for i in range(9):
            box = self.get_box(i)
            if box[box > 9].size > 0:
                return False
            box = box[box > 0]
            if box.size != np.unique(box).size:
                return False
        for i in range(9):
            for j in range(9):
                if self.square_value(i, j) == 0:
                    if self.possibles(i, j).size == 0:
                        return False
        for irow in range(9):
            row = self.get_row(irow)
            for n in range(1, 10):
                candidates = False
                i = 0
                while i < 9 and not candidates:
                    if row[i] == n:
                        candidates = True
                    elif n in self.possibles(irow, i):
                        candidates = True
                    i += 1
                if not candidates:
                    return False
        for icol in range(9):
            col = self.get_column(icol)
            for n in range(1, 10):
                candidates = False
                i = 0
                while i < 9 and not candidates:
                    if col[i] == n:
                        candidates = True
                    elif n in self.possibles(i, icol):
                        candidates = True
                    i += 1
                if not candidates:
                    return False
        for ibox in range(9):
            box = self.get_box(ibox)
            for n in range(1, 10):
                candidates = False
                i = 0
                while i < 9 and not candidates:
                    irow, icol = self.box_to_puzzle(ibox, i)
                    if box[i] == n:
                        candidates = True
                    elif n in self.possibles(irow, icol):
                        candidates = True
                    i += 1
                if not candidates:
                    return False
        return True

    def is_complete(self) -> bool:
        """Returns if we have valid board with no blanks"""
        return self.is_valid() and self.board[self.board == 0].size == 0

    def _find_naked_single(self) -> tuple[int, int, int] | None:
        """Returns (row, col, value) for first cell with exactly one possible value, or None."""
        for irow in range(9):
            for icol in range(9):
                if self.square_value(irow, icol) == 0:
                    p = self.possibles(irow, icol)
                    if p.size == 1:
                        return (irow, icol, int(p[0]))
        return None

    def _find_hidden_single_in_row(self, irow: int) -> tuple[int, int, int] | None:
        """Returns (row, col, value) for first hidden single in row, or None."""
        pos = np.zeros((9, 9))
        for icol in range(9):
            if self.square_value(irow, icol) == 0:
                for p in self.possibles(irow, icol):
                    pos[p - 1][icol] += 1
        for val in range(9):
            if pos[val].sum() == 1:
                index = int(np.where(pos[val] == 1)[0][0])
                return (irow, index, val + 1)
        return None

    def _find_hidden_single_in_col(self, icol: int) -> tuple[int, int, int] | None:
        """Returns (row, col, value) for first hidden single in column, or None."""
        pos = np.zeros((9, 9))
        for irow in range(9):
            if self.square_value(irow, icol) == 0:
                for p in self.possibles(irow, icol):
                    pos[p - 1][irow] += 1
        for val in range(9):
            if pos[val].sum() == 1:
                index = int(np.where(pos[val] == 1)[0][0])
                return (index, icol, val + 1)
        return None

    def _find_hidden_single_in_box(self, ibox: int) -> tuple[int, int, int] | None:
        """Returns (row, col, value) for first hidden single in box, or None."""
        pos = np.zeros((9, 9))
        for jbox in range(9):
            irow, icol = self.box_to_puzzle(ibox, jbox)
            if self.square_value(irow, icol) == 0:
                for p in self.possibles(irow, icol):
                    pos[p - 1][jbox] += 1
        for val in range(9):
            if pos[val].sum() == 1:
                index = int(np.where(pos[val] == 1)[0][0])
                irow, icol = self.box_to_puzzle(ibox, index)
                return (irow, icol, val + 1)
        return None

    def get_next_move(self) -> tuple[int, int, int] | None:
        """Return the next logical move (row, col, value), or None if complete or stuck.

        Uses naked singles and hidden singles. Does not mutate the board.
        """
        if self.is_complete() or not self.is_valid():
            return None

        move = self._find_naked_single()
        if move is not None:
            return move

        for irow in range(9):
            move = self._find_hidden_single_in_row(irow)
            if move is not None:
                return move
        for icol in range(9):
            move = self._find_hidden_single_in_col(icol)
            if move is not None:
                return move
        for ibox in range(9):
            move = self._find_hidden_single_in_box(ibox)
            if move is not None:
                return move

        return None

    def simple_solve(self) -> None:
        """Naked Singles Algorithm - find squares with only one possible value"""
        while (move := self._find_naked_single()) is not None:
            self.set_square_value(move[0], move[1], move[2])

    def uni_possibles_solve(self) -> None:
        """Hidden Singles Algorithm - find unique candidates per row/column/box"""
        for irow in range(9):
            while (move := self._find_hidden_single_in_row(irow)) is not None:
                self.set_square_value(move[0], move[1], move[2])
                self.simple_solve()
        for icol in range(9):
            while (move := self._find_hidden_single_in_col(icol)) is not None:
                self.set_square_value(move[0], move[1], move[2])
                self.simple_solve()
        for ibox in range(9):
            while (move := self._find_hidden_single_in_box(ibox)) is not None:
                self.set_square_value(move[0], move[1], move[2])
                self.simple_solve()

    def _solve(self) -> str:
        """Main solve routine. Returns status string."""
        if not self.is_valid():
            return 'Invalid Puzzle ("no solution")'
        self.simple_solve()
        if self.is_complete():
            return "Unique Solution"

        init_state = np.zeros((9, 9))
        while not self.is_complete() and not np.array_equal(init_state, self.board):
            init_state = np.array(self.board)
            self.uni_possibles_solve()

        if self.is_complete():
            return "Unique Solution"

        valid = self.is_valid()
        complete = self.is_complete()
        if not valid:
            status = 'Invalid Puzzle ("no solution")'
        elif self.num_givens < 17 and valid and not complete:
            status = 'Invalid Puzzle ("not enough givens" / "multiple solutions")'
        elif valid and not complete:
            status = 'Invalid Puzzle ("no unique solution")'
        else:
            status = 'Invalid Puzzle ("unknown")'

        return status

    def solve(self) -> str:
        """Main solve routine. Returns status string."""
        return self._solve()
