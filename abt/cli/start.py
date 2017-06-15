#!/usr/bin/env python2

"""
Put waiting task to active
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('gid', action='store', help="gid of the task to start")
    conn, extra = cli.parse_connection_options()
    args, extra = parser.parse_known_args(extra)

    aria2, _ = client.connect(**conn)

    print aria2.unpause(args.gid)

