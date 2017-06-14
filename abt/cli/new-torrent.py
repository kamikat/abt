#!/usr/bin/env python2

"""
Create torrent.
"""

import sys
import argparse
import better_bencode as bb
import abt.torrent as torrent
import abt.cli as cli

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('path', action='store', help="the path of file or directory to share")
    parser.add_argument('--add-tracker', action='append', dest='announce_list', metavar='TRACKER',
                                         help="add tracker (NOTE torrent without tracker can only be inferred from DHT)")
    parser.add_argument('--comment', action='store', help="add torrent file comment")
    parser.add_argument('--name', action='store', help="set name of shared file/directory")
    parser.add_argument('--private', action='store_true', help="flag for restricted access")
    parser.add_argument('--output', action='store', help="save torrent to file")
    args = parser.parse_args()

    torrent_data = torrent.create_torrent_data(args.path, name=args.name, announce_list=args.announce_list, private_flag=args.private)

    if args.comment:
        torrent_data['comment'] = args.comment

    out = sys.stdout

    if args.output:
        out = open(args.output, 'wb')

    out.write(bb.dumps(torrent_data))
