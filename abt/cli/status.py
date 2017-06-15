#!/usr/bin/env python2

"""
Show aria2 status
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

def print_status(aria2, active=True, waiting=False, stopped=False):
    summary = aria2.getGlobalStat()

    print "aria2 ({0} active, {1} waiting, {2} stopped)".format(
            summary['numActive'], summary['numWaiting'],
            summary['numStopped'], summary['numStoppedTotal'])

    if active:
        print_active(aria2)

    if waiting:
        print_waiting(aria2)

    if stopped:
        print_stopped(aria2)

    print
    print u"\u21f1 {0}/s".format(naturalsize(summary['uploadSpeed']))
    print u"\u21f2 {0}/s".format(naturalsize(summary['downloadSpeed']))
    print

def print_active(aria2):
    print
    print "Active Tasks (gid/sz/prg/conn/up/down):\n"
    active_info = aria2.tellActive(['gid', 'totalLength', 'completedLength', 'connections', 'numSeeders', 'seeder', 'dir', 'uploadSpeed', 'downloadSpeed'])
    if len(active_info) == 0:
        print "  (empty)"
        return
    for info in active_info:
        print "  {0:<16} {1:>10} {2:>4.0f}% {3:<6} {4:<11} {5:<11}".format(
                info['gid'],
                naturalsize(info['totalLength']) if int(info['totalLength']) > 0 else "-",
                round(100 * float(info['completedLength']) / float(info['totalLength'])) if int(info['totalLength']) > 0 else "-",
                "%s(%s)" % (info['connections'], info['numSeeders']) if info['seeder'] != 'true' else info['connections'],
                format_speed(info['uploadSpeed']),
                format_speed(info['downloadSpeed']))

def print_waiting(aria2):
    print
    print "Waiting Tasks (gid/sz/prg/dir):\n"
    task_info = aria2.tellWaiting(0, 100, ['gid', 'totalLength', 'completedLength', 'connections', 'numSeeders', 'seeder', 'dir', 'uploadSpeed', 'downloadSpeed'])
    if len(task_info) == 0:
        print "  (empty)"
        return
    for info in task_info:
        print "  {0:<16} {1:>10} {2:>4.0f}% {3}".format(
                info['gid'],
                naturalsize(info['totalLength']) if int(info['totalLength']) > 0 else "-",
                round(100 * float(info['completedLength']) / float(info['totalLength'])) if int(info['totalLength']) > 0 else "-",
                info['dir'])

def print_stopped(aria2):
    print
    print "Stopped Tasks (gid/sz/prg/dir):\n"
    task_info = aria2.tellStopped(0, 100, ['gid', 'totalLength', 'completedLength', 'connections', 'numSeeders', 'seeder', 'dir', 'uploadSpeed', 'downloadSpeed'])
    if len(task_info) == 0:
        print "  (empty)"
        return
    for info in task_info:
        print "  {0:<16} {1:>10} {2:>4.0f}% {3}".format(
                info['gid'],
                naturalsize(info['totalLength']) if int(info['totalLength']) > 0 else "-",
                round(100 * float(info['completedLength']) / float(info['totalLength'])) if int(info['totalLength']) > 0 else "-",
                info['dir'])

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

