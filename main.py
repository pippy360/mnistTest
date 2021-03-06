import os
import struct
from array import array
from random import randint

def start(path='./data'):

	test_img_fname = 't10k-images-idx3-ubyte'
	test_lbl_fname = 't10k-labels-idx1-ubyte'

#	test_img_fname = 'img_1'
#	test_lbl_fname = 'label_1'

	train_img_fname = 'train-images-idx3-ubyte'
	train_lbl_fname = 'train-labels-idx1-ubyte'

	org_test_images = []
	org_test_labels = []

	org_train_images = []
	org_train_labels = []

	org_test_images, org_test_labels = load_wrapper(path, train_img_fname, train_lbl_fname)	
	org_test_images, org_test_labels = mixThem_random(org_test_images, org_test_labels, validInts=[0,1,2,3,4])
	fin_images = packOurNewData(org_test_labels, org_test_images)
	#print fin_images
	text_file = open("train_mixed_numbers_data.csv", "w+")
	text_file.write(fin_images+'\n')
	text_file.close()
	#org_test_images, org_test_labels = load_wrapper(path, train_img_fname, train_lbl_fname)


	org_test_images, org_test_labels = load_wrapper(path, test_img_fname, test_lbl_fname)	
	org_test_images, org_test_labels = mixThem_random(org_test_images, org_test_labels, validInts=[5,6,7,8,9])
	fin_images = packOurNewData(org_test_labels, org_test_images)
	#print fin_images
	text_file = open("test_mixed_numbers_data.csv", "w+")
	text_file.write(fin_images+'\n')
	text_file.close()
	#print org_test_images[0]
#	print junk[0]
#	print displayNumOfTrueOrFalse(junk)

#	saveThemToFile(('label_1', fin_labels), ('img_1', fin_images))

	#    print org_test_labels



def load_wrapper(path, img_fname, lbl_fname):
    ims, labels = load(os.path.join(path, img_fname),
                            os.path.join(path, lbl_fname))

    return ims, labels


def load(path_img, path_lbl):

    with open(path_lbl, 'rb') as file:
        magic, size = struct.unpack(">II", file.read(8))
        if magic != 2049:
            raise ValueError('Magic number mismatch, expected 2049,'
                             'got {}'.format(magic))

        labels = array("B", file.read())

    with open(path_img, 'rb') as file:
        magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
        if magic != 2051:
            raise ValueError('Magic number mismatch, expected 2051,'
                             'got {}'.format(magic))

        image_data = array("B", file.read())

    images = []
    for i in range(size):
        images.append([0] * rows * cols)

    for i in range(size):
        images[i][:] = image_data[i * rows * cols:(i + 1) * rows * cols]

    return images, labels


def display(img, width=28, threshold=200):
    render = ''
    for i in range(len(img)):
        if i % width == 0:
            render += '\n'
        if img[i] > threshold:
            render += '@'
        else:
            render += '.'
    return render


##################### 
#new stuff
##################### 

def isValidInt(value, validInts):
	for val in validInts:
		if value == val:
			return True
	return False

def mixThem_random(images, labels, validInts, num=100):
	
	if len(images) < num:
		num = len(images)

	ret_images = []
	ret_labels = []

	for i in range(num):

		
		isItTrue = randint(0,1) == 1 
		if isItTrue:
			image1, label1, image2, label2 = getTwoMatchingimages(images, labels, validInts)
		else:
			image1, label1, image2, label2 = getTwoNotMatchingimages(images, labels, validInts)

		
		print "isTrue: "+str(isItTrue)
		print "label1: "+str(label1)+" : "+str(label2)

		tempImg = image1[:]
		tempImg.extend(image2)
		ret_images.append(tempImg)

		ret_labels.append(isItTrue)

	return ret_images, ret_labels		



def getTwoMatchingimages(images, labels, validInts):
	idx1 = randint(0,len(images)-1)
		
	while not isValidInt(labels[idx1], validInts):
		idx1 = randint(0,len(images)-1)
	
	
	idx2 = randint(0,len(images)-1)
	while not isValidInt(labels[idx2], validInts) or labels[idx2] != labels[idx1]:
		idx2 = randint(0,len(images)-1)
	
	return images[idx1], labels[idx1], images[idx2], labels[idx2]

def getTwoNotMatchingimages(images, labels, validInts):
	idx1 = randint(0,len(images)-1)
	idx2 = randint(0,len(images)-1)
		
	while not isValidInt(labels[idx1], validInts):
		idx1 = randint(0,len(images)-1)

	while not isValidInt(labels[idx2], validInts):
		idx2 = randint(0,len(images)-1)
	
	return images[idx1], labels[idx1], images[idx2], labels[idx2]




def displayNumOfTrueOrFalse(inputBoolArr):
	t_count = 0
	f_count = 0
	for item in inputBoolArr:
		if item == True:
			t_count += 1
		else:
			f_count += 1

	return "true: " + str(t_count) + " false: " + str(f_count)


#returns byte array
def packImages(images, labels, width=28, magic_num=2051):
	ret = []
	size = len(images)
	cols = width
	rows = len(images[0])/cols
	lengthOfTheWholeThing=6000
	packed = ""
	topCount = 1568#len(images[0])
	packed = packed + str(lengthOfTheWholeThing) + ","
	packed = packed + str(topCount) + ","
	#for i in range(topCount):
	#	packed = packed + "p"+str(i)+","
		
	packed = packed + "True,"
	packed = packed + "False"
	packed = packed + "\n"

	for i in range(len(images)):
		image = images[i]
		count = 0
		vals = image[:topCount]
		packed = packed + ('.0,'.join(map(str, vals)))
		print len(vals)
		labelValue = 1 if labels[i] else 0
		packed = packed + ',' + str(labelValue)
		
		if i >= lengthOfTheWholeThing-1:
			break	
		packed = packed + "\n"
	
	return packed


def packOurNewData(labels, images):
	return packImages(images, labels)

start()
