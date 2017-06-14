from sys import argv
from os.path import basename, splitext

progname = "abt %s" % splitext(basename(argv[0]))[0]
