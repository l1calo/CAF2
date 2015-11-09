#!/usr/bin/env python
"""
Find calibration runs and save them to the database for further processing.
Search parameters are defined in :mod:`settings` module.

Uses database schema defined in :mod:`model`

.. code-block:: bash
    usage: caf_db_find.py [-h] [-l {ERROR,WARNING,INFO,DEBUG,VERBOSE}] [-r]

    Find runs by the specified creterias

    optional arguments:
      -h, --help            show this help message and exit
      -l {ERROR,WARNING,INFO,DEBUG,VERBOSE}, --log {ERROR,WARNING,INFO,DEBUG,VERBOSE}
                            Logging level
      -r, --recreate        Recreate database


"""
# ======================================================================
import json
import argparse
# import pdb
# ======================================================================
import settings
import models
import peewee
# ======================================================================
import caf_find
import caf_files
# ======================================================================


def _get_cli():
    parser = argparse.ArgumentParser(
        description='Find runs by the certain creteria'
    )
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument('-r', '--recreate', action='store_true',
                        help="Recreate database", default=False)
    return parser.parse_args()
# ======================================================================


def _process_listener(lst, loglevel):
    runs = caf_find.get_runs(
        run=lst['initialrun'],
        loglevel=loglevel,
        runtype=lst['runtype'],
        partitions=lst['daqpartitions'],
        recenabled=lst.get('reconly', True),
        cleanstop=lst.get('cleanstop', True),
        minevents=lst.get('minevents', 0)
    )

    try:
        db_lst = models.Listener.get(models.Listener.Name == lst['name'])
    except peewee.DoesNotExist:
        db_lst = models.Listener.create(Name=lst['name'])

    for run in runs:
        files = caf_files.get_files(run['RunNumber'])
        if not files:
            print("Could not find files for run %d" % run['RunNumber'])
            continue
        try:
            db_run = models.Run.get(models.Run.RunNumber == run['RunNumber'])
        except peewee.DoesNotExist:
            db_run = models.Run.create(**run)
            for f in files:
                db_file = models.File.create(Name=f, Run=db_run)
        run_lst = [l for l in db_run.Listeners if l.Name == db_lst.Name]
        if not run_lst:
            db_run.Listeners.add(db_lst)

    print(json.dumps(runs, indent=2))
# ======================================================================


def _main():
    cli = _get_cli()
    models.connect(recreate=cli.recreate)

    for listener in settings.SCANS:
        if listener.get('enabled', True):
            _process_listener(listener, cli.log)
# ======================================================================

if __name__ == '__main__':
    _main()
