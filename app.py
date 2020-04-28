#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import config
import dpkt

pcap_file = '{base}/capture-00-00-00.pcap'.format(base=config.default['PCAP_PATH'])

f = open(pcap_file)
pcap = dpkt.pcap.Reader(f)

for ts, buf in pcap:
 eth = dpkt.ethernet.Ethernet(buf)
 ip = eth.data
 udp = ip.data

 if udp.dport == 27016 and len(udp.data) > 0:
     print(udp)

f.close()