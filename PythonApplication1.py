# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:38:58 2015

@author: Gourab Haldar
"""

# Import dataset, classifiers and performance metrics
from sklearn import svm
# The data that we are interested in is made of 40x40 images of digits
# Note that each image must have the same size. For theseimages,
# we know which Letter they represent: it is given in the [1]th position of
# the dataset.
def classify(img,letters):
    # The letters dataset
    # To apply a classifier on this data, we need to flatten the image, to
    # turn the data in a (samples, feature) matrix:
    n_samples = len(letters[0])
    data = letters[0].reshape((n_samples,-1))


    # Create a classifier: a support vector classifier
    classifier = svm.SVC(gamma=0.001)

    # We learn the digits on the first half of the digits
    classifier.fit(data,letters[1])
    # Now predict the value of the digit on the second half:
    predicted = classifier.predict(img.reshape(1600))
    #print result

    return str(int(predicted))