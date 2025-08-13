# ScionPathML

A Python toolkit for SCION network measurement and machine learning dataset generation.

## Overview

ScionPathML provides a command-line interface for systematic SCION network measurement campaigns and data processing. The toolkit coordinates SCION's native measurement tools (`scion ping`, `scion-bwtestclient`, `scion traceroute`, `scion showpaths`) through automated scheduling and converts raw measurement outputs to analysis-ready CSV datasets.

## Installation

```bash
git clone https://github.com/Keshvadi/mpquic-on-scion-ipc.git
cd installation-folder/mpquic-on-scion-ipc
pip install -e .
```
## Prerequisites
- Python 3.8+ 
- SCION infrastructure access (SCIONLab and active AS)
- SCION measurement tools for bandwidth: `sudo apt install scion-apps-bwtester`

## Network Configuration 

### Configure autonomous systems
scionpathml add-as -a 19-ffaa:1:11de -i 192.168.1.100 -n MyAS< br / >
scionpathml add-server -a 19-ffaa:1:22ef -i 10.0.0.50 -n TestServer< br / >

### View configuration
scionpathml show

## Measurement Control

### Control measurement pipeline
scionpathml show-cmds< br / >
scionpathml enable-cmd -m bandwidth< br / >
scionpathml disable-category -c tracing< br / >

### Schedule automated measurements
scionpathml -f 30  # Run every 30 minutes

## Data Processing

### Transform JSON measurements to CSV
scionpathml transform< br / >
scionpathml transform-data /path/to/measurements< br / >
scionpathml transform multipath --output-dir /output/< br / >

## Manage datasets
scionpathml data-overview< br / >
scionpathml data-show Archive< br / >
scionpathml data-show Archive --interractive< br / >
scionpathml data-move Archive History< br / >

## Monitoring

### View logs and status
scionpathml logs pipeline< br / >
scionpathml view-log bandwidth latest< br / >
scionpathml transform-status< br / >

## Measurement Types

Path Discovery: scion showpaths coordination< br / >
Latency Testing: scion ping with configurable parameters< br / >
Bandwidth Testing: scion-bwtestclient throughput measurement< br / >
Path Analysis: scion traceroute hop-by-hop latency< br / >
Multipath Testing: mp-prober and mp-bandwidth for concurrent measurements< br / >
Path Comparison: Historical path availability tracking< br / >


## Data Organization

Data/
├── Archive/     # Archive measurement data< br / >
├── Currently/   # Current measurement data< br / >
├── History/     # Preivous measurement data< br / >
└── Logs/        # Execution and error logs< br / >


## License
MIT License
