#!/usr/bin/env python
import csv
import Queue
import sys

myTableStr = []
myTable = []
movingAverage = Queue.Queue()
movingAverageWindow = 50
movingAverage2 = Queue.Queue()
movingAverageWindow2 = 100

for i in range(movingAverageWindow):
	movingAverage.put(0)

for i in range(movingAverageWindow2):
	movingAverage2.put(0)


#Read file as csv
with open(sys.argv[1], 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
	for row in spamreader:
		 myTableStr+=[ row  ]

#convert strings to ints
for row in myTableStr:
	newRow = []
	for col in row:
		newRow += [int(col)]
	myTable += [newRow]

for row in myTable:
	total = 0
	for col in row[1:]:
		total += abs(col)
	row += [total]

count = 0
for row in myTable:
	currentAverage = 0
	
	movingAverage.put(row[10])	

	if movingAverage.qsize() > movingAverageWindow:
		movingAverage.get()

	for i in range(movingAverage.qsize()):
		temp = movingAverage.get()
		currentAverage += temp
		movingAverage.put(temp)
	
	currentAverage = currentAverage / movingAverage.qsize()


        lookBehindIndex = count - ( movingAverageWindow / 2 )

        if lookBehindIndex >= 0:
                myTable[lookBehindIndex] += [currentAverage]

        count += 1


lookBehindFixupIndex =  movingAverageWindow / 2
for row in myTable[-lookBehindFixupIndex:]:
        row += [0]


	
previous = 0
for row in myTable:
	difference = row[11] - previous
	row += [difference]
	previous = row[11]


count = 0
for row in myTable:
        currentAverage = 0.0



        movingAverage2.put(row[12])

        if movingAverage2.qsize() > movingAverageWindow2:
                movingAverage2.get()

        for i in range(movingAverage2.qsize()):
                temp = movingAverage2.get()
                currentAverage += temp
                movingAverage2.put(temp)

        currentAverage = currentAverage / movingAverage2.qsize()


	lookBehindIndex = count - ( movingAverageWindow2 / 2 )

	if lookBehindIndex >= 0:
        	myTable[lookBehindIndex] += [currentAverage*100]

	count += 1


lookBehindFixupIndex =  movingAverageWindow2 / 2
for row in myTable[-lookBehindFixupIndex:]:
	row += [0]



count = 0
for row in myTable:
        count+=1
        row[0] = count

maxDerivitive = 0
maxDerivitiveIndex = 0
minDerivitive = 0
maxDerivitiveIndex = 0
count = 0
for row in myTable:
	if row[13] > maxDerivitive:
		maxDerivitive = row[13]
		maxDerivitiveIndex = count
	if row[13] < minDerivitive:
		minDerivitive = row[13]
		minDerivitiveIndex = count
	count+=1



count = 0
for row in myTable[maxDerivitiveIndex:minDerivitiveIndex]:
	print count,
	for col in row[1:]:
		print ',' + str(abs(col)),
	print

	count += 1
