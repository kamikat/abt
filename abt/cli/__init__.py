import sys
import subprocess
import argparse
from os import path, listdir
from imp import load_source

progname = path.splitext(path.basename(sys.argv[0]))[0]
progname = "abt %s" % progname if progname != "abt" else "abt"
cli_path = path.dirname(__file__)

def main():
    if len(sys.argv) > 1:
        command = path.join(cli_path, "%s.py" % sys.argv[1])
        if path.exists(command):
            subprocess.call([sys.executable, command] + sys.argv[2:])
            return
    print "usage: %s <command> [<args>]\n" % progname
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

class StoreToDict(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        d = getattr(namespace, self.dest)
        for opt in values:
            k,v = opt.split("=", 1)
            k = k.lstrip("-")
            d[k] = v
        setattr(namespace, self.dest, d)

def parse_options(args):
    parser = argparse.ArgumentParser(prefix_chars=' ')
    parser.add_argument("options", nargs="*", action=StoreToDict, default=dict())
    return parser.parse_args(args).options

