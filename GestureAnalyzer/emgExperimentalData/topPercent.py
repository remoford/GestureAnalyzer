#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

factor = 0.5

pkts = []
highestPwr = 0
highestIntegral = 0
while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	
	pkt = json.load(StringIO(line))
	
	if pkt["pktType"] != "interval":
		continue

	pwr = pkt["totalPwr"]
	integral = pwr * (pkt["endTime"] - pkt["beginTime"])
	pkts += [pkt]
	if pwr > highestPwr:
		highestPwr = pwr
	if integral > highestIntegral:
		highestIntegral = integral

for pkt in pkts:
	integral = pkt["totalPwr"] * (pkt["endTime"] - pkt["beginTime"])
	pkt["integral"] = integral
	if (integral >= highestIntegral*factor) and (pkt["totalPwr"] >= highestPwr*factor):
		print json.dumps(pkt)






