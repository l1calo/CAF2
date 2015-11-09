#!/usr/bin/env python
# ======================================================================
import argparse
# ======================================================================
import peewee
# ======================================================================
import settings
import caf_prepare
import models
# ======================================================================


def get_cli():
    parser = argparse.ArgumentParser(description='Prepare job options for analysis')
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument('-o', '--output', help="Output directory")
    parser.add_argument('-d', '--dry',
                        help="Dry run - create options, but not update status in database",
                        action='store_true')
    parser.add_argument('-r', "--run", type=int, help="Prepare only for selected run")

    return parser.parse_args()

def prepare_analysis(analysis, files, output, asetup=None, dry=False, run=None):
    caf_prepare.prepare(
        jo=analysis['file'],
        files=files,
        output=output,
        asetup=asetup,
        postexec=analysis['postexec']
    )

def prepare(analyses, files, output, asetup=None, dry=False, run=None):
    models.connect()
    # for ana in analyses:
    #     for (run in models.Run.select().Join(model.Job, peewee.JOIN.LEFT_OUTER).where(
    #         models.Job.Analysis == ana
    #     ).count()):
    #         prepare_analysis(ana, files, output, asetup, dry, run)


def main():
    cli = get_cli()
    prepare(
        analyses=settings.ANALYSIS,
        output=cli.output,
        dry=cli.dry,
        run=cli.run
    )

if __name__ == '__main__':
    main()
