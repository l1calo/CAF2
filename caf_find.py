#!/usr/bin/env python
"""
Find calibration runs by the specified conditions
"""
import logging
import argparse
import json
import sys

try:
    from PyCool import cool
except ImportError:
    sys.stderr.write("Please run asetup before running the tool (any configuration)\n")
    sys.exit(-1)

from CoolConvUtilities import AtlCoolLib

# =============================================================================
# Setup logger
# =============================================================================
logger = logging.getLogger("caf-find")
console = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
# =============================================================================


def get_cli():
    parser = argparse.ArgumentParser(description='Find runs by the certain creteria')
    parser.add_argument('-l', '--log',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG', 'VERBOSE'],
                        help="Logging level", default='ERROR')
    parser.add_argument('--runtype', help="Run type", default='cismono')
    parser.add_argument('-p', '--partitions', help="Paritition names", nargs='+',
                        default=['TileL1CaloCombined'])
    parser.add_argument('--recenabled', type=bool, help="Recording enabled?", default=True)
    parser.add_argument('--cleanstop', type=bool, help="Clean stop", default=True)
    parser.add_argument('-r', "--run", type=int, help="Run number to start from",
                        default=266000, required=True)

    return parser.parse_args()
# =============================================================================


def payload_to_dict(payload):
    result = {}
    for p in payload:
        result[p] = payload[p]
    return result
# =============================================================================


class Selector(object):
    coolpath = '/TDAQ/RunCtrl'
    cooltlbpath = '/TRIGGER/LUMI'
    cooll1calopath = '/TRIGGER/L1Calo/V1/Conditions'
    coolstrategypath = '/TRIGGER/Receivers/Conditions'

    def __init__(self, cool_tdaq, cool_trig, oracle=False):
        self.filter = {}
        try:
            self.cool_tdaq = AtlCoolLib.indirectOpen(
                cool_tdaq, True, oracle, debug=False
            )
            self.cool_trig = AtlCoolLib.indirectOpen(
                cool_trig, True, oracle, debug=False
            )
        except Exception:
            logger.exception("Could not open cool database")
            return
        logger.info("Connected to {0}".format(cool_tdaq))

        self.mintime = cool.ValidityKeyMin
        self.maxtime = cool.ValidityKeyMax

    def _filter_by_sor(self, payload):
        res = True
        if "RunType" in self.filter:
            res = payload["RunType"] == self.filter["RunType"]
        if "RecordingEnabled" in self.filter:
            res &= (
                self.filter["RecordingEnabled"] == payload["RecordingEnabled"]
            )
        return res

    def _filter(self, payload):
        for name, value in self.filter.iteritems():
            special_index = name.find('__')
            if special_index > 0:
                payload_name = name[:special_index]
            else:
                payload_name = name
            if payload_name not in payload:
                return False

            if value:
                if name.endswith('__gt'):
                    if payload[payload_name] < value:
                        return False
                    continue

                if name.endswith('__in'):
                    if payload[payload_name] not in value:
                        return False
                    continue

                if payload[payload_name] != value:
                    return False

        return True

    def set_selection(self, **argw):
        self.filter = argw

    def runs_by_range(self, run1=0, run2=(1 << 31) - 1):
        """Query /TDAQ/RunCtrl/LB_Params to get details of runs in runrange
        Use both SOR_Params and EOR_Params to catch runs which ended badly.
        Return a map of runs to RunParams objects"""
        # get detector status information if needed

        runlist = {}

        # =====================================================================
        # SOR
        # =====================================================================
        nsor = 0
        # nsor_filtered = 0

        folder_sor = self.cool_tdaq.getFolder(Selector.coolpath + '/SOR')

        itr = folder_sor.browseObjects(
            (run1 << 32),
            (run2 << 32),
            cool.ChannelSelection.all()
        )

        while itr.goToNext():
            nsor += 1
            payload = itr.currentRef().payload()
            run = payload['RunNumber']
            if self._filter_by_sor(payload):
                runlist[run] = payload_to_dict(payload)

        itr.close()
        if not runlist:
            return runlist
        # =====================================================================
        # EOR
        # =====================================================================
        # now query EOR and fill in missing info
        neor = 0
        # neor_filtered = 0
        folder_eor = self.cool_tdaq.getFolder(Selector.coolpath + '/EOR')
        itr = folder_eor.browseObjects(
            min(runlist.keys()) << 32,
            max(runlist.keys()) << 32,
            cool.ChannelSelection.all()
        )
        while itr.goToNext():
            payload = itr.currentRef().payload()
            run = payload['RunNumber']
            if run in runlist:
                runlist[run].update(payload_to_dict(payload))
                neor += 1

        # logging.info("EOR has data for %i runs" % neor)
        itr.close()
        # =====================================================================
        # EventCounters
        # =====================================================================
        # nevc = 0
        # nevc_filtered = 0

        folder_counters = self.cool_tdaq.getFolder(
            Selector.coolpath + '/EventCounters')
        itr = folder_counters.browseObjects(
            min(runlist.keys()) << 32,
            max(runlist.keys()) << 32,
            cool.ChannelSelection.all()
        )

        while itr.goToNext():
            obj = itr.currentRef()
            payload = obj.payload()
            run = obj.since() >> 32
            if run in runlist:
                runlist[run].update(payload_to_dict(payload))
        itr.close()

        # =====================================================================
        # Gain strategy
        # =====================================================================
        gain_list = list()
        folder_gains = self.cool_trig.getFolder(
            '{}/Strategy'.format(self.coolstrategypath)
        )
        itr = folder_gains.browseObjects(self.mintime, self.maxtime,
                                         cool.ChannelSelection(0, 1))
        current = -1
        while itr.goToNext():
            obj = itr.currentRef()
            if obj.since() != current:
                gain_list.append(
                    {
                        'since': obj.since(),
                        'until': obj.until(),
                        'payload': obj.payload()['name']
                    }
                )
                current = obj.since()
        # logging.info("Gain list %s" % str(gain_list))
        # =====================================================================
        # logging.info("Runs before selection:  %i" % len(runlist))
        for run in list(runlist.iterkeys()):
            if not self._filter(runlist[run]):
                del runlist[run]
            else:
                for gain in sorted(gain_list):
                    if gain['since'] <= runlist[run]['SORTime'] <= gain['until']:
                        runlist[run]['GainStrategy'] = gain['payload']

        # logging.info("Runs after selection:  %i" % len(runlist))
        # =====================================================================
        return runlist


def get_runs(run, loglevel, runtype, partitions, recenabled, cleanstop, minevents):
    logger.setLevel(getattr(logging, loglevel))
    # =========================================================================
    # Setup runs selector
    # =========================================================================
    # TODO(sasha): convert to the function with one call to runs_by_range
    selector = Selector("COOLONL_TDAQ/CONDBR2", "COOLONL_TRIGGER/CONDBR2")
    selector.set_selection(
        RunType=runtype,
        PartitionName__in=partitions,
        RecordingEnabled=recenabled,
        CleanStop=cleanstop,
        RecordedEvents__gt=minevents
    )
    # =========================================================================
    runs = selector.runs_by_range(run1=run)
    result = []
    for key in sorted(runs.iterkeys()):
        result.append(runs[key])
    return result


def main():
    # Get command line parameters
    cli = get_cli()
    runs = get_runs(run=cli.run, loglevel=cli.log, runtype=cli.runtype, partitions=cli.partitions,
                    recenabled=cli.recenabled, cleanstop=cli.cleanstop, nrecords=0
                    )
    # =========================================================================
    print(json.dumps(runs, indent=2))

if __name__ == '__main__':
    main()
