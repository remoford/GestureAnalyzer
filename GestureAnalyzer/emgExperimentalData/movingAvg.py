#!/usr/bin/env python

import sys
import json
from StringIO import StringIO
import Queue

if len(sys.argv) != 4:
        sys.exit('Wrong number of arguments! Expect sourceColumn destColumn windowSize')
sourceColumn = sys.argv[1]
destColumn = sys.argv[2]
windowSize = int(sys.argv[3])

movingAverage = Queue.Queue()

pastQueue = Queue.Queue()


def computeAverage(oldQueue, indexStr):
	newQueue = Queue.Queue()
	#tmpPastQueue = Queue.Queue()
	size = oldQueue.qsize()
	pastSize = pastQueue.qsize()
	average = 0
	averagingCount = 0
	pastAveragingCount = 0
	for idx in range(0, size):
		pkt = oldQueue.get()
		if indexStr in pkt:
			average += pkt[indexStr]
			averagingCount += 1
		oldQueue.put(pkt)

	for idx in range(0, pastSize):
		pkt = pastQueue.get()
		if indexStr in pkt:
			average += pkt[indexStr]
			pastAveragingCount += 1
		pastQueue.put(pkt)


	if (averagingCount + pastAveragingCount) == 0:
                return None
	average = average / (averagingCount + pastAveragingCount)
	return average
	
def returnAverage(pkt):
	if pkt["pktType"] == "sample":

		pastQueue.put(pkt)
		if pastQueue.qsize() >= windowSize:
			pastQueue.get()

		avgValue = computeAverage(movingAverage, sourceColumn)
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
	movingAverage.put(pkt)
	if movingAverage.qsize() < windowSize:
		continue
	else:
		returnAverage(movingAverage.get())

while movingAverage.qsize() > 0:
	returnAverage(movingAverage.get())



	



