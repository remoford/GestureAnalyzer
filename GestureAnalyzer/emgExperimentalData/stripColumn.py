#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 2:
        sys.exit('Wrong number of arguments! Expect targetColumn')
targetColumn = sys.argv[1]

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


	if targetColumn in pkt: del pkt[targetColumn]

	print json.dumps(pkt)





