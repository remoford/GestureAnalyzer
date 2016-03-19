#!/usr/bin/env python

import sys
import json
from StringIO import StringIO

if len(sys.argv) != 3:
        sys.exit('Wrong number of arguments! Expect XRANGE')
x_range = int(sys.argv[1])
sourceColumn = sys.argv[2]


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

	if (pkt["sourceColumn"] != sourceColumn) and (pkt["sourceColumn"] != (sourceColumn + "_derivitive")) and (pkt["sourceColumn"] != (sourceColumn + "_derivitive2nd")):
		continue


	rectLine = "set obj rect from graph "
	rectLine += str(float(pkt["beginTime"]) / x_range)
	rectLine += ",graph 0 to graph "
	rectLine += str(float(pkt["endTime"]) / x_range) + ", graph 1"

	print rectLine
