import json
import os
import subprocess
from os.path import isfile, join
import numpy
def EulerToQuat(X,Y,Z):

    b = X * numpy.pi / 360
    h = Y * numpy.pi / 360
    a = Z * numpy.pi / 360

    c1 = numpy.cos(h)
    c2 = numpy.cos(a)
    c3 = numpy.cos(b)
    s1 = numpy.sin(h)
    s2 = numpy.sin(a)
    s3 = numpy.sin(b)

    qw = numpy.round((c1*c2*c3 - s1*s2*s3)*100000)/100000
    qx = numpy.round((s1*s2*c3 + c1*c2*s3)*100000)/100000
    qy = numpy.round((s1*c2*c3 + c1*s2*s3)*100000)/100000
    qz = numpy.round((c1*s2*c3 - s1*c2*s3)*100000)/100000

    return qx,qy,qz,qw

def main():
	#Reading JSON File. Specify the path to the json file as argument to open if not present within the same directory.
	devnull = open('/dev/null', 'w')
	#subprocess.call(["rm -rf results/Teapot"],shell=True)
	#subprocess.call(["mkdir results/Teapot"],shell=True)
	with open("DataSet_v3.json") as json_file:
		json_data=json.load(json_file)

	#Iterating through the DataSet
	directory="/home/champ/Documents/PointClouds/PCD_Empty/"
	outputDirectory="/home/champ/Documents/PointClouds/results/Empty/"
	files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
	i=0
	offset=-10
	files.sort()
	s=""
	for f in files:
		inputFile=f[:-4]+".pcd"
		s=s+outputDirectory+"transformed_"+inputFile+" "
		#command="python UTU-DepthToPointCloud-V001.py RealDepth/Teapot/"+f+" "+outputDirectory+outputFile
		#print command
		#print "Processing file "+f
		#process = subprocess.call([command],stdout=devnull,shell=True)

		#process = subprocess.Popen(, stdout=subprocess.PIPE, shell=True)
		if(json_data["DataSet"][i]["deviceType"]=="kinect2_simulated"):

			zpostition, xposition, yposition =json_data["DataSet"][i]["data"]["depth"]["globalPosition"]
			thetaz,thetax,thetay=json_data["DataSet"][i]["data"]["depth"]["globalRotation"]

			command="pcl_transform_point_cloud "+directory+inputFile+" temp.pcd"

			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.0,1.0,0.0"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.70711000000000002,0.0,0.70711000000000002"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.0,-0.70711000000000002,0.70711000000000002"
			subprocess.call([command],stdout=devnull,shell=True)

			theta=EulerToQuat(0,0,thetaz)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)

			theta=EulerToQuat(thetax,0,0)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)

			theta=EulerToQuat(0,thetay,0)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)

			command="pcl_transform_point_cloud temp.pcd "+outputDirectory+"transformed_"+inputFile+" -trans "+str(xposition)+","+str(yposition)+","+str(zpostition)
			subprocess.call([command],shell=True,stdout=devnull)
		i+=1

	subprocess.call(["pcl_viewer -ax 5000 "+s],shell=True,stdout=devnull)
if __name__=="__main__":
	main()
