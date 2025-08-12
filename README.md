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

1. pathdiscover_scion.py discovers paths to the 3 other ASes. These are saved as timestamped json files for further use by the other scripts, analysis down the line and archival purposes.
2. comparer.py Compares the path availability of inter AS paths between two test instances providing us data on Path Churn as well as full connectivity breakdown (observed in ISD 17).
3. prober.py will run the adapted “scion ping” command using SCMP to probe path latency as well as packet loss and (if possible) packet sequencing. This data will be saved per path per AS in timestamped json.
4. traceroute.py runs the adapted “scion traceroute” command using SCMP to probe the AS-level hops (hop count), RTT and path structure. The results are saved per path per AS in timestamped JSON files.
5. bw_collector_scion.py performs automated bandwidth testing from the local AS to 4 remote ASes over all available SCION paths, using predefined target rates (1–250 Mbps). For each direction (client-to-server and server-to-client), it collects detailed performance metrics including attempted and achieved throughput, packet loss percentage, and interarrival time (min/avg/max/mdev). Results are saved in timestamped JSON files for later analysis and benchmarking.
6. Wrapper.py will handle the compilation of data from the previous three sources into a csv for later use and analysis
7. Custom Cron Job: will run the 4 scripts in a set interval and handle cleanup of the working directories and updates of the Archive directory from which data may be pulled during testing.
   
This approach gives us both a compiled CSV as well as all the raw data at the and. Through the structure of working and archive directories we are also able to access the already collected data at any point without interfering with the ongoing measurements. This may be used for backup needs.



## Cron Job Setup
1. To create the cronjob. Make sure that the repo is at /home/vagrant.

2. Run the command crontab -e and select you text editior

3. Paste the following entry:
```
SHELL=/bin/bash
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
*/5 * * * * /home/vagrant/mpquic-on-scion-ipc/Scripts/pipeline.sh
```

Change number of bandwidth tests at this time : Mon Jul 14 17:24:14 UTC 2025 on Scion Machine