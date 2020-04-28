#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import config
import dpkt
import socket
import database
from sqlalchemy.orm import sessionmaker
import glob


class Counter(object):
    def __init__(self, port, packet_len):
        self.port = port
        self.packets = 1
        self.bytes = packet_len

    def increment(self, packet_len):
        self.packets += 1
        self.bytes += packet_len


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


db = database.Db()
session = sessionmaker(bind=db.engine)()
fcount = 0

for pcap_file in glob.glob("{base}/*.pcap".format(base=config.default['PCAP_PATH'])):
    fcount += 1
    print('Processing file #{n} {f}'.format(n=fcount, f=pcap_file))

    with open(pcap_file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)

        counters = []

        for ts, buf in pcap:
            eth = dpkt.ethernet.Ethernet(buf)

            if not isinstance(eth.data, dpkt.ip.IP):
                continue

            ip = eth.data
            proto = ip.data
            curr_dst = inet_to_str(ip.dst)

            if hasattr(proto, 'dport') and curr_dst == config.dst_target:

                counter = next((x for x in counters if x.port == proto.dport), None)
                if counter:
                    counter.increment(len(buf))
                else:
                    counter = Counter(proto.dport, len(buf))
                    counters.append(counter)

        for counter in counters:
            incoming = database.Incoming(config.dst_target, counter.port, counter.packets, counter.bytes)
            session.add(incoming)

        session.commit()
