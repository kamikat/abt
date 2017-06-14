import argparse
from sys import argv
from os.path import basename, splitext

progname = "abt %s" % splitext(basename(argv[0]))[0]

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

