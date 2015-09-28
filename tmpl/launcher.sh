#!/bin/bash
source /afs/cern.ch/atlas/software/releases/20.1.0/CMT/v1r25/mgr/setup.sh
pwd
ls -lrt

export AtlasSetup=/afs/cern.ch/atlas/software/releases/20.1.0/AtlasSetup
source $AtlasSetup/scripts/asetup.sh {{ASETUP}}

cat jobo.py
ls -lts
athena.py jobo.py

{{POSTEXEC}}
