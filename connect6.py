#!/usr/bin/env python

class Connect6():
    EMPTY = ' '

    def __init__(self, R = 19, C = 19):
        self.R = R
        self.C = C

        # construct grid
        self.grid = [[self.EMPTY for c in range(self.C)] for r in range(self.R)]

        # marks game over
        self.gg = False
        self.winner = None

        self.player = 'x'
        self.turns  = 1
        self.total  = 0

    def _check_winner(self, r, c):
        piece = self.grid[r][c]

        check_directions = [ (0, 1), (1, 1), (1, 0), (1, -1) ]

        for dr, dc in check_directions:
            consecutive = 1

            # check along the initial vector and the 180deg opposing vector
            for direc in [1, -1]:
                tr, tc = r + direc * dr, c + direc * dc

                while 0 <= tr < self.R and 0 <= tc < self.C and \
                    self.grid[tr][tc] == piece and consecutive < 6:
                    consecutive += 1
                    tr, tc = tr + direc * dr, tc + direc * dc

            if consecutive == 6:
                return True

        return False

    def valid(self, r, c):
        if not (0 <= r <= self.R and 0 <= c <= self.C):
            return False
        if self.grid[r][c] != self.EMPTY:
            return False

        assert self.turns > 0
        assert self.total < self.R * self.C

        return True

    def turn(self, r, c):
        assert self.valid(r, c)
        
        self.grid[r][c] = self.player
        self.total += 1
        self.turns -= 1

        winner = self._check_winner(r, c)
        if winner or self.total == self.R * self.C:
            self.gg = True

        if winner:
            self.winner = self.player
            self.player = None
        else:
            # update player
            if self.turns == 0:
                self.turns = 2
                self.player = {'x': 'o', 'o': 'x'}[self.player]

    def pos(self, r, c):
        return (2*r + 1, 4*c + 2)

    def __str__(self):
        s = ""

        row_sep = "---".join("+" * (self.C + 1)) + "\n"
        s += row_sep
        for (i, row) in enumerate(self.grid):
            s += "| " + " | ".join(row) + " |\n"
            s += row_sep

        return s
