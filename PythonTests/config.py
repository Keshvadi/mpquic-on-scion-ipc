# config.py
import os

# AS list adjust with your own AS
AS_FOLDER_MAP = {
    "19-ffaa:1:11de": "AS-1",
    "17-ffaa:1:11e4": "AS-2",
    "18-ffaa:1:11e5": "AS-3",
    "22-ffaa:1:11ee": "AS-4",
    "17-ffaa:0:1095": "AS-12",
    "17-ffaa:120:1212": "madsd",
    "17-ffaa:120:1215": "MA",
}

# Define AS targets and their folder name with IP address
AS_TARGETS = {
    "19-ffaa:1:11de": ("127.0.0.1", "AS-1"),
    "17-ffaa:1:11e4": ("127.0.0.1", "AS-2"),
    "18-ffaa:1:11e5": ("127.0.0.1", "AS-3"),
    "22-ffaa:1:11ee": ("127.0.0.1", "AS-4"),  
    "17-ffaa:0:1095": ("127.0.0.1", "AS-12"),
    "17-ffaa:120:1212": ("127.0.0.1", "madsd"),
    "17-ffaa:120:1215": ("127.0.0.1", "MA"),
}

BWTEST_SERVERS = {
    "19-ffaa:0:1303": ("141.44.25.144", "Server-3"),
    "18-ffaa:0:1201": ("128.2.24.126", "Server-5"),
    "12-ffaa:098:153a": ("127.0.0.1", "TEST-S"),
}