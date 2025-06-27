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