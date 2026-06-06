import time
from pathlib import Path

LOG_FILE = "Main_Folder/ds/raw_logs/live_syslog.log"

with open(LOG_FILE, "w") as f:
    pass

Path(
    "Main_Folder/ds/raw_logs"
).mkdir(
    parents=True,
    exist_ok=True
)

sample_logs = [

    "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down",

    "%BGP-5-ADJCHANGE: neighbor 192.168.1.1 Down",

    "%OSPF-5-ADJCHG: Process 1, Nbr 10.0.0.2 on GigabitEthernet0/0 from FULL to DOWN",

    "%LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to up",

    "%BGP-5-ADJCHANGE: neighbor 192.168.1.1 Up"
]

print("Starting log stream...")

for log in sample_logs:

    with open(LOG_FILE, "a") as f:

        f.write(log + "\n")

    print(log)

    time.sleep(3)