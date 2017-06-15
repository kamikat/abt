import sys
import subprocess
import argparse
import abt.rpc_client as client
from os import path, listdir
from imp import load_source
from sys import exit as error

progname = path.splitext(path.basename(sys.argv[0]))[0]
progname = "abt %s" % progname if progname != "abt" else "abt"
cli_path = path.dirname(__file__)

def main():
    if len(sys.argv) > 1:
        command = path.join(cli_path, "%s.py" % sys.argv[1])
        if path.exists(command):
            try:
                subprocess.call([sys.executable, command] + sys.argv[2:])
            except KeyboardInterrupt:
                pass
            return
    print "usage: %s <command> [<args>]" % progname
    print "       %s <command> [--jsonrpc JSONRPC] [--no-verify] [--ca-certificate CA_CERTIFICATE] [<args>]" % progname
    print "       %s <command> [-h]\n" % progname
    print "abt is a BitTorrent management workflow.\n"
    print "List of Commands:"
    for command_source in listdir(cli_path):
        if command_source.endswith('.pyc') or command_source.startswith('__'):
            continue
        command = command_source.split('.')[0]
        command_file = path.join(cli_path, command_source)
        command_module = load_source(command, command_file)
        description = command_module.__doc__.strip().replace('\n', '\n' + ' ' * 20) if command_module.__doc__ else ""
        print "   %s %s" % ("{0: <16}".format(command), description)
    print

def parse_connection_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(prog="abt", usage="%(prog)s <command> [--jsonrpc JSONRPC] [--no-verify] [--ca-certificate CA_CERTIFICATE]", add_help=False)
    parser.add_argument("--jsonrpc", action='store', dest='url', default="http://localhost:6800/jsonrpc")
    parser.add_argument("--no-verify", action='store_true')
    parser.add_argument("--ca-certificate", action='store', dest='ca_file')
    args, extra = parser.parse_known_args(args)
    return vars(args), extra

class StoreToDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest)
        for opt in values:
            try:
                k,v = opt.split("=", 1)
            except:
                parser.error("invalid option '%s'" % opt)
            k = k.lstrip("-")
            d[k] = v
        setattr(namespace, self.dest, d)

def parse_options(args):
    parser = argparse.ArgumentParser(prefix_chars=' ', prog="abt", usage="%(prog)s <command> [<args>] [--<key>=<value> [--<key>=<value> ...]]", add_help=False)
    parser.add_argument("options", nargs="*", action=StoreToDict, default=dict())
    return parser.parse_args(args).options

