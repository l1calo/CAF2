get_files -jo COOLIdDump.txt
python {{BASEDIR}}/scripts/RunPlotCalibrationGains.py || (touch error; exit 1)
