INPUT: .csv file in format of ip_address,snmp_community
OUTPUT: devices_status.csv file with IP Address, Status, Hostname, Vendor/IOS Version, Serial Number

HOW_TO_RUN:
./inventory

NOTE:

Python is not required to run the script.

Source code can be found in 'inventory.py', 'get_snmp.py', and 'ipv4_check.py' files.
