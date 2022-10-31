# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:38:58 2015

@author: Gourab Haldar
"""
import numpy as np

def load_characters():
    im=np.load("./npy/data.npy")
    return im