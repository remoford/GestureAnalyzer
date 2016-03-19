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
	
	if pkt["pktType"] != "interval":
		continue

	sumVec = pkt["sumVector"]
	print "0\t0\t" + str(sumVec[0]) + "\t" + str(sumVec[1])





