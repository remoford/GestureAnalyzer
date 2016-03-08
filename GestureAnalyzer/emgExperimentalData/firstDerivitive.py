#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 4:
        sys.exit('Wrong number of arguments! Expect sourceColumn destColumn scaleFactor')
sourceColumn = sys.argv[1]
destColumn = sys.argv[2]
scaleFactor = float(sys.argv[3])



lastPkt = {}
firstSample = True
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
		pkt[destColumn] = 0
		lastPkt = pkt
		continue
	

	
	run = float(int(pkt["timestamp"]) - int(lastPkt["timestamp"])) + 0.00001

	rise = float(int(pkt[sourceColumn]) - int(lastPkt[sourceColumn])) * scaleFactor


	pkt[destColumn] = rise / run

	print json.dumps(pkt)


	lastPkt = pkt


