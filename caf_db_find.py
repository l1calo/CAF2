#!/usr/bin/env python
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
# ======================================================================


def get_cli():
    parser = argparse.ArgumentParser(
        description='Find runs by the certain creteria'
    )
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument('-r', '--recreate', type=bool,
                        help="Recreate database", default=False)
    return parser.parse_args()
# ======================================================================


def process_listener(lst, loglevel):
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
        try:
            db_run = models.Run.get(models.Run.RunNumber == run['RunNumber'])
        except peewee.DoesNotExist:
            db_run = models.Run.create(**run)
            print db_run.id
        run_lst = [l for l in db_run.Listeners if l.Name == db_lst.Name]
        if not run_lst:
            db_run.Listeners.add(db_lst)

    print(json.dumps(runs, indent=2))
# ======================================================================


def main():
    models.connect(recreate=False)
    cli = get_cli()
    for listener in settings.SCANS:
        if listener.get('enabled', True):
            process_listener(listener, cli.log)
# ======================================================================

if __name__ == '__main__':
    main()