"""
CAF configuration:
* Calibration runs' search paramaters
* Calibration analysis' configuration

Example:

Search parameters

.. code-block:: python

    SCANS = [
        {
            "name": "TileEnergyScan",
            "runtype": "cismono",
            "daqpartitions": [
                "L1CaloCombined",
                "TileL1CaloCombined"
            ],
            "minevents": 1700,
            "initialrun": 272549,
            "enabled": True
        }
    ]

Analysis configuration:

.. code-block:: python

    ANALYSIS = [
        {
            "name": "TileRampMaker",
            "file": "RampMaker.py",
            "postexec": "RunPlotCalibrationGains.sh"
        }
    ]
"""

SCANS = [
    {
        "name": "TileEnergyScan",
        "runtype": "cismono",
        "daqpartitions": [
            "L1CaloCombined",
            "TileL1CaloCombined"
        ],
        "minevents": 1700,
        "initialrun": 272549,
        "enabled": True
    },
    {
        "name": "LArEnergyScan",
        "runtype": "LarCalibL1Calo",
        "daqpartitions": [
            "L1CaloCombined",
            "LArgL1CaloCombined"
        ],
        "minevents": 1700,
        "initialrun": 272549,
        "enabled": True
    }
]

ANALYSIS = [
    {
        "name": "TileRampMaker",
        "file": "RampMaker.py",
        "postexec": "RunPlotCalibrationGains.sh"
    }
]
