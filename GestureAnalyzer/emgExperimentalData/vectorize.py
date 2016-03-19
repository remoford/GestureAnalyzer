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
		print json.dumps(pkt)
		continue

	diag = 0.7071

	# according to https://developer.thalmic.com/forums/topic/1641/?page=1#post-7056
	#    4
	#  5   3
	#6       2
	#  7   1
	#    8

	pkt["vectors"] = []
	for idx in range(0,8):
		mag = pkt["intervalAverage"][idx]
		if idx == 0: # Channel 1
			pkt["vectors"] += [[diag*mag,0-diag*mag]]
		if idx == 1: # Channel 2
			pkt["vectors"] += [[0,mag]]
		if idx == 2: # Channel 3
			pkt["vectors"] += [[diag*mag,diag*mag]]
		if idx == 3: # Channel 4
			pkt["vectors"] += [[mag, 0]]
		if idx == 4: # Channel 5
			pkt["vectors"] += [[0-diag*mag, diag*mag]]
		if idx == 5: # Channel 6
			pkt["vectors"] += [[0-mag,0]]
		if idx == 6: # Channel 7
			pkt["vectors"] += [[0-diag*mag,0-diag*mag]]
		if idx == 7: # Channel 8
			pkt["vectors"] += [[0,0-mag]]

	sumVec = [0,0]
	for idx in range(0,8):
		sumVec[0] += pkt["vectors"][idx][0]
		sumVec[1] += pkt["vectors"][idx][1]
	
	sumVec[0] = sumVec[0] / 8
	sumVec[1] = sumVec[1] / 8

	pkt["sumVector"] = sumVec

	print json.dumps(pkt)





