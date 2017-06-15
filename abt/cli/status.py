#!/usr/bin/env python2

"""
Show aria2 status
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
import abt.format as fmt

keys = ['gid', 'status', 'totalLength', 'completedLength', 'connections', 'numSeeders', 'seeder', 'dir', 'uploadSpeed', 'downloadSpeed']

def print_status(aria2, active=True, waiting=False, stopped=False):
    summary = aria2.getGlobalStat()

    print "aria2 ({numActive} active, {numWaiting} waiting, {numStopped} stopped)".format(**summary)

    def print_tasks(pattern, tasks):
        if len(tasks) == 0:
            print "  (empty)"
        for task in tasks:
            print pattern % fmt.Task(task)

    if active:
        print
        print "Active Tasks (gid/sz/prg/conn/up/down):\n"
        print_tasks("  %(gid)s %(sz)s %(prg)s  %(conn)s %(up)s %(down)s", aria2.tellActive(keys))

    if waiting:
        print
        print "Waiting Tasks (gid/sz/prg/dir):\n"
        print_tasks("  %(gid)s %(sz)s %(prg)s  %(dir)s", aria2.tellWaiting(0, 999, keys))

    if stopped:
        print
        print "Stopped Tasks (gid/sz/prg/dir):\n"
        print_tasks("  %(gid)s %(sz)s %(prg)s  %(dir)s", aria2.tellStopped(0, 999, keys))

    print
    print u"\u21f1 {}".format(fmt.format_speed(summary['uploadSpeed']))
    print u"\u21f2 {}".format(fmt.format_speed(summary['downloadSpeed']))
    print

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('-a', '--all', action='store_true', help="show all tasks")
    parser.add_argument('--waiting', action='store_true', help="show waiting tasks")
    parser.add_argument('--stopped', action='store_true', help="show stopped tasks")
    parser.add_argument('--no-active', action='store_false', dest='active', help="hide active tasks")
    conn, extra = cli.parse_connection_options()
    args, extra = parser.parse_known_args(extra)
    aria2, _ = client.connect(**conn)

    try:
        version_info = aria2.getVersion()
    except:
        cli.error("aria2 is not running.")

    print_status(aria2, active=args.all or args.active,
                       waiting=args.all or args.waiting,
                       stopped=args.all or args.stopped)

