#!/usr/bin/env python
"""
Tool for finding calibration files in EOS

.. code-block:: bash

    usage: caf_files.py [-h] [-l {ERROR,WARNING,INFO,DEBUG,VERBOSE}]
                        [-p PATHS [PATHS ...]] -r RUN

    Find files in eos by their path

    optional arguments:
      -h, --help            show this help message and exit
      -l {ERROR,WARNING,INFO,DEBUG,VERBOSE}, --log {ERROR,WARNING,INFO,DEBUG,VERBOSE}
                            Logging level
      -p PATHS [PATHS ...], --paths PATHS [PATHS ...]
                            EOS paths
      -r RUN, --run RUN     Run number

Default paths for searching raw files:
    /eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPmtScan
    /eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloEnergyScan
    /eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprDacScanPars
    /eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPedestalRunPars
    /eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPhos4ScanPars

"""
import argparse
import subprocess
import json
import os

DEAFULT_SOURCE = [
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPmtScan/",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloEnergyScan/",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprDacScanPars/",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPedestalRunPars/",
    "/eos/atlas/atlastier0/rucio/data15_calib/calibration_L1CaloPprPhos4ScanPars/",
]

EOS_CMD = '/afs/cern.ch/project/eos/installation/0.3.84-aquamarine/bin/eos.select'


def get_cli():
    parser = argparse.ArgumentParser(description='Find files in eos by their path')
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument('-p', '--paths', nargs='+', help="EOS paths", default=DEAFULT_SOURCE)
    parser.add_argument('-r', '--run',  type=int, help="Run number", required=True)

    return parser.parse_args()


def get_files_by_path(run, eos_path):
    result = []
    lines = ""
    run_path = os.path.join(eos_path, "%08d" % run)
    try:
        FNULL = open(os.devnull, 'w')
        lines = subprocess.check_output([EOS_CMD, 'ls', run_path], stderr=FNULL)
    except subprocess.CalledProcessError:
        pass

    for line in lines.split('\n'):
        if line:
            raw_path = os.path.join(run_path, line)
            files = subprocess.check_output([EOS_CMD, 'ls', raw_path])
            for f in files.split('\n'):
                if f:
                    result.append(os.path.join(raw_path, f))
    return result


def get_files(run, paths=None):
    result = []
    paths = paths if paths else DEAFULT_SOURCE

    for path in paths:
        result += get_files_by_path(run, path)
    return result


def main():
    cli = get_cli()
    result = get_files(cli.run, cli.paths)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
