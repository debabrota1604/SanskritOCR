# -*- coding: utf-8 -*-
"""
Created on Sat Apr 04 19:17:12 2015

@author: Gourab Haldar
"""

import numpy as np
import header as hF
from scipy import misc
import dataset
import PythonApplication1 as p
import codecs

print "Please Wait..."
im = misc.imread('test.jpg') #reating a gray scale image
im = hF.rgb2gray(im)
im = (im).astype(np.uint8)
im=hF.threshold(im)#thresholding
#mahotas.imsave("url1.png",im)
lst=hF.getlines(im)
lst1=hF.getwords(im,lst)

lst2=hF.getletters(im,lst1)

letters = dataset.load_characters()


a=[]
j=1
y=0
z=0
st=""

for i in lst2:
    f=0
    if z!=i[0]:
        a.append(10)
    if y!=i[1]:
        a.append(32)
        f=1
    z=i[0]
    y=i[1]
    ima=im[i[2]:i[3],i[4]:i[5]]
    ima=hF.pad_img(ima)
    img=misc.imresize(ima,(40,40))
    img=hF.threshold_h(img)
    j+=1
    x=p.classify(img,letters)

    if len(x)>4:
        c1=0
        c2=4
        for m in range(len(x)/4):
            a.append(int(x[c1:c2]))
            c1=c2
            c2=c2+4



    else:
        a.append(int(x))

SYNC=hF.syncletters(a)
for i in SYNC:
    if i==0:
        break
    st+=(unichr(i))

text_file = codecs.open("Output.txt", "w",encoding='utf8')
text_file.write(st)
text_file.close()