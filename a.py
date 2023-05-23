import curses
import time
import asyncio

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()


loglines = []
errors = []

def make_color(num, color):
    curses.init_pair(num, color, curses.COLOR_BLACK)
    return curses.color_pair(num)

@curses.wrapper
def main(stdscr):
    # Clear screen
    stdscr.clear()

    ERROR_COLOR = make_color(1, curses.COLOR_RED)
    COPYTEXT_COLOR = make_color(2, curses.COLOR_BLUE)
    LOG_COLOR = make_color(3, curses.COLOR_YELLOW)
    MEASURE_COLOR = make_color(4, curses.COLOR_GREEN)
    PROGRESS_COLOR = make_color(5, curses.COLOR_WHITE)

    nerrors = 0
    nsuccess = 1
    oldheight, oldwidth = (0,0)
    for i in range(1,10000):
        loglines.append(str(i)*20)
        height, width = stdscr.getmaxyx()
        if oldheight != height or oldwidth != width:
            # this is a resize event
            stdscr.clear()
            curses.resizeterm(height, width)
            oldheight, oldwidth = (height, width)

        nloglines = height-5
        offset = 2
        for line in loglines[-nloglines:]:
            trimmedline = line[0:width-2]
            stdscr.addstr(offset,1,trimmedline,LOG_COLOR)
            offset += 1
        
        stdscr.addstr(0,1,f"Errors: {nerrors}", ERROR_COLOR)
        stdscr.addstr(1,1,"Current Requests: ", COPYTEXT_COLOR)

        progressstr = "Total Progress: ="
        stdscr.addstr(height-3,1,progressstr, COPYTEXT_COLOR)
        prog = int((0.5)*100)
        progwidth = width - 1 - len(progressstr) - 4
        stdscr.addstr(height-3,len(progressstr), "_"*progwidth, PROGRESS_COLOR)
        stdscr.addstr(height-3,len(progressstr)+progwidth+1, f"{prog}%", MEASURE_COLOR)

        successstr = "Data successfully saved for requests up to"
        successstr = successstr[0:width-10]
        successpct = int((0.45)*100)
        stdscr.addstr(height-1,1,successstr +": ", COPYTEXT_COLOR)
        stdscr.addstr(height-1,len(successstr)+3, f"{successpct}%", MEASURE_COLOR)

        stdscr.refresh()
        i += 1
        time.sleep(0.1)
    stdscr.getkey()

