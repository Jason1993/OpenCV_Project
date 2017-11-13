
import cv2
import numpy as np
import pcl
import os
import sys
from os import listdir
from os.path import isfile, join
import os
import sys



fileDestination = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/RealDepth/Teapot/PCD/"
folderToProcess = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/RealDepth/Teapot/"

x = True

#prosess all files in a folder
while x == True:
	for files in os.listdir(folderToProcess):
		fileToProcess = folderToProcess + files

		cloud = pcl.PointCloud()


		original = cv2.imread(fileToProcess,-1)
		original=cv2.bitwise_not(original)

		shape = original.shape
		height = shape[0]
		width = shape[1]
		num = height*width

		a = np.zeros((num, 3),dtype=np.float32)

		cameraType = "kinect"

		if cameraType == "kinect":
			hFOV = 70		#horizontal
			vFOV = 60		#vertical
			dc = 0.0693195

		if cameraType == "rando":
			hFOV = 119		#horizontal
			vFOV = 104		#vertical
			dc = 0.1

		if cameraType == "stereo":
			hFOV = 84		#horizontal
			vFOV = 53		#vertical
			dc = 0.1

		focalPixelH = (width * 0.5) / (np.math.tan((hFOV*0.5*np.math.pi/180)))
		focalPixelV = (height * 0.5) / (np.math.tan((vFOV*0.5*np.math.pi/180)))

		fx = focalPixelH
		fy = focalPixelV
		#dc = 0.0679026


		def pinhole(original):
			height = original.shape[0]
			width = original.shape[1]
			num = height * width
			cx = width / 2
			cy = height / 2
			a = np.zeros((num, 3),dtype=np.float32)
			index = 0
			fileDepth = len(original.shape)

			for v in xrange(0, height):
				for u in xrange(0, width):
					#print original[v][u]
					if fileDepth == 2:
						check = original[v][u]	#non depth based
					if fileDepth == 3:
						check = original[v][u][0]


					if check <= 0  :
						a[index][2] = np.nan
						a[index][0] = np.nan
						a[index][1] = np.nan

					if check == 255  :
						a[index][2] = np.nan
						a[index][0] = np.nan
						a[index][1] = np.nan

					else:
						if fileDepth == 2:
							a[index][2] = (original[v][u] * dc) #non depth base
							a[index][1] = (a[index][2] * (v-cy)) / fy
							a[index][0] = (a[index][2] * (u-cx)) / fx
						else:
							a[index][2] = (original[v][u][0] * dc)
							a[index][1] = (a[index][2] * (v-cy)) / fy
							a[index][0] = (a[index][2] * (u-cx)) / fx
					index += 1
			return a

		a = pinhole(original)

		cloud.from_array(a)
		cloud.to_file(fileDestination + str(files).split(".")[0]+ ".pcd")

		print "done"

y = False

#process individual file
while y == True:
	files = "ZDepth-0000.png"

	fileToProcess = folderToProcess + files

	cloud = pcl.PointCloud()


	original = cv2.imread(fileToProcess,-1)
	original=cv2.bitwise_not(original)

	shape = original.shape
	height = shape[0]
	width = shape[1]
	num = height*width

	a = np.zeros((num, 3),dtype=np.float32)

	cameraType = "kinect"

	if cameraType == "kinect":
		hFOV = 70		#horizontal
		vFOV = 60		#vertical
		dc = 0.0693195

	if cameraType == "rando":
		hFOV = 119		#horizontal
		vFOV = 104		#vertical
		dc = 0.1

	if cameraType == "stereo":
		hFOV = 84		#horizontal
		vFOV = 53		#vertical
		dc = 0.1

	focalPixelH = (width * 0.5) / (np.math.tan((hFOV*0.5*np.math.pi/180)))
	focalPixelV = (height * 0.5) / (np.math.tan((vFOV*0.5*np.math.pi/180)))

	fx = focalPixelH
	fy = focalPixelV
	#dc = 0.0679026


	def pinhole(original):
		height = original.shape[0]
		width = original.shape[1]
		num = height * width
		cx = width / 2
		cy = height / 2
		a = np.zeros((num, 3),dtype=np.float32)
		index = 0
		fileDepth = len(original.shape)

		for v in xrange(0, height):
			for u in xrange(0, width):
				#print original[v][u]
				if fileDepth == 2:
					check = original[v][u]	#non depth based
				if fileDepth == 3:
					check = original[v][u][0]


				if check <= 0  :
					a[index][2] = np.nan
					a[index][0] = np.nan
					a[index][1] = np.nan

				if check == 255  :
					a[index][2] = np.nan
					a[index][0] = np.nan
					a[index][1] = np.nan

				else:
					if fileDepth == 2:
						a[index][2] = (original[v][u] * dc) #non depth base
						a[index][1] = (a[index][2] * (v-cy)) / fy
						a[index][0] = (a[index][2] * (u-cx)) / fx
					else:
						a[index][2] = (original[v][u][0] * dc)
						a[index][1] = (a[index][2] * (v-cy)) / fy
						a[index][0] = (a[index][2] * (u-cx)) / fx
				index += 1
		return a

	a = pinhole(original)

	cloud.from_array(a)
	cloud.to_file(fileDestination + str(files).split(".")[0]+ ".pcd")

	print "done"
