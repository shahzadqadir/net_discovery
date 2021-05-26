#!/home/python/venvs/net_disc/bin/python
import os
import platform
from csv import reader
from csv import writer
from csv import DictWriter
import ipv4_check
import get_snmp

class Inventory:

    def __init__(self, input_file):
        self.input_file = input_file

    def check_connectivity(self,host):
        if "Windows" in platform.platform():
            if self.host_chk_win(host):
                return True
            return False
        elif "Linux" in platform.platform():
            if self.host_chk_linux(host):
                return True
            return False
        else:
            print("Sorry, only Windows and Linux are supported.")

    def host_chk_linux(self, host):
        if os.system(f"ping -c 1 -W 2 {host} > /dev/null") == 0:
            return True
        return False

    def host_chk_win(self, host):
        if os.system(f"ping -n 3 -w 999 {host} > null") == 0:
            return True
        return False

    def hosts_with_community(self):
        with open(self.input_file) as file:
            hosts_list = list(reader(file))
        return [{"host":host[0],"community":host[1]} if len(host) > 1 else {"host":host[0], "community":""}
                for host in hosts_list]

    def host_status(self):
        devices = self.hosts_with_community()
        devices_with_status = {}
        for device in devices:
            print(f"Checking host {device['host']}")
            if self.check_connectivity(device['host']):
                devices_with_status[device['host']] = "Live"
            else:
                devices_with_status[device['host']] = "Not live"
        return devices_with_status

while True:
    filename = input("Enter devices file (.csv): ")
    if ipv4_check.IPv4Check.check_file_format(filename):
        inventory = Inventory(filename)
        break
    else:
        print("Only supported files types are text (.txt) or CSV (.csv)")

devices_status = inventory.host_status()
devices_list = inventory.hosts_with_community()
#print(devices_list)
full_inventory = {}
inventory_list = []
for device in devices_list:
    full_inventory["ip_add"]=device['host']
    if inventory.check_connectivity(device['host']):
        full_inventory["status"]="Live"
        if device['community']:
            full_inventory["hostname"] = get_snmp.GetSNMP.get_hostname(device['host'], device['community'])
            full_inventory["vendor"] = get_snmp.GetSNMP.get_version(device['host'], device['community'])
            full_inventory["serial_no"] = get_snmp.GetSNMP.get_serial_no(device['host'], device['community'])
        else:
            full_inventory["hostname"] = "missing snmp"
            full_inventory["vendor"] = "missing snmp"
            full_inventory["serial_no"] = "missing snmp"
    else:
        full_inventory["status"]="Not Live"
    inventory_list.append(full_inventory.copy())

with open("devices_status.csv", "w", newline='') as file:
    fieldnames = ["ip_add", "status", "hostname", "vendor", "serial_no"]
    csv_writer = DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for temp in inventory_list:
        csv_writer.writerow(temp)



#print(inventory_list)
# with open("devices_status.csv", "w", newline='') as file:
#     csv_writer = writer(file)
#     csv_writer.writerow(["hostname", "status"])
#     for device in devices_list:
#         csv_writer.writerow(device)


