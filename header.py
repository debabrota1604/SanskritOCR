# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 10:34:19 2015

@author: Gourab Haldar
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 19:43:04 2015

@author: Gourab Haldar
"""
#import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
from skimage.filter import threshold_adaptive,threshold_otsu

def rgb2gray(rgb):

    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def threshold(im):
    im_otsu=im
    row=len(im)
    col=len(im[0])
    block_size=(row+col)/20
    threshold_val=threshold_otsu(im)
    im_ad=threshold_adaptive(im,block_size,offset=10)
    for i in range(row):
        for j in range(col):
            if im[i][j] >=threshold_val:
                im_otsu[i][j]=255
            else:
                im_otsu[i][j]=0

    im_out=im
    for i in range(row):
        for j in range(col):
            if im_otsu[i][j]==0 and im_ad[i][j]==0:
                im_out[i][j]=0
            else:
                im_out[i][j]=255

    return im_out

def threshold_h(im):
    im_otsu=im
    row=len(im)
    col=len(im[0])
    block_size=(row+col)/20
    threshold_val=threshold_otsu(im)
    im_ad=threshold_adaptive(im,block_size,offset=10)
    for i in range(row):
        for j in range(col):
            if im[i][j] >=128:
                im_otsu[i][j]=255
            else:
                im_otsu[i][j]=0


    return im_otsu


def pad_img(im):
    v_pos=[0,0]
    j=0
    for i in range(len(im[0])):
        if vproj(im,i)>0:
            v_pos[j]=i
            j=1
            v_pos[j]=i


    j=0
    h_pos=[0,0]
    for i in range(len(im)):
        if hproj(im,i)>0:
            h_pos[j]=i
            j=1
            h_pos[j]=i

    h_pos[1]+=1
    v_pos[1]+=1
    height=h_pos[1]-h_pos[0]
    width=v_pos[1]-v_pos[0]
    if height==width:
        return im[h_pos[0]:h_pos[1],v_pos[0]:v_pos[1]]
    if height>width:
        big=height
    else:
        big=width
    temp_im=255*np.ones((big,big))
    k=(big-height)/2
    for i in range(h_pos[0],h_pos[1]):
        l=(big-width)/2
        for j in range(v_pos[0],v_pos[1]):
            temp_im[k][l]=im[i][j]
            l+=1
        k+=1
    return temp_im

def getlines(im):
    lst=[]
    row=len(im)
    col=len(im[0])
    flag=0
    i=0
    total_seg=0
    flag1=0
    while i < row:
        j=0
        sum=0
        while j < col:
            sum+=im[i][j]
            j=j+1

        #if average of the values in the coloumn is less than 254 then marking the row
        if sum/col <255:
            flag+=1
            flag1=0
        if sum/col==255 and flag>0:
            flag1+=1
            """
            some places are also detected in the normal process of height less than 3
            where 'matras' are present like ी ू etc due to a space between normal
            letters and matras in some rows of the image due to thresholding and high
            presence of white pixel in the row....hence those detected areas are
            undone by backtracing and unmarking the rows
            """

            if flag>3:
                if flag1>2:
                    lst.append([total_seg,i-flag-flag1,i])
                    total_seg+=1
                    flag=0
                    flag1=0

        i=i+1
    return lst

def getwords(im,lst1):
    lst=[]
    for k in lst1:
        ima=im[k[1]:k[2],:]
        row=len(ima)
        col=len(ima[0])
        total_seg=0
        j=0
        flag=0
        flag1=0
        while j < col:
            i=0
            sum=0
            while i < row:
                sum+=ima[i][j]
                i+=1
            #if average of the values in the coloumn is less than 254 then marking the row
            if (sum/row) < 255:
                flag+=1
                flag1=0
            if sum/row==255 and flag>0:
                flag1+=1
                if flag1>2:
                    lst.append([k[0],total_seg,k[1],k[2],j-flag-2,j])
                    total_seg+=1
                    flag=0
                    flag1=0
                if flag>0:
                    flag+=1
            j+=1
    return lst

def getletters(im,words):
    letArray=[]
    for T in words:
        ima=im[T[2]:T[3],T[4]:T[5]]
        k=detHorizontal(ima)
        ls=segmentMidLetters(k,T,im)
        ls1=LowerMatras(k,ls,T[3]-(T[2]+k[0]),im)
        #ls3=segmentYuktakshar(k,ls,im)
        ls2=segmentUpMatras(k,T,im)
        if ls2 or ls1:
            if ls1:
                ls=syncDnMatras(ls,ls1)
            if ls2:
                ls=syncUpMatras(ls,ls2)
        for l in ls:
            letArray.append(l)
    return letArray



def detHorizontal(im):
    row=len(im)
    col=len(im[0])
    i=0
    k=0
    flag=0
    while i < row/2:
        j=0
        sum=0
        while j < col:
            sum+=im[i][j]
            j+=1
        if (sum) < (255*col*0.50):
            if k==0:
                k=i
            flag=1
        if (sum)>=(255*col*0.50) and flag==1:
            break
        i+=1
    if flag!=1:
        return [0,0]
    return [k,i]

def segmentMidLetters(k,T,im):
    lst=[]
    ima=im[(T[2]+k[1]):T[3],T[4]:T[5]]
    row=len(ima)
    col=len(ima[0])
    total_seg=0
    j=0
    flag=0
    while j < col:
        i=0
        sum=0
        while i < row:
            sum+=ima[i][j]
            i+=1
        if (sum/row) < 255:
            flag+=1
        if sum/row==255 and flag>0:
            flag1=0
            l=T[3]
            while l>T[2]+k[0]:
                m=T[4]+j-flag
                while m<T[4]+j:
                    if im[l][m]==0:
                        flag1=1
                        break
                    m+=1
                if flag1==1:
                    break
                l-=1
            lst.append([T[0],T[1],T[2]+k[0],l+1,T[4]+j-flag,T[4]+j])
            total_seg+=1
            flag=0
        j+=1


    return lst

def segmentUpMatras(k,T,im):
    lst=[]
    if k[0]<=0 or (T[5]-T[4])<=0:
        return
    ima=im[T[2]:(T[2]+k[0]),T[4]:T[5]]
    row=len(ima)
    col=len(ima[0])
    total_seg=0
    j=0
    flag=0
    while j < col:
        i=0
        sum=0
        while i < row:
            sum+=ima[i][j]
            i+=1
        if (sum/row) < 255:
            flag+=1
        if sum/row==255 and flag>0:
            lst.append([T[0],T[1],T[2],T[2]+k[0],T[4]+j-flag,T[4]+j])
            total_seg+=1
            flag=0
        j+=1
    return lst


def LowerMatras(k,lst,total_height,im):
    b1=0
    b2=0
    lst1=[]
    lst2=[]
    j=-1
    for i in lst:
        j+=1
        h=i[3]-i[2]
        if h>0.70*total_height:
            b1+=1
            lst1.append(j)
        else:
            b2+=1
    if b1<b2 and b1>0:
        lst2=segmentLower(k,lst,lst1,im)
    return lst2


def segmentLower(L,lst,lst1,im):
    lstout=[]
    for i in lst1:
        ima=im[lst[i][2]:lst[i][3],lst[i][4]:lst[i][5]]
        row=len(ima)
        k=len(ima)/2
        minv=len(ima[0])
        mini=k
        while k<row:
            t=hproj(ima,k)
            if t==0:
                mini=k
                break
            if t<minv:
                mini=k
                minv=t
            k+=1
        lstout.append([lst[i][2]+mini,lst[i][3],lst[i][4],lst[i][5]])
        lst[i][3]=lst[i][2]+mini-1
        ima=im[(lst[i][2]+L[1]):lst[i][3],lst[i][4]:lst[i][5]]
        j=len(ima[0])-1
        while j>=0:
            if vproj(ima,j)>0:
                break
            j-=1
        lst[i][5]=lst[i][4]+j+1
    return lstout

def syncUpMatras(letters,matras):
    Sync=[]
    l=len(letters)
    j=0
    flag=0
    for i in matras:
        if j>=l:
            break
        while i[5]>letters[j][4]:
            Sync.append(letters[j])
            j+=1
            if j>=l:
                flag=1
                break
        Sync.append(i)
        if flag==1:
            break
        Sync.append(letters[j])
        j+=1
    while j<l:
        Sync.append(letters[j])
        j+=1
    return Sync

def syncDnMatras(ls,ls1):
    Sync=[]
    l=len(ls)
    j=0
    for i in ls1:
        if j>=l:
            break
        while i[2]>ls[j][4]:
            Sync.append(ls[j])
            j+=1
            if j>=l:
                break
        Sync.append(ls[j])
        Sync.append([ls[j][0],ls[j][1],i[0],i[1],i[2],i[3]])
        j+=1
    while j<l:
        Sync.append(ls[j])
        j+=1
    return Sync

def syncletters(st):
    buff=[0 for i in range(len(st))]
    j=0
    vert_line=0
    flag=0
    for i in range(len(st)):
        if st[i]==2358 or st[i]==2327 or st[i]==2339:
            a=st[i]
            flag=1
        elif st[i]==2367 or st[i]==2368:
            if vert_line==1 and st[i-3]==a:
                buff[j]=2367
            else:
                buff[j]=2368
                j+=1
        elif st[i]==2381 and flag==1:
            print "H"
        elif st[i]==2366:
            if flag==1 and st[i-2]==a:
                buff[j]=a
                j+=1
                flag=0
            elif st[i-1]==32:
                buff[j]=2404
                j+=1
            elif i+1<len(st):
                
                if st[i+1]==2368 or st[i+1]==2367:
                    k=1
                else:
                    k=2
                #flag1=1
                    while((k+i)<len(st)):
                        if st[k+i]!=2381:
                            break 
                        k+=2
                    if st[i+k]==2367 or st[i+k]==2368:
                        vert_line=1
                    else:
                        buff[j]=2366
                        j+=1
                
        elif st[i]==2375 and st[i-1]==2366:
            buff[j]=2379
            j+=1
        elif st[i]==2376 and st[i-1]==2366:
            buff[j]=2380
            j+=1
        else:
            buff[j]=st[i]
            j+=1
    
    #print buff
    return buff

def hproj(image,row):
    total=0
    col=len(image[0])
    j=0
    while j<col:
        if image[row][j]==0:
            total+=1
        j+=1
    return total

def vproj(image,col):
    total=0
    i=len(image)-1
    while i>=0:
        if image[i][col]==0:
            total+=1
        i-=1
    return total