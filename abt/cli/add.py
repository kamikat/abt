#!/usr/bin/env python2

"""
Add BitTorrent download task
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client
import base64

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('torrent', nargs='?', action='store', help="path to torrent file")
    parser.add_argument('--uri', action='store', help="load torrent file from uri")
    args, extra = parser.parse_known_args()
    options = cli.parse_options(extra)

    if (not args.torrent) == (not args.uri):
        parser.error("Exactly one of torrent file path or --uri is expected.")

    aria2, _ = client.connect()

    if args.torrent:
        torrent_data = open(args.torrent, 'rb').read()
        torrent_b64 = base64.b64encode(torrent_data)
        print aria2.addTorrent(torrent_b64, [], options)
    else:
        options['follow-torrent'] = 'true'
        print aria2.addUri([args.uri], options)

