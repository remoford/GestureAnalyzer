#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

yMin = 0
yMax = 0
while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	
	pkt = json.load(StringIO(line))
	
	if pkt["pktType"] == "footer":
		pkt["yMin"] = yMin
		pkt["yMax"] = yMax
		print json.dumps(pkt)
		continue

	if pkt["pktType"] != "sample":
		print json.dumps(pkt)
		continue


	for channel in range(0,8):
		curVal = pkt["emg"][channel]
		if curVal > yMax:
			yMax = curVal
		if curVal < yMin:
			yMin = curVal

	print json.dumps(pkt)





