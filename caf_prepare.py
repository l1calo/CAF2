#!/usr/bin/env python
"""
Generate job options for the specified analysis.


This tool can be executed as a standalone program or used as a library.

.. code-block:: bash

    usage: caf_prepare.py [-h] -input INPUT -f FILES [FILES ...] [-a ASETUP]
                          [-p POSTEXEC] -o OUTPUT

    Prepare job options

    optional arguments:
      -h, --help            show this help message and exit
      -input INPUT, --input INPUT
                            Job option or recotf template
      -f FILES [FILES ...], --files FILES [FILES ...]
                            Files
      -a ASETUP, --asetup ASETUP
                            asetup string
      -p POSTEXEC, --postexec POSTEXEC
                            Post exec script
      -o OUTPUT, --output OUTPUT
                            Output folder
"""
# ======================================================================
import os
import argparse
# ======================================================================


def _get_cli():
    parser = argparse.ArgumentParser(description='Prepare job options')
    # parser.add_argument('-l', '--log',
    #                     choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
    #                     help="Logging level", default='ERROR')
    parser.add_argument('-input', '--input', help="Job option or recotf template", required=True)
    parser.add_argument('-f', '--files', help="Files", nargs='+', required=True)
    parser.add_argument('-a', '--asetup', help="asetup string", default="20.1.7.2")
    parser.add_argument('-p', '--postexec', help="Post exec script",)
    parser.add_argument('-o', '--output', help="Output folder", required=True)

    return parser.parse_args()
# ======================================================================


def _main():
    cli = _get_cli()

    prepare(jo=cli.input, files=cli.files, asetup=cli.asetup,
            postexec=cli.postexec, output=cli.output)
# ======================================================================


def prepare(jo, files, output, asetup=None, postexec=None):
    """ Generate job options for the spedified analysis.

    Args:
        jo (string): path to job options
        files ([string]): raw files for analysis
        output ([string]): output directory
        asetup (string): parameters of `asetup` command
        postexec (string): path to the script that runs after the job options
    """
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
# ======================================================================

if __name__ == '__main__':
    _main()
# ======================================================================
