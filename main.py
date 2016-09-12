import os
import struct
from array import array
from random import randint

def start(path='./data'):

#	test_img_fname = 't10k-images-idx3-ubyte'
#	test_lbl_fname = 't10k-labels-idx1-ubyte'

	test_img_fname = 'img_1'
	test_lbl_fname = 'label_1'

	train_img_fname = 'train-images-idx3-ubyte'
	train_lbl_fname = 'train-labels-idx1-ubyte'

	org_test_images = []
	org_test_labels = []

	org_train_images = []
	org_train_labels = []

	org_test_images, org_test_labels = load_wrapper(path, test_img_fname, test_lbl_fname)

#	org_test_images, org_test_labels = mixThem_random(org_test_images, org_test_labels)

	#print org_test_images[0]
	print display(org_test_images[0])
#	print junk[0]
#	print displayNumOfTrueOrFalse(junk)

	fin_labels, fin_images = packOurNewData(org_test_labels, org_test_images)

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

def mixThem_random(images, labels, num=9999):
	
	if len(images) < num:
		num = len(images)

	ret_images = []
	ret_labels = []

	for i in range(num):

		idx1 = randint(0,len(images)-1)
		idx2 = randint(0,len(images)-1)

		tempImg = images[idx1][:]
		tempImg.extend(images[idx2])
		ret_images.append(tempImg)

		if labels[idx1] == labels[idx2]:
			ret_labels.append(True)
		else:
			ret_labels.append(False)

	return ret_images, ret_labels		


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
def packImages(images, width=28, magic_num=2051):
	ret = []
	size = len(images)
	cols = width
	rows = len(images[0])/cols

 	packed = struct.pack(">IIII", magic_num, size, rows, cols)
	
 	for byte in packed:
 		ret.append(byte)

	for image in images:
		ret.extend(image)

	return ret



#returns byte array
def packLabels(labels, magic_num=2049):
	ret = []
	size = len(labels)

 	packed = struct.pack(">II", magic_num, size)

 	for byte in packed:
 		ret.append(byte)

	for label in labels:
		ret.append(label)

	return ret


def packOurNewData(labels, images):
	fin_images = packImages(images)
	fin_labels = packLabels(labels)
	return fin_labels, fin_images

def saveThemToFile(labels_tup, images_tup):
	saveToFile(labels_tup)
	saveToFile(images_tup)

def saveToFile(tup):
	#print tup
	name, byteArr = tup

	f = open('./data/'+name, 'w+')
	for byte in bytearray(byteArr):
		bigEndByte = struct.pack(">B", byte)
		f.write(bigEndByte)
	f.close()

start()