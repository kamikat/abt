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
    args, extra = parser.parse_known_args()
    options = cli.parse_options(extra)

    if (not args.torrent) == (not args.uri):
        parser.error("Exactly one of torrent file path or --uri is expected.")

    aria2, _ = client.connect()

    if args.uri:
        torrent_file = tempfile.mkstemp()
        ret = os.system("aria2c --no-conf --async-dns=false --dir=%s --out=%s \"%s\"" % (os.path.dirname(torrent_file),
                                                                                         os.path.basename(torrent_file),
                                                                                         args.uri))
        if ret != 0:
            cli.error("Failed. Cannot fetch torrent from %s", args.uri)
    else:
        torrent_file = args.torrent

    torrent_data = open(torrent_file, 'rb').read()
    torrent_b64 = base64.b64encode(torrent_data)
    print aria2.addTorrent(torrent_b64, [], options)

