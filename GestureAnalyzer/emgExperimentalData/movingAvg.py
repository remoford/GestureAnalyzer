#!/usr/bin/env python

import sys
import json
from StringIO import StringIO
#import Queue
from collections import deque

if len(sys.argv) != 4:
        sys.exit('Wrong number of arguments! Expect sourceColumn destColumn windowSize')
sourceColumn = sys.argv[1]
destColumn = sys.argv[2]
windowSize = int(sys.argv[3])

futureDeque = deque()
pastDeque = deque()

def computeAverage(oldQueue, indexStr):
	futureSize = len(futureDeque)
	pastSize = len(pastDeque)
	average = 0
	count = 0

	for idx in range(0, futureSize):
		if indexStr in pkt:
			average += futureDeque[idx][indexStr]
			count += 1

	for idx in range(0, pastSize):
		if indexStr in pkt:
			average += pastDeque[idx][indexStr]
			count += 1
		
	if count == 0:
                return None
	else:
		return average / count
	
def returnAverage(pkt):
	if pkt["pktType"] == "sample":
		pastDeque.appendleft(pkt)
		if len(pastDeque) >= len(futureDeque):
			pastDeque.pop()

		avgValue = computeAverage(futureDeque, sourceColumn)
		if avgValue == None:
			pkt[destColumn] = pkt[sourceColumn]
		else:
			pkt[destColumn] = avgValue

	print json.dumps(pkt)

while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	pkt = json.load(StringIO(line))
	
	futureDeque.appendleft(pkt)
	if len(futureDeque) < windowSize:
		continue
	else:
		returnAverage(futureDeque.pop())

while len(futureDeque) > 0:
	returnAverage(futureDeque.pop())

