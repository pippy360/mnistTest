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
path_to_nn = './thenn/'


def does_it_match(image1, image2):

	#FIXME: allow the two images to be 2d and also enforce the width/height
	image1.extend(image2)
	does_it_match(image1)

def does_it_match(singleSample):

	# Classify two new flower samples.
	#new_samples = np.array([singleSample], dtype=float)
	
	new_samples = np.array([singleSample,singleSample], dtype=float)
	y = g_theNN.predict(new_samples)
	print('Predictions: {}'.format(str(y)))
	return y == 1

def buildAndTestTheNN():
	theNN = buildTheNN()
	testTheNN(theNN)
	return theNN

def loadNN():
	classifier = tf.contrib.learn.DNNClassifier(
                                            feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10])

def testTheNN(theNN):
	# Evaluate accuracy.
	accuracy_score = theNN.evaluate(x=test_set.data,
                                     y=test_set.target)["accuracy"]
	print('Accuracy: {0:f}'.format(accuracy_score))



def buildTheNN(load_from_cache=False):
	global g_theNN
	g_theNN = None
	if load_from_cache:
		g_theNN = _buildTheNN_load_from_cache()
	else:
		g_theNN = _buildTheNN()
	return g_theNN

def _buildTheNN_load_from_cache():
	
	# Build 3 layer DNN with 10, 20, 10 units respectively.
	size = len(training_set[0][0])
	feature_columns = [tf.contrib.layers.real_valued_column("", dimension=size)]
	classifier = tf.contrib.learn.DNNClassifier(
                                            feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
						model_dir=path_to_nn)
	return classifier

def _buildTheNN():


	size = len(training_set[0][0])
	# Specify that all features have real-value data
	feature_columns = [tf.contrib.layers.real_valued_column("", dimension=size)]

	# Build 3 layer DNN with 10, 20, 10 units respectively.
	classifier = tf.contrib.learn.DNNClassifier(
                                            feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
						model_dir=path_to_nn)
	# Fit model.
	classifier.fit(x=training_set.data, 
               y=training_set.target, 
               steps=2000)
	

	return classifier
