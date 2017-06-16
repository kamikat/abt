#!/usr/bin/env python2

"""
Get/set aria2 options
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
import base64
import os
import tempfile

def print_options(options):
    for k, v in options.items():
        print "--%s=%s" % (k, v)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('gid', nargs='?', action='store', help="gid to show/change options of")
    conn, extra = cli.parse_connection_options()
    options, extra = cli.parse_option_dict(extra)
    args = parser.parse_args(extra)
    aria2, _ = client.connect(**conn)

    if not args.gid:
        if options:
            print aria2.changeGlobalOption(options)
        else:
            print_options(aria2.getGlobalOption())
    else:
        if options:
            print aria2.changeOption(args.gid, options)
        else:
            print_options(aria2.getOption(args.gid))

