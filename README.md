# mpquic-on-scion-ipc
Compilation of my Scion Measurements Scripts


For use, copy the entire PythonTest dir to the SCION AS from which you wish to measure. Then set up the cron job as described below to run the scripts every 5 Minutes. To extract data use the Archive dir where the archived raw data as well as the continually updated csv will be saved. Please do not try to download the data from the working dir /paths as this may interfere with ongoing measurements.


## Motivation and initial Idea

To gather the needed data, we have set up 4 ASes in the SCIONLab environment. These will run as 4 separate Vagrant machines on a Google cloud host machine. The 4 chosen machines are the following:

- 19-ffaa:1:11de 	Lars Herschbach ScionLab 1 	EU 	Magdeburg AP 	VPN:50000
- 17-ffaa:1:11e4 	Lars Herschbach ScionLab 2 	Switzerland 	ETHZ-AP 	VPN:50001
- 18-ffaa:1:11e5 	Lars Herschbach ScionLab 3 	North America 	CMU AP 	VPN:50000
- 22-ffaa:1:11ee 	Lars Herschbach ScionLab 4 	Taiwan 	NTU 	VPN:50000

These were chosen based on the following criteria:
- Geographical diversity
- Accessibility (through the SCIONLab VPN option)
- Stability (or lack thereof in some cases giving us more representative data)
  
All of these machines follow the same setup and are created as vagrant machines attached to their Access Points via VPN to avoid NAT issues. Their geographical diversity allows us to replicate results gathered by related work before us. The instability of some of these ASes allow us to gather more accurate data as opposed to a fully static sandbox environment, while the diversity of ASes should be sufficient, that at least one should always be able to measure.
Each AS will run a suite of python scripts which will gather data to all 3 other ASes. This is done in the following way:

1. Pathdiscover.py discovers paths to the 3 other ASes. These are saved as timestamped json files for further use by the other scripts, analysis down the line and archival purposes.
2. Comparer.py Compares the path availability of inter AS paths between two test instances providing us data on Path Churn as well as full connectivity breakdown (observed in ISD 17).
3. Prober.py will run the adapted “scion ping” command using SCMP to probe path latency as well as packet loss and (if possible) packet sequencing. This data will be saved per path per AS in timestamped json.
4. Wrapper.py will handle the compilation of data from the previous three sources into a csv for later use and analysis
5. Custom Cron Job: will run the 4 scripts in a set interval and handle cleanup of the working directories and updates of the Archive directory from which data may be pulled during testing.
   
This approach gives us both a compiled CSV as well as all the raw data at the and. Through the structure of working and archive directories we are also able to access the already collected data at any point without interfering with the ongoing measurements. This may be used for backup needs.



## Cron Job Setup
To be done

