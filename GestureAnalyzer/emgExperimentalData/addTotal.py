#!/usr/bin/env python

import sys
import json
from StringIO import StringIO


while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	
	pkt = json.load(StringIO(line))
	
	if pkt["pktType"] != "sample":
		print json.dumps(pkt)
		continue

	total = 0
	for channel in pkt["emg"]:
		total += abs(channel)
	total = total

	pkt["totalPower"] = total

	print json.dumps(pkt)





