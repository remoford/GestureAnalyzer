#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 2:
        sys.exit('Wrong number of arguments! Expect sourceColumn')
sourceColumn = sys.argv[1]


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

	pkt[sourceColumn] = int(pkt[sourceColumn])

	print json.dumps(pkt)





