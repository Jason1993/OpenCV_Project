import json
import os
import subprocess
from os.path import isfile, join
import numpy
import sys
import cv2
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
	directory=sys.argv[1]
	outputDirectory=sys.argv[2]
	subprocess.call(["rm -rf "+outputDirectory],shell=True)
	subprocess.call(["mkdir "+outputDirectory],shell=True)
	with open("DataSet_v4.json") as json_file:
		try:
                	json_data=json.load(json_file)
	    	except Exception,e:
			print str(e)
	files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
	i=0
	offset=-10
	files.sort()
	s=""
	j=0
	while j<len(files):
		f=files[j]
		#raw_input()
		outputFile=f[:-4]+".pcd"
		s=s+outputDirectory+"/transformed_"+outputFile+" "
		command="python UTU-DepthToPointCloud-V001.py "+directory+"/"+f+" "+outputDirectory+outputFile
		#print command
		print "Processing file "+f
		process = subprocess.call([command],stdout=devnull,shell=True)
		
		#command="python removeNoise.py "+outputDirectory+outputFile+" "+outputDirectory+outputFile
		#subprocess.call([command],stdout=devnull,shell=True)
		#process = subprocess.Popen(, stdout=subprocess.PIPE, shell=True)
		if(json_data["DataSet"][i]["deviceType"]=="kinect2_simulated"):

			zpostition, xposition, yposition =json_data["DataSet"][i]["data"]["depth"]["globalPosition"]
			thetaz,thetax,thetay=json_data["DataSet"][i]["data"]["depth"]["globalRotation"]

			command="pcl_transform_point_cloud "+outputDirectory+"/"+outputFile+" temp.pcd"

			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.0,1.0,0.0"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.70711000000000002,0.0,0.70711000000000002"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.0,0.0,-0.70711000000000002,0.70711000000000002"
			subprocess.call([command],stdout=devnull,shell=True)
			
			command="pcl_transform_point_cloud temp.pcd temp.pcd -trans 0,"+str(offset)+",0"
			#print command
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

			command="pcl_transform_point_cloud temp.pcd "+outputDirectory+"/transformed_"+outputFile+" -trans "+str(xposition)+","+str(yposition)+","+str(zpostition)
			subprocess.call([command],shell=True,stdout=devnull)
		i+=1
		j+=20
	print "pcl_viewer -ax 5000 "+s
	subprocess.call(["pcl_viewer -ax 5000 "+s],shell=True,stdout=devnull)
if __name__=="__main__":
	main()
			
			
			
			
			
			

	
