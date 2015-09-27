#!/bin/env python
import ROOT
ROOT.gROOT.SetBatch(True)

from TrigT1CaloCalibUtils.PlotCalibrationGains import PlotCalibrationGains
from TrigT1CaloCalibUtils.PlotRamps import PlotRamps
from TrigT1CaloCalibUtils.PlotCalibrationTiming import PlotCalibrationTiming
PlotCalibrationGains()
PlotRamps()
PlotCalibrationTiming()
