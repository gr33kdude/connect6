#!/usr/bin/env python

from connect6 import Connect6
import curses

def plural(val, suffix):
    return "" if val == 1 else suffix

def bound(MIN, val, MAX):
    return max(MIN, min(MAX, val))

def status_line(scr, s):
    h, w = scr.getmaxyx()
    r, c = scr.getyx()
    scr.move(h-1, 0)
    scr.clrtoeol()
    scr.addstr(s)
    scr.move(r, c)

class ScreenNotBigEnoughException():
    def __init__(self, h, w):
        self.h = h
        self.w = w

    def __str__(self):
        s = "Error: terminal screen too small; resize to at least {}x{}"
        return s.format(self.w, self.h)

def main(scr):
    c6 = Connect6()

    h, w = scr.getmaxyx()
    R, C = c6.pos(c6.R, c6.C)
    R += 1 + 1 # 0-based-to-1 + status line
    C += 1     # 0-based-to-1
    print
    if h < R or w < C:
        raise ScreenNotBigEnoughException(R, C)

    # start the cursor in the middle of the grid
    r, c = c6.R / 2, c6.C / 2
    scr.addstr(str(c6))
    scr.refresh()

    move_keys = {
        curses.KEY_LEFT:  (0, -1),
        ord('h'):         (0, -1),
        curses.KEY_DOWN:  (1, 0),
        ord('j'):         (1, 0),
        curses.KEY_UP:    (-1, 0),
        ord('k'):         (-1, 0),
        curses.KEY_RIGHT: (0, 1),
        ord('l'):         (0, 1),
    }

    statline = ""
    done = False
    while not done:
        #status_line(scr, "You pressed key: {}".format(curses.keyname(ch)))

        args = [c6.player.upper(), c6.turns, plural(c6.turns, "s")]
        statline += "It is player {}'s turn.  You have {} move{} left.".format(*args)
        status_line(scr, statline)

        scr.refresh()
        ch = scr.getch(*c6.pos(r, c))

        if ch in move_keys.keys():
            dr, dc = move_keys[ch]
            r, c = (bound(0, r + dr, c6.R - 1), bound(0, c + dc, c6.C - 1))
        elif ch == ord('q'):
            done = True
        elif ch == ord(' ') or ch == curses.KEY_ENTER:
            if c6.valid(r, c):
                pr, pc = c6.pos(r, c)
                scr.addch(pr, pc, ord(c6.player.upper()))
                c6.turn(r, c)
            else:
                statline = "Invalid move!  "
                #curses.beep()
                curses.flash()
                continue

        if c6.gg:
            if c6.winner:
                status_line(scr, "GAME OVER: PLAYER {} WINS!!!".format(c6.winner.upper()))
            else:
                status_line(scr, "GAME OVER: DRAW!")
            scr.refresh()
            curses.curs_set(0)
            ch = scr.getch()
            done = True

        statline = ""

try:
    curses.wrapper(main)
except ScreenNotBigEnoughException as e:
    print e
