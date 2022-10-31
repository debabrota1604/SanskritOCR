# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 02:08:48 2015

@author: lenovo
"""
def classify(im,letters):
    j=0
    for i in letters[0]:
        if (i-im).all==0:
            break;
    return str(int(letters[1][j]))