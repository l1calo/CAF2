#!/usr/bin/env python

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
    parser.add_argument('-r', '--runs', nargs='+', type=int, help="Run number(s)", required=True)

    return parser.parse_args()


def get_files(run, eos_path):
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


def main():
    cli = get_cli()
    result = []
    for run in cli.runs:
        for path in cli.paths:
            result += get_files(run, path)

    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
