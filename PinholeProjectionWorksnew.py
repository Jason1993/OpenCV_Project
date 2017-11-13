import cv2
import numpy as np
import pcl
import os
import sys
import math
from os import listdir
from os.path import isfile, join
fileDestination = "/home/champ/Documents/Final_PCDS/"

#fileToProcess = "/home/champ/UTU_Depth_Project/ROOM-4000mm-2000mmUP.png"
fileToProcess = "//home/champ/Documents/Final_Dataset/RealDepth/Teapot/ZDepth-0001.png"

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
			if check <= 0:
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
theta_x = 80.827
theta_y = 0
theta_z = 90
radians_x = math.radians(theta_x)
radians_y = math.radians(theta_y)
radians_z = math.radians(theta_z)
cos_x = math.cos(radians_x)
cos_y = math.cos(radians_y)
cos_z = math.cos(radians_z)
sin_x = math.sin(radians_x)
sin_y = math.sin(radians_y)
sin_z = math.sin(radians_z)

print a.shape
rx = np.array([[1, 0, 0], [0, cos_x, sin_x ], [0, sin_x, cos_x]], dtype=np.float32)
ry = np.array([[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]], dtype=np.float32)
rz = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]], dtype=np.float32)
print rx.shape
rx_after = np.dot(a, rx)
ry_after = np.dot(rx_after, ry)
rz_after = np.dot(ry_after, rx)


cloud.from_array(rz_after)
cloud.to_file(fileDestination + "teapot_rotate_cam01_radians.pcd")

print "done"