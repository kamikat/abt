#!/usr/bin/env python2

"""
Remove download task
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('gid', action='store', help="gid of the task to remove")
    parser.add_argument('-f', '--force', action='store_true', help="remove task immediately without sending stats to tracker")
    conn, extra = cli.parse_connection_options()
    args, extra = parser.parse_known_args(extra)

    aria2, _ = client.connect(**conn)

    if args.force:
        print aria2.forceRemove(args.gid)
    else:
        print aria2.remove(args.gid)

    aria2.removeDownloadResult(args.gid)
