#!/usr/bin/env python2

import os
import hashlib

def get_pieces(files, piece_length=0x8000):
    if isinstance(files, basestring):
        files = [ files ]
    piece_data = ""
    for f in files:
        current_file = open(f, 'rb')
        while True:
            piece_data += current_file.read(piece_length - len(piece_data))
            if len(piece_data) != piece_length:
                current_file.close()
                break
            yield piece_data
            piece_data = ""
    if piece_data:
        yield piece_data

def get_files(path):
    for (dirname, dirs, files) in os.walk(path):
        for f in files:
            yield os.path.join(dirname, f)

def get_checksum(data):
    m = hashlib.sha1()
    m.update(data)
    return m.digest()

def create_torrent_data(path, name=None, announce=None, announce_list=None, private_flag=False, piece_length=0x8000):
    info = {}
    info['name'] = name if name else os.path.basename(path)
    info['piece length'] = piece_length
    if private_flag:
        info['private'] = 1
    if os.path.isfile(path):
        info['length'] = os.path.getsize(path);
        pieces_data = get_pieces(path)
    else:
        files = [ f for f in get_files(path) ]
        info['files'] = [ { 'path': [ os.path.relpath(f, path) ], 'length': os.path.getsize(f) } for f in files ]
        pieces_data = get_pieces(files)
    info['pieces'] = ''.join(map(get_checksum, pieces_data))
    torrent = {}
    if announce:
        torrent['announce'] = announce
    if announce_list:
        torrent['announce-list'] = [ [announce] for announce in announce_list ]
    torrent['info'] = info
    return torrent

def main():
    import sys
    import argparse
    import better_bencode as bb

    parser = argparse.ArgumentParser(description="Create torrent.")
    parser.add_argument('path', action='store', help="the path of file or directory to share")
    parser.add_argument('--add-tracker', action='append', dest='announce_list', metavar='TRACKER',
                                         help="add tracker (NOTE torrent without tracker can only be inferred from DHT)")
    parser.add_argument('--comment', action='store', help="add torrent file comment")
    parser.add_argument('--name', action='store', help="set name of shared file/directory")
    parser.add_argument('--private', action='store_true', help="flag for restricted access")
    parser.add_argument('--output', action='store', help="save torrent to file")
    args = parser.parse_args()

    torrent = create_torrent_data(args.path, name=args.name, announce_list=args.announce_list, private_flag=args.private)

    if args.comment:
        torrent['comment'] = args.comment

    out = sys.stdout

    if args.output:
        out = open(args.output, 'wb')

    out.write(bb.dumps(torrent))

if __name__ == '__main__':
    main()

