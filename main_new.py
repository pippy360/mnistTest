import numpy as np
from numpy import genfromtxt
from random import randint
import array_vals as av
import fin_nn as fn


def main():
	lines = loadTheData("train_mixed_numbers_data.csv")
	
	fn.buildTheNN()
	
	for i in range(100):
		line, label = getARandomLine(lines)
		print "label :" + str(label)
		label = fn.does_it_match(line)
		print displayValue(line, label)

def loadTheData(path):
	lines = genfromtxt(path, delimiter=',', skip_header=1, max_rows=100)
	return lines

def getARandomLine(lines):
	lineIdx = randint(0,len(lines))
	line = lines[lineIdx]
	
	#format it as a list
	retLine = []	
	for i in range(len(line)):
		retLine.append(line[i])
	line = retLine

	#get the label
	boolVal = line[-1]
	line.pop()

	return line, boolVal 


def displayValue(wholeLineAsArray, label, cols=28):
	rows = len(wholeLineAsArray)/cols
	ret = ""
	tempStr = "TRUE. Match found" if label else "FALSE. No match found"
	ret = ret + tempStr
	for i in range(rows):
		for j in range(cols):
			idx = (i*cols) + j
			#ret = ret + str(wholeLineAsArray[idx])
			value = '@' if wholeLineAsArray[idx] > 200 else ' '
			ret = ret + value

		ret = ret + "\n"
	return ret

main()
