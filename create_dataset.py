# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:38:03 2015

@author: Gourab Haldar
"""
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import header as hF
#import headFunc
import os
from pandas import Series

n_samples=160
Image=np.ndarray((n_samples,40,40))
Unicode=np.ndarray((n_samples))
name_unicode=[]
i=0
for root, dirs, files in os.walk("./Temp", topdown=False):
    for name in files:
        im=misc.imread(root+"/"+name)
        im=hF.rgb2gray(im)
        im=hF.threshold_h(im)
        im = (im).astype(np.uint8)
        Image[i]=im
        Unicode[i]=(name[0:((len(name))-4-len(name)%4)])
        print Unicode[i]
        i+=1
dct={'I':Image,'U':Unicode}
M=Series(dct)
print M[0][0]
plt.title('output image', fontsize=12)
plt.imshow(M[0][1],cmap = plt.cm.gray,origin='upper')
plt.show()
np.save("./npy/data.npy",M)