#!/usr/bin/python

import nmap

nm= nmap.PortScanner()
nm.scan(hosts='172.22.0.0/24', arguments='-p U:161')

print nm.command_line()

hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

resultFile = open('scanResult.txt', 'w')

for host, status in hosts_list:
	resultFile.write(host+" "+status+"\n")

resultFile.close()

