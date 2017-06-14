import sys
import subprocess
from os import path, listdir
from imp import load_source

cli_path = path.join(path.dirname(__file__), 'cli')

def main():
    if len(sys.argv) > 1:
        command = path.join(cli_path, "%s.py" % sys.argv[1])
        if path.exists(command):
            subprocess.call([sys.executable, command] + sys.argv[2:])
            return
    print "usage: %s <command> [<args>]\n" % sys.argv[0]
    print "abt is a BitTorrent management workflow.\n"
    print "List of Commands:"
    for command_source in listdir(cli_path):
        if command_source.endswith('.pyc') or command_source.startswith('__'):
            continue
        command = command_source.split('.')[0]
        command_file = path.join(cli_path, command_source)
        command_module = load_source(command, command_file)
        description = command_module.__doc__.strip() if command_module.__doc__ else ""
        print "   %s %s" % ("{0: <16}".format(command), description)
    print

main()
