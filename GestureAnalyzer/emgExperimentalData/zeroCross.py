#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 2:
        sys.exit('Wrong number of arguments! Expect sourceColumn')
sourceColumn = sys.argv[1]



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
		lastPkt = pkt
		print json.dumps(pkt)
		continue
	
	if (lastPkt[sourceColumn] > 0) and (pkt[sourceColumn] <= 0):
		zeroCrossPkt = '{"pktType":"zeroCross","timestamp":'
		zeroCrossPkt += str(pkt["timestamp"])
		zeroCrossPkt += ',"sign":"negative","sourceColumn":"'
		zeroCrossPkt += str(sourceColumn)
		zeroCrossPkt += '"}'
		print zeroCrossPkt
	if (lastPkt[sourceColumn] <= 0) and (pkt[sourceColumn] > 0):
		zeroCrossPkt = '{"pktType":"zeroCross","timestamp":'
		zeroCrossPkt += str(pkt["timestamp"])
		zeroCrossPkt += ',"sign":"positive","sourceColumn":"'
		zeroCrossPkt += str(sourceColumn)
		zeroCrossPkt += '"}'
		print zeroCrossPkt

	print json.dumps(pkt)


	lastPkt = pkt


