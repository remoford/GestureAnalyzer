#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

firstSample = True
presentKeys = []
while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	
	pkt = json.load(StringIO(line))
	
	if pkt["pktType"] != "sample":
		continue

	if firstSample:
		firstSample = False
		presentKeys += list(pkt.keys())
		presentKeys.remove("timestamp")
		presentKeys = ["timestamp"] + presentKeys
		headerStr = "#  "
		for key in presentKeys:
			if key == "pktType":
				continue
			if key == "emg":
				for channel in range(0,8):
					headerStr += "emg" + str(channel) + "\t"
			else:
				headerStr += key + "\t"
		print headerStr

	dataStr = ""
	for key in presentKeys:
		if key == "pktType":
			continue
		if key == "emg":
			for channel in range(0,8):
				dataStr += str(pkt["emg"][channel]) + "\t"

		else:
			dataStr += str(pkt[key]) + "\t"
	print dataStr







