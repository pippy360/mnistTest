from numpy import genfromtxt
from random import randint

def main():
	filename = "output.txt"
	my_data = genfromtxt(filename, delimiter=',')
	lineIdx = randint(0,len(my_data)-1)
	line = my_data[lineIdx]
	print len(line)
	print displayValue(line)

def displayValue(wholeLineAsArray, cols=28):
	rows = len(wholeLineAsArray)/cols
	ret = "\n\n"
	tempStr = "TRUE. Match found" if wholeLineAsArray[-1] == 1 else "FALSE. No match found"
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
