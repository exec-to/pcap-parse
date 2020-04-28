#!/bin/bash
HOST=192.168.0.105
tcpdump -i enp2s0f1 -nn -vvv  -net host ${HOST}  -w /var/tcpdump/capture-%H-%M-%S.pcap -G 1
