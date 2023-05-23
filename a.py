import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)


curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()



@curses.wrapper
def main(stdscr):
    # Clear screen
    stdscr.clear()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)

    ERROR_COLOR = curses.color_pair(1)
    COPYTEXT_COLOR = curses.color_pair(2)
    LOG_COLOR = curses.color_pair(3)
    MEASURE_COLOR = curses.color_pair(4)
    PROGRESS_COLOR = curses.color_pair(5)

    stdscr.addstr(1,0,'ERROR_COLOR',ERROR_COLOR)
    stdscr.addstr(2,0,'COPYTEXT_COLOR',COPYTEXT_COLOR)
    stdscr.addstr(3,0,'LOG_COLOR',LOG_COLOR)
    stdscr.addstr(4,0,'MEASURE_COLOR',MEASURE_COLOR)
    stdscr.addstr(5,0,'PROGRESS_COLOR',PROGRESS_COLOR)

    stdscr.refresh()
    stdscr.getkey()
