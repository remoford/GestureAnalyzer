#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

firstSample = True
beginTime = 0
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

	if firstSample:
		firstSample = False
		beginTime = pkt["timestamp"]
		

	pkt["timestamp"] = pkt["timestamp"] - beginTime
		
	print json.dumps(pkt)





