# config.py
import os

# AS list adjust with your own AS
AS_FOLDER_MAP = {
    "19-ffaa:1:11de": "AS-1",
    "17-ffaa:1:11e4": "AS-2",
    "18-ffaa:1:11e5": "AS-3",
    "22-ffaa:1:11ee": "AS-4",
}

# Define AS targets and their folder name with IP address
AS_TARGETS = {
    "19-ffaa:1:11de": ("127.0.0.1", "AS-1"),
    "17-ffaa:1:11e4": ("127.0.0.1", "AS-2"),
    "18-ffaa:1:11e5": ("127.0.0.1", "AS-3"),
    "22-ffaa:1:11ee": ("127.0.0.1", "AS-4"), 
}

BWTEST_SERVERS = {
    "19-ffaa:0:1303": ("141.44.25.144", "Server-3"),
    "18-ffaa:0:1201": ("128.2.24.126", "Server-5"),
}

# Pipeline commands configuration
PIPELINE_COMMANDS = {
    "pathdiscovery": {
        "enabled": True,
        "script": "pathdiscovery_scion.py",
        "description": "Discover available network paths using SCION",
        "category": "discovery",
        "execution_order": 1
    },
    "comparer": {
        "enabled": True,
        "script": "comparer.py",
        "description": "Compare and analyze discovered paths",
        "category": "analysis",
        "execution_order": 2
    },
    "prober": {
        "enabled": True,
        "script": "prober_scion.py",
        "description": "Basic network connectivity probing",
        "category": "probing",
        "execution_order": 3
    },
    "mp-prober": {
        "enabled": True,
        "script": "mp-prober.py",
        "description": "Multi-path network probing",
        "category": "probing",
        "execution_order": 4
    },
    "traceroute": {
        "enabled": True,
        "script": "tr_collector_scion.py",
        "description": "Collect traceroute information",
        "category": "tracing",
        "execution_order": 5
    },
    "bandwidth": {
        "enabled": True,
        "script": "bw_alldiscover_path.py",
        "description": "Measure bandwidth for all discovered paths",
        "category": "bandwidth",
        "execution_order": 6
    },
    "multipath-bw": {
        "enabled": True,
        "script": "bw_multipath.py",
        "description": "Multi-path bandwidth measurement",
        "category": "bandwidth",
        "execution_order": 7
    },
}

