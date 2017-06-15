#!/usr/bin/env python2

"""
Show aria2 daemon/task status
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
from humanize import naturalsize

def format_speed(speed):
    if int(speed) == 0:
        return "-"
    else:
        return "%s/s" % naturalsize(speed)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('pathspec', nargs='?', action='store', help="path to task folder")
    conn, extra = cli.parse_connection_options()
    args, extra = parser.parse_known_args(extra)

    aria2, _ = client.connect(**conn)

    try:
        version_info = aria2.getVersion()
    except:
        cli.error("aria2 is not running.")

    print "aria2 %s" % version_info['version'],

    summary = aria2.getGlobalStat()

    print "({0} active, {1} waiting, {3} stopped)".format(
            summary['numActive'], summary['numWaiting'],
            summary['numStopped'], summary['numStoppedTotal'])

    active_info = aria2.tellActive(['gid', 'totalLength', 'completedLength', 'connections', 'numSeeders', 'dir', 'uploadSpeed', 'downloadSpeed'])

    if active_info:
        print
        print "Active Tasks (gid/sz/prg/conn/up/down):\n"
        for info in active_info:
            print "  {0:<16} {1:>10} {2:>4.0f}% {3:<6} {4:<11} {5:<11}".format(
                    info['gid'], naturalsize(info['totalLength']),
                    round(100 * float(info['completedLength']) / float(info['totalLength'])),
                    "%s(%s)" % (info['connections'], info['numSeeders']),
                    format_speed(info['uploadSpeed']),
                    format_speed(info['downloadSpeed']))
    print
    print u"\u21f1 {0}/s".format(naturalsize(summary['uploadSpeed']))
    print u"\u21f2 {0}/s".format(naturalsize(summary['downloadSpeed']))
    print
