#!/usr/bin/env python

import sys
import os.path
import re

if len(sys.argv) != 2:
	sys.exit('Wrong number of arguments!')

try:
	fh = open(sys.argv[1])
except IOError as e:
	print("({})".format(e))
	sys.exit()


lines = fh.readlines()

beginTime = ""
beginTimeInstances = 0
endTime = ""
endTimeInstances = 0
for index in range(0, len(lines)):
	if re.match("^Starting time:", lines[index]):
		beginTimeInstances += 1
		beginTime = lines[index].split(':')[1].rstrip()
	if re.match("^Ending time:", lines[index]):
		endTimeInstances += 1
		endTime = lines[index].split(':')[1].rstrip()

if beginTimeInstances != 1 or endTimeInstances != 1:
	sys.exit('Did not find one and ONLY one header in file!')

emgPkts = []
for index in range(0, len(lines)):
	splitLine = lines[index].split(',')
	pktStr = ""
	if len(splitLine) == 9:
		pktStr = '{"pktType":"sample","timestamp":'
		pktStr += splitLine[0]
		pktStr += ',"emg":['
		pktStr += splitLine[1]
		for emgIdx in range(2,9):
			pktStr += ',' + splitLine[emgIdx].rstrip()
		pktStr += ']}\n'
		emgPkts += [pktStr]

headerPkt = '{"pktType":"header","beginTime":'
headerPkt += beginTime
headerPkt += '}\n'

footerPkt = '{"pktType":"footer","endTime":'
footerPkt += endTime
footerPkt += '}\n'

fileName = sys.argv[1]
fileName = fileName.replace('./','')
fileName = fileName.replace('/','_')
fileName = fileName.replace('.txt.csv','.spfmt')


outFile = open(fileName, 'w')
outFile.truncate()

outFile.write(headerPkt)
for pktStr in emgPkts:
	outFile.write(pktStr)
outFile.write(footerPkt)


