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

	for idx in range(0,8):
		vec = pkt["vectors"][idx]
		print "0\t0\t" + str(vec[0]) + "\t" + str(vec[1])
		
	sumVec = pkt["sumVector"]
	print "0\t0\t" + str(sumVec[0]) + "\t" + str(sumVec[1])





