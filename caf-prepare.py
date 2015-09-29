#!/usr/bin/env python

import os
import argparse


def get_cli():
    parser = argparse.ArgumentParser(description='Prepare job options')
    # parser.add_argument('-l', '--log',
    #                     choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
    #                     help="Logging level", default='ERROR')
    parser.add_argument('-input', '--input', help="Job option or recotf template", required=True)
    parser.add_argument('-f', '--files', help="Files", nargs='+', required=True)
    parser.add_argument('-a', '--asetup', help="asetup string", default="20.1.7.2")
    parser.add_argument('-p', '--postexec', help="Post exec script",)
    parser.add_argument('-o', '--output', help="Output folder", required=True)
    parser.add_argument("run", type=int, help="Run number")

    return parser.parse_args()


def main():
    cli = get_cli()

    prepare(jo=cli.input, files=cli.files, asetup=cli.asetup,
            postexec=cli.postexec, output=cli.output, run=cli.run)


def prepare(jo, files, asetup, postexec, output, run):
    # -------------------------------------------------------------------------
    if not os.path.exists(output):
        os.makedirs(output)
    # -------------------------------------------------------------------------
    files = ["'root://eosatlas/%s'" % f for f in files]
    # -------------------------------------------------------------------------
    base_dir = os.path.dirname(os.path.abspath(__file__))
    tmpl_dir = os.path.join(base_dir, 'tmpl')
    # -------------------------------------------------------------------------
    postexec_content = None
    if postexec:
        with open(os.path.join(tmpl_dir, postexec), 'r') as f:
            postexec_content = f.read()
            postexec_content = postexec_content.replace('{{BASEDIR}}', base_dir)
    # -------------------------------------------------------------------------
    templates = [jo, os.path.join(tmpl_dir, 'launcher.sh')]
    for i, tmpl in enumerate(templates):
        content = None
        with open(os.path.join(tmpl_dir, tmpl), 'r') as f:
            content = f.read()
            # -----------------------------------------------------------------
            content = content.replace('{{BASEDIR}}', base_dir)
            content = content.replace('{{OUTPUT}}', os.path.abspath(output))
            content = content.replace('{{RUN}}', str(run))
            content = content.replace('{{FILES}}', ', '.join(files))
            content = content.replace('{{ASETUP}}', asetup)
            # -----------------------------------------------------------------
            if postexec_content:
                content = content.replace('{{POSTEXEC}}', postexec_content)
        # ---------------------------------------------------------------------
        if content:
            output_name = "jobo.py" if i == 0 else os.path.basename(tmpl)
            with open(os.path.join(output, output_name), 'w') as f:
                f.write(content)
    # -------------------------------------------------------------------------


if __name__ == '__main__':
    main()
