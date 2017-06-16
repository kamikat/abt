#!/usr/bin/env python2

"""
Add BitTorrent download task
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
import base64
import os
import tempfile

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('torrent', nargs='?', action='store', help="path to torrent file")
    parser.add_argument('--uri', action='store', help="load torrent file from uri")
    conn, extra = cli.parse_connection_options()
    options, extra = cli.parse_option_dict(extra)
    args = parser.parse_args(extra)

    if (not args.torrent) == (not args.uri):
        parser.error("Exactly one of torrent file path or --uri is expected.")

    aria2, _ = client.connect(**conn)

    if args.uri:
        _, torrent_file = tempfile.mkstemp()
        fmt = "aria2c --no-conf --allow-overwrite=true --follow-torrent=false --async-dns=false --dir=%s --out=%s \"%s\""
        cmd = fmt % (os.path.dirname(torrent_file), os.path.basename(torrent_file), args.uri)
        ret = os.system(cmd)
        if ret != 0:
            cli.error("Failed. Cannot fetch torrent from %s" % args.uri)
    else:
        torrent_file = args.torrent

    torrent_data = open(torrent_file, 'rb').read()
    torrent_b64 = base64.b64encode(torrent_data)
    print aria2.addTorrent(torrent_b64, [], options)

