import cv2
import numpy as np
import pcl

fileToProcess = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/results/teapot.png"

fileDestination = "/home/silverstein_louis/Desktop/FTP_REPO/2016-USC-UTU/results/"

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
fy = 365.6058
dc = 0.0679026

focalPixel = (width * 0.5) / (np.math.tan((hFOV*0.5*np.math.pi/180)))

print focalPixel

cloud = pcl.PointCloud()
a = np.zeros((num, 3),dtype=np.float32)
index = 0

for x in xrange(0, width):
    for y in xrange(0, height):
        check = original[y][x][0]
        if check == 0:
            a[index][2] = 0
            a[index][0] = 0
            a[index][1] = 0

        else:
            a[index][2] = (original[y][x][0] * dc)
            a[index][0] = (a[index][2] * (x-cy)) / fy
            a[index][1] = (a[index][2] * (y-cx)) / fx


        index += 1

cloud.from_array(a)
cloud.to_file(fileDestination + "test2.pcd")
print height
print width
print cloud
