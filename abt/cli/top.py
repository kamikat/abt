#!/usr/bin/env python2

"""
Show aria2 status in top-like style
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
import abt.cli.status
import sys
import time
import curses
import locale

class StdOutWrapper:
    text = ""
    def write(self,txt):
        self.text += txt
        self.text = '\n'.join(self.text.split('\n')[-30:])

def top(screen):
    screen.nodelay(True)
    try:
        while True:
            if screen.getch() == ord('q'):
                break
            screen.clear()
            scrout = StdOutWrapper()
            sys.stdout = scrout # override stdout
            abt.cli.status.print_status(aria2)
            screen.addstr(0, 0, scrout.text.encode('utf-8'))
            screen.refresh()
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    conn, extra = cli.parse_connection_options()
    args, extra = parser.parse_known_args(extra)
    aria2, _ = client.connect(**conn)

    try:
        version_info = aria2.getVersion()
    except:
        cli.error("aria2 is not running.")

    locale.setlocale(locale.LC_ALL, '')
    curses.wrapper(top)

