#!/usr/bin/env python2

"""
This is a template file of abt command
"""

import argparse
import abt.cli as cli
import abt.rpc_client as client

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=cli.progname, description=__doc__.strip())
    parser.add_argument('arg1', action='store', help="balabalah")
    parser.add_argument('arg2', action='store', help="balabalah")
    parser.add_argument('--opt1', action='store', help="balabalah")
    parser.add_argument('--opt2', action='store', help="balabalah")
    args = parser.parse_args()

