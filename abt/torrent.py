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
