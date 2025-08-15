# Measurement Results

This directory contains the results of our four-week measurement campaign in SCIONLab.  
It is organized into three folders, each corresponding to one of the three labs where the measurement suite was deployed. In each case, the other two labs served as targets.  

Each lab folder contains:  
- **Data/** – the raw measurement data, organized by the day it was collected.  
- **Analysis/** – the processed results, including `.txt` files with analysis summaries and subfolders containing the generated graphs.  

---

## Disclaimer on Data

Due to unforeseen changes in our testing suite during the measurement period, data collected between **July 11** and **July 16** is **not directly comparable** to the data gathered from **July 16** onward.  

Changes during this period included:  
- Fixing a file-naming issue.  
- Reducing the number of paths tested in both bandwidth and ping measurements.  
- Other internal adjustments to the measurement process.  

Although this earlier data is still valuable—capturing, for example, the novel *path discrepancy phenomenon*—it should be analyzed separately and not combined with the “clean” dataset collected after July 16.  

All pre-done analysis in this repository was conducted using data from **July 16** onward.
