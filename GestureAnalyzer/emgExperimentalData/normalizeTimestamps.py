#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

oddPkt = {}
prevPkt = {}
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

	if pkt["seqNum"] == 0:
		print json.dumps(pkt)
		prevPkt = pkt
		continue

	if pkt["seqNum"]%2 == 1:
		oddPkt = pkt
	else:
		difference = pkt["timestamp"] - prevPkt["timestamp"]
		oddPkt["timestamp"] = prevPkt["timestamp"] + difference/2
		prevPkt = pkt
		print json.dumps(oddPkt)
		print json.dumps(pkt)
	







