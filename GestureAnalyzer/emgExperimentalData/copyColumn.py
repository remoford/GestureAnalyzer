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
	
	if pkt["pktType"] != "sample":
		print json.dumps(pkt)
		continue

	label = ""
	for channel in range(0,8):
		label = "emg" + str(channel)
		pkt[label] = abs(pkt["emg"][channel])


	print json.dumps(pkt)




