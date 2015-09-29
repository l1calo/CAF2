#!/usr/bin/env python

import os
import subprocess
import argparse


def get_cli():
    parser = argparse.ArgumentParser(description='Submit job')
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument(
        '-t', '--type', help="Submit engine", choices=['local', 'bsub'], default='local')
    parser.add_argument('folder', help="Folder with launcher.sh")

    return parser.parse_args()


def get_launcher(folder):
    return os.path.join(folder, 'launcher.sh')


def submit(folder, kind):
    folder_abs = os.path.abspath(folder)
    os.chdir(folder_abs)
    if kind == 'local':
        return local(folder_abs)
    return None


def local(folder):
    p = subprocess.Popen([get_launcher(folder)], stdout=subprocess.PIPE)
    with open(os.path.join(folder, 'log.out'), 'w') as log:
        while p.poll() is None:
            l = p.stdout.readline()  # This blocks until it receives a newline.
            print l,
            log.write(l)
        last = p.stdout.read()
        print last
        log.write(last)

def main():
    cli = get_cli()
    result = submit(folder=cli.folder, kind=cli.type)

if __name__ == '__main__':
    main()
