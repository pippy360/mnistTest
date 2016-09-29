from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np


# Data sets
IRIS_TRAINING = "train_mixed_numbers_data.csv"
IRIS_TEST = "test_mixed_numbers_data.csv"

# Load datasets.
training_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TRAINING, 
                                                       target_dtype=np.int)
test_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TEST, 
                                                   target_dtype=np.int)
g_theNN = None
path_to_nn = 'theNN.nn'


def does_it_match(image1, image2):

	#FIXME: allow the two images to be 2d and also enforce the width/height
	image1.extend(image2)
	does_it_match(image1)

def does_it_match(singleSample):

	# Classify two new flower samples.
	new_samples = np.array(    [singleSample], dtype=float)
	y = g_theNN.predict(new_samples)
	print('Predictions: {}'.format(str(y)))


def buildAndTestTheNN():
	theNN = buildTheNN()
	testTheNN(theNN)
	return theNN

def loadNN():
	classifier = tf.contrib.learn.DNNClassifier(
                                            feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10])
	classifier.restore(path_to_nn)

def testTheNN(theNN):
	# Evaluate accuracy.
	accuracy_score = theNN.evaluate(x=test_set.data,
                                     y=test_set.target)["accuracy"]
	print('Accuracy: {0:f}'.format(accuracy_score))



def buildTheNN():


	size = len(training_set[0][0])
	# Specify that all features have real-value data
	feature_columns = [tf.contrib.layers.real_valued_column("", dimension=size)]

	print("feature_columns")
	print(feature_columns)

	# Build 3 layer DNN with 10, 20, 10 units respectively.
	classifier = tf.contrib.learn.DNNClassifier(
                                            feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10])
	classifier.save(path_to_nn)
	# Fit model.
	classifier.fit(x=training_set.data, 
               y=training_set.target, 
               steps=2000)
	
	global g_theNN
	g_theNN = classifier

	return classifier
