#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 3:
        sys.exit('Wrong number of arguments! Expect thresholdPwr sourceColumn')
thresholdPwr = int(sys.argv[1])
sourceColumn = sys.argv[2]

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
			if pkt["sourceColumn"] == sourceColumn:
				if pkt["sign"] == "negative":
					insideInterval = True
					intervalCount = 0
					intervalSum = [0,0,0,0,0,0,0,0]
					beginTime = pkt["timestamp"]
				if pkt["sign"] == "positive":
					insideInterval = False
					if intervalCount == 0:
						continue
					totalPwr = 0
					for channel in range(0,8):
						intervalSum[channel] = float(intervalSum[channel]) / intervalCount
						totalPwr += intervalSum[channel]
					intervalPkt = '{"pktType":"interval","beginTime":'
					intervalPkt += str(beginTime)
					intervalPkt += ',"endTime":'
					intervalPkt += str(pkt["timestamp"])
					intervalPkt += ',"intervalAverage":'
					intervalPkt += str(intervalSum)
					intervalPkt += ',"totalPwr":'
					intervalPkt += str(totalPwr)
					intervalPkt += ',"sourceColumn":"'
					intervalPkt += sourceColumn
					intervalPkt += '"}'
					if thresholdPwr < totalPwr:
						print intervalPkt


		print json.dumps(pkt)
		continue

	if insideInterval:
		intervalCount += 1
		for channel in range(0,8):
			intervalSum[channel] += abs(pkt["emg"][channel])

	print json.dumps(pkt)


	lastPkt = pkt


