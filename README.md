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
scionpathml add-as -a 19-ffaa:1:11de -i 192.168.1.100 -n MyAS  
scionpathml add-server -a 19-ffaa:1:22ef -i 10.0.0.50 -n TestServer  

### View configuration
scionpathml show

## Measurement Control

### Control measurement pipeline
scionpathml show-cmds  
scionpathml enable-cmd -m bandwidth  
scionpathml disable-category -c tracing  

### Schedule automated measurements
scionpathml -f 30  # Run every 30 minutes  

## Data Processing

### Transform JSON measurements to CSV
scionpathml transform  
scionpathml transform-data /path/to/measurements  
scionpathml transform multipath --output-dir /output/  

## Manage datasets
scionpathml data-overview  
scionpathml data-show Archive   
scionpathml data-show Archive --interractive  
scionpathml data-move Archive History  

## Monitoring

## View logs and status
scionpathml logs pipeline  
scionpathml view-log bandwidth latest  
scionpathml transform-status  

## Measurement Types

Path Discovery: scion showpaths coordination  
Latency Testing: scion ping with configurable parameters  
Bandwidth Testing: scion-bwtestclient throughput measurement  
Path Analysis: scion traceroute hop-by-hop latency  
Multipath Testing: mp-prober and mp-bandwidth for concurrent measurements  
Path Comparison: Historical path availability tracking  


## Data Organization

Data/  
├── Archive/     # Archive measurement data  
├── Currently/   # Current measurement data  
├── History/     # Preivous measurement data  
└── Logs/        # Execution and error logs  


## License
MIT License


## CSV to DataFrame Guide

If necessary, you can also convert your CSV file to a DataFrame. Here is some documentation to help you do this:

### Prerequisites

Ensure you have Python and the pandas library installed. You can install pandas via pip if necessary:

```bash
pip install pandas
```
### Example Code

```python
import pandas as pd

# Load data from CSV into a DataFrame
df = pd.read_csv('your_file.csv')
print(df.head())
```


