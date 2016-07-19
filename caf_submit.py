#!/usr/bin/env python
"""
Submit a job from the specified folder.

This tool can be executed as a standalone program or used as a library.

.. code-block:: bash

    usage: caf_submit.py [-h] [-l {ERROR,WARNING,INFO,DEBUG,VERBOSE}]
                         [-t {local,bsub}]
                         folder

    Submit job

    positional arguments:
      folder                Folder with the launcher.sh

    optional arguments:
      -h, --help            show this help message and exit
      -l {ERROR,WARNING,INFO,DEBUG,VERBOSE}, --log {ERROR,WARNING,INFO,DEBUG,VERBOSE}
                            Logging level
      -t {local,bsub}, --type {local,bsub}
                            Submit engine

"""

import os
import subprocess
import argparse


def _get_cli():
    parser = argparse.ArgumentParser(description='Submit job')
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument(
        '-t', '--type', help="Submit engine", choices=['local', 'bsub'], default='local')
    parser.add_argument('folder', help="Folder with the launcher.sh")

    return parser.parse_args()


def _get_launcher(folder):
    return os.path.join(folder, 'launcher.sh')


def submit(folder, kind):
    """ Submit job from the specified folder
    Folder should contains launcher.sh script that do the main jon

    Args:
        folder (string): Folder with launcher.sh script
        kind (string): Name of the job processing backend. Can be `local`
        (for example run at lxplus) or `bsub` batch system (not implemented yet)
    """
    folder_abs = os.path.abspath(folder)
    os.chdir(folder_abs)
    if kind == 'local':
        _local(folder_abs)


def _local(folder):
    p = subprocess.Popen([_get_launcher(folder)], stdout=subprocess.PIPE)
    with open(os.path.join(folder, 'log.out'), 'w') as log:
        while p.poll() is None:
            l = p.stdout.readline()  # This blocks until it receives a newline.
            print l,
            log.write(l)
        last = p.stdout.read()
        print last
        log.write(last)


def _main():
    cli = _get_cli()
    submit(folder=cli.folder, kind=cli.type)

if __name__ == '__main__':
    _main()
