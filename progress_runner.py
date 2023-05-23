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

nerrors = 0
nsuccess = 0


def make_color(num, color):
    curses.init_pair(num, color, curses.COLOR_BLACK)
    return curses.color_pair(num)


async def display_main(stdscr, params):
    global nsuccess, nerrors, loglines

    stdscr.clear()

    ERROR_COLOR = make_color(1, curses.COLOR_RED)
    COPYTEXT_COLOR = make_color(2, curses.COLOR_BLUE)
    LOG_COLOR = make_color(3, curses.COLOR_YELLOW)
    MEASURE_COLOR = make_color(4, curses.COLOR_GREEN)
    PROGRESS_COLOR = make_color(5, curses.COLOR_WHITE)

    oldheight, oldwidth = (0,0)
    for i in range(1,10000):
        # loglines.append(str(i)*20)
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
        prog = (nsuccess+nerrors)/(nsuccess+nerrors+len(params))
        progwidth = width - 1 - len(progressstr) - 4
        progstr = "="*int(progwidth*prog) + "_"*int(progwidth*(1-prog))
        stdscr.addstr(height-3,len(progressstr), progstr, PROGRESS_COLOR)
        stdscr.addstr(height-3,len(progressstr)+progwidth+1, f"{int(100*prog)}%", MEASURE_COLOR)

        successstr = "Data successfully saved for requests up to"
        successstr = successstr[0:width-10]
        successpct = int(100*nsuccess/(nsuccess+nerrors+len(params)))
        stdscr.addstr(height-1,1,successstr +": ", COPYTEXT_COLOR)
        stdscr.addstr(height-1,len(successstr)+3, f"{successpct}%", MEASURE_COLOR)

        stdscr.refresh()
        await asyncio.sleep(0.1)
    stdscr.getkey()


async def worker(fn, params):
    global nsuccess, nerrors
    while len(params) > 0:
        p = params.pop()
        ret = await fn(*p)
        if ret:
            nsuccess += 1
        else:
            nerrors += 1


async def run_tasks(fn, params, nthreads):
    workers = [ ]
    for i in range(nthreads):
        workers.append(worker(fn, params))

    await asyncio.gather(*workers)


async def run_display_and_tasks(stdscr, fn, params, nthreads=5):
    await asyncio.gather(display_main(stdscr, params), run_tasks(fn, params, nthreads))


import random

async def custom_fn(num):
    loglines.append(f"{num} ")
    await asyncio.sleep(random.random())
    return random.random() > 0.1




def main(stdscr):
    params = [ [i] for i in range(1000) ]
    asyncio.run(run_display_and_tasks(stdscr, custom_fn, params, nthreads=20))
    
def

if __name__ == "__main__":
    curses.wrapper(main)
