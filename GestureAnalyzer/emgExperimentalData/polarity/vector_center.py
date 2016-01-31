#!/usr/bin/env python
import csv
import sys
import math

myTable=[]
myTableStr=[]

#Read file as csv
with open(sys.argv[1], 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
                 myTableStr+=[ row  ]

#convert strings to ints
for row in myTableStr:
        newRow = []
        for col in row:
                newRow += [float(col)]
        myTable += [newRow]


for row in myTable:
	x1 = 0.0 * row[0]
	y1 = 1.0 * row[0]

	x2 = 0.707 * row[1]
	y2 = 0.707 * row[1]

	x3 = 1.0 * row[2]
	y3 = 0.0 * row[2]

	x4 = 0.707 * row[3]
	y4 = -0.707 * row[3]

	x5 = 0.0 * row[4]
	y5 = -1.0 * row[4]

	x6 = -0.707 * row[5]
	y6 = -0.707 * row[5]

	x7 = -1.0 * row[6]
	y7 = 0.0 * row[6]

	x8 = -0.707 * row[7]
	y8 = 0.707 * row[7]

	xTotal = x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8
	yTotal = y1 + y2 + y3 + y4 + y5 + y6 + y7 + y8

	magnitude = math.sqrt(xTotal**2 + yTotal**2)

	print magnitude









