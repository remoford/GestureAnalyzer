#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

intervalSum = [0,0,0,0,0,0,0,0]
intervalCount = 0
insideInterval = False
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
		if pkt["pktType"] == "zeroCross":
			if pkt["sign"] == "negative":
				insideInterval = True
				intervalCount = 0
				intervalSum = [0,0,0,0,0,0,0,0]
				beginTime = pkt["timestamp"]
			if pkt["sign"] == "positive":
				insideInterval = False
				if intervalCount == 0:
					continue
				for channel in range(0,8):
					intervalSum[channel] = float(intervalSum[channel]) / intervalCount
				intervalPkt = '{"pktType":"interval","beginTime":'
				intervalPkt += str(beginTime)
				intervalPkt += ',"endTime":'
				intervalPkt += str(pkt["timestamp"])
				intervalPkt += ',"intervalAverage":'+str(intervalSum)+'}'
				print intervalPkt


		print json.dumps(pkt)
		continue

	if insideInterval:
		intervalCount += 1
		for channel in range(0,8):
			intervalSum[channel] += abs(pkt["emg"][channel])

	print json.dumps(pkt)


	lastPkt = pkt


