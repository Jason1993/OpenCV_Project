import cv2
import numpy as np
import pcl
import os
import sys
from os import listdir
from os.path import isfile, join
fileDestination = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/results/"

fileToProcess = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/results/research/ROOM-4000mm-2000mmUP.png"
fileToProcess = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/results/research/teapot-000.png"

cloud = pcl.PointCloud()


original = cv2.imread(fileToProcess,-1)
original=cv2.bitwise_not(original)

shape = original.shape
height = shape[0]
width = shape[1]
num = height*width

a = np.zeros((num, 3),dtype=np.float32)

hFOV = 70		#horizontal
vFOV = 60		#vertical


focalPixelH = (width * 0.5) / (np.math.tan((hFOV*0.5*np.math.pi/180)))
focalPixelV = (height * 0.5) / (np.math.tan((vFOV*0.5*np.math.pi/180)))

fx = focalPixelH

fy = focalPixelV
dc = 0.1
#dc = 0.0679026


def pinhole(original):
	height = original.shape[0]
	width = original.shape[1]
	num = height * width
	cx = width / 2
	cy = height / 2
	a = np.zeros((num, 3),dtype=np.float32)
	index = 0
	
	for v in xrange(0, height):
	    for u in xrange(0, width):
	        check = original[v][u][0]
	        if check <= 0  :
        	    a[index][2] = np.nan
        	    a[index][0] = 0
        	    a[index][1] = 0
        	else:
        	    a[index][2] = (original[v][u][0] * dc)
        	    a[index][1] = (a[index][2] * (v-cy)) / fy
        	    a[index][0] = (a[index][2] * (u-cx)) / fx
        	index += 1
	return a

a = pinhole(original)

cloud.from_array(a)
cloud.to_file(fileDestination + "testPinhole.pcd")

print "done"