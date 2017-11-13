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
	subprocess.call(["rm -rf results/Teapot"],shell=True)
	subprocess.call(["mkdir results/Teapot"],shell=True)
	with open("DataSet_v3.json") as json_file:
		try:
                	json_data=json.load(json_file)
	    	except Exception,e:
			print str(e)
	#Iterating through the DataSet
	directory="RealDepth/Teapot"
	files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
	i=0
	offset=-10
	files.sort()
	for f in files:
		command="python UTU-DepthToPointCloud-V001.py RealDepth/Teapot/"+f+" results/Teapot/"+f[:-4]+".pcd"
		#print command
		print "Processing file "+f
		process = subprocess.call([command],stdout=devnull,shell=True)
		
		#process = subprocess.Popen(, stdout=subprocess.PIPE, shell=True)
		if(json_data["DataSet"][i]["deviceType"]=="kinect2_simulated"):
			
			position=json_data["DataSet"][i]["data"]["depth"]["globalPosition"]
			thetax,thetaz,thetay=json_data["DataSet"][i]["data"]["depth"]["globalRotation"]
			command="pcl_transform_point_cloud results/Teapot/"+f[:-4]+".pcd temp.pcd -quat 0,0,1,0"
			
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0,1,0,0"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat 0.70711,0,0,-0.70711"
			subprocess.call([command],stdout=devnull,shell=True)
			command="pcl_transform_point_cloud temp.pcd temp.pcd -trans 0,-10,0"
			subprocess.call([command],stdout=devnull,shell=True)
			
			theta=EulerToQuat(thetax,0,0)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)
			theta=EulerToQuat(0,thetay,0)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)
			theta=EulerToQuat(0,0,thetaz)
			#print theta
			command="pcl_transform_point_cloud temp.pcd temp.pcd -quat "+str(theta[0])+","+str(theta[1])+","+str(theta[2])+","+str(theta[3])
			subprocess.call([command],shell=True,stdout=devnull)
			command="pcl_transform_point_cloud temp.pcd results/Teapot/transformed_"+f[:-4]+".pcd -trans -"+str(position[0])+","+str(position[1])+","+str(position[2])
			subprocess.call([command],shell=True,stdout=devnull)
		i+=1
	
if __name__=="__main__":
	main()
			
			
			
			
			
			

	
