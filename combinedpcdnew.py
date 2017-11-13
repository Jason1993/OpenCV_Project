#Code to generate one pcd file from multiple depth images
#Needs two command line arguments. The first one is the input and the second is output
#The input path can be either a file or directory. If it's a file then the output will be same as our previous code
#If input is a directory then this code generates a combined pcd of all the depth files in the input folder.
#The output is the pcd file to store in, test.pcd by default if it's not provided
import cv2
import numpy as np
import pcl
import os
import sys
from os import listdir
from os.path import isfile, join


hFOV = 70
vFOV = 60
fx = 365.6058
fy = 367.194
dc = 0.0679026

def pinhole(original):
	height = original.shape[0]
	width = original.shape[1]
	num = height * width
	cx = width / 2
	cy = height / 2
	a = np.zeros((num, 3),dtype=np.float32)
	index = 0
	
	for x in xrange(0, width):
	    for y in xrange(0, height):
	        check = original[y][x][0]
	        if check <= 0  :
        	    a[index][2] = np.nan
        	    a[index][0] = 0
        	    a[index][1] = 0
        	else:
        	    a[index][2] = (original[y][x][0] * dc)
        	    a[index][0] = (a[index][2] * (x-cy)) / fy
        	    a[index][1] = (a[index][2] * (y-cx)) / fx
        	index += 1
	return a

def matlab(original):
	rows = original.shape[0]
	columns = original.shape[1]
	center=[rows / 2,columns / 2]
	topleft=[1,1]
	MM_PER_M = 1000
	
	depth_data=np.zeros((original.shape[0],original.shape[1]),dtype=np.float32)
	for i in range(0,original.shape[0]):
		for j in range(0,original.shape[1]):
			depth_data[i][j]=original[i][j][0]
	index=0
	depth_data[depth_data==0]=np.nan
	a = np.zeros((rows,columns, 3),dtype=np.float32)
	xgrid= np.ones((rows,1)) * np.arange(1,columns+1) + (topleft[0]-1) -center[0]
	ygrid= (np.arange(1,rows+1)[np.newaxis]).T * np.ones((1,columns)) + (topleft[1]-1) -center[1]

	a[:,:,0]=np.multiply(xgrid,depth_data)/ fx/ MM_PER_M
	a[:,:,1]=np.multiply(ygrid,depth_data)/ fy/ MM_PER_M
	a[:,:,2]=depth_data/MM_PER_M
	a=np.vstack(a)
	return a

def cvreproject(fileToProcess):
	original = cv2.imread(fileToProcess , 0)
	print original.dtype
	print original.shape
	rows = original.shape[0]
	columns =original.shape[1]
	Q = np.float32([[1, 0, 0, -0.5*columns],
                    [0,-1, 0,  0.5*rows],
                    [0, 0, 0,     -fx], 
                    [0, 0, 1,      0]])
	points = cv2.reprojectImageTo3D(original, Q)
	mask = original > original.min()
	out_points = points[mask]
	return out_points


if len(sys.argv) <3:
	print "combinepcd.py file-or-directory-path output-file "
	sys.exit(1)
if os.path.isdir(sys.argv[1]):
	files = [sys.argv[1]+"/"+f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
elif os.path.isfile(sys.argv[1]):
	files=[sys.argv[1]]
else:
	print "Incorrect argument"
	sys.exit(1)

#if len(sys.argv) < 3:
#	destination="test.pcd"
#else:
#	destination=sys.argv[2]
if len(sys.argv) < 4:
	option=1
else:
	option=sys.argv[3]
destination=sys.argv[2]
#print files
final=np.empty((0,3),dtype=np.float32)
for fileToProcess in files:
	original = cv2.imread(fileToProcess , -1)
	cv2.bitwise_not(original, original)
	a=np.empty((0,3),dtype=np.float32)
	if option=='1':
		a=pinhole(original)
	elif option=='2':
		a=matlab(original)
	elif option=='3':
		a=cvreproject(fileToProcess)
	final=np.concatenate([final,a])

cloud = pcl.PointCloud()
cloud.from_array(final)
cloud.to_file(destination)


#Code to remove noise
#Need to test on multiple images and check if the parameters passed to the filter should be changed
'''p = pcl.load(destination)	
fil = p.make_statistical_outlier_filter()
fil.set_mean_k(50)
fil.set_std_dev_mul_thresh(2.5)

pcl.save(fil.filter(), "filtered.pcd")'''

