#!/usr/bin/env python

import os
import argparse


def get_cli():
    parser = argparse.ArgumentParser(description='Prepare job options')
    # parser.add_argument('-l', '--log',
    #                     choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
    #                     help="Logging level", default='ERROR')
    parser.add_argument('-t', '--templates', help="Templates", nargs='+', required=True)
    parser.add_argument('-f', '--files', help="Files", nargs='+', required=True)
    parser.add_argument('-a', '--asetup', help="asetup string", default="20.1.7.2")
    parser.add_argument('-p', '--postexec', help="Post exec script",)
    parser.add_argument('-o', '--output', help="Output folder", required=True)
    parser.add_argument("run", type=int, help="Run number")

    return parser.parse_args()


def main():
    cli = get_cli()
    if not os.path.exists(cli.output):
        os.makedirs(cli.output)
    files = ["'root://eos/%s'" % f for f in cli.files]
    for tmpl in cli.templates:
        content = None
        with open(tmpl, 'r') as f:
            content = f.read()
            content = content.replace('{{RUN}}', str(cli.run))
            content = content.replace('{{FILES}}', ', '.join(files))
            content = content.replace('{{ASETUP}}', cli.asetup)
        if content:
            with open(os.path.join(cli.output, "jobo.py"), 'w') as f:
                f.write(content)


if __name__ == '__main__':
    main()
