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

if len(sys.argv) <2:
	print "combinepcd.py file-or-directory-path output-file "
	sys.exit(1)
if os.path.isdir(sys.argv[1]):
	files = [sys.argv[1]+"/"+f for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f))]
elif os.path.isfile(sys.argv[1]):
	files=[sys.argv[1]]
else:
	print "Incorrect argument"
	sys.exit(1)
if len(sys.argv) < 3:
	destination="test.pcd"
else:
	destination=sys.argv[2]
#print files
final=np.empty((0,3),dtype=np.float32)
for fileToProcess in files:
	original = cv2.imread(fileToProcess , -1)
	cv2.bitwise_not(original, original)
	hFOV = 70
	vFOV = 60
	height = original.shape[0]
	width = original.shape[1]
	num = height * width
	cx = width / 2
	cy = height / 2
	fx = 365.6058
	fy = 367.194
	dc = 0.0679026

	cloud = pcl.PointCloud()
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
	final=np.concatenate([final,a])
	print final.shape
cloud.from_array(final)
cloud.to_file(destination)


#Code to remove noise
#Need to test on multiple images and check if the parameters passed to the filter should be changed
p = pcl.load(destination)	
fil = p.make_statistical_outlier_filter()
fil.set_mean_k(50)
fil.set_std_dev_mul_thresh(2.5)

pcl.save(fil.filter(), "test3.pcd")

print height
print width
print cloud
