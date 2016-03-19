#!/usr/bin/env python

import sys
import json
from StringIO import StringIO
from collections import deque

if len(sys.argv) != 2:
        sys.exit('Wrong number of arguments! Expect windowSize')
windowSize = int(sys.argv[1])

myBuffer = deque()

while 1:
	try:
		line = sys.stdin.readline()
	except KeyboardInterrupt:
		break
	if not line:
        	break
	
	pkt = json.load(StringIO(line))

	myBuffer.appendleft(pkt)
	
	if len(myBuffer) >= windowSize:
		print json.dumps(myBuffer.pop())


while len(myBuffer) > 0:
	pkt = myBuffer.pop()
	if pkt["pktType"] != "sample":
		print json.dumps(pkt)
		continue







