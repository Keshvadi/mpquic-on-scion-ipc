# config.py
import os

# AS list adjust with your own AS
AS_FOLDER_MAP = {
    "17-ffaa:0:1108": "MyAS",
}

# Define AS targets and their folder name with IP address
AS_TARGETS = {
    "17-ffaa:0:1108": ("127.0.0.1", "MyAS"),
}

BWTEST_SERVERS = {
}

# Pipeline commands configuration
PIPELINE_COMMANDS = {
    "pathdiscovery": {
        "enabled": True,
        "script": "pathdiscovery.py",
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
        "script": "prober.py",
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
        "script": "traceroute.py",
        "description": "Collect traceroute information",
        "category": "tracing",
        "execution_order": 5
    },
    "bandwidth": {
        "enabled": True,
        "script": "bandwidth.py",
        "description": "Measure bandwidth for all discovered paths",
        "category": "bandwidth",
        "execution_order": 6
    },
    "mp-bandwidth": {
        "enabled": True,
        "script": "mp-bandwidth.py",
        "description": "Multi-path bandwidth measurement",
        "category": "bandwidth",
        "execution_order": 7
    },
}

