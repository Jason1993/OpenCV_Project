import cv2
import numpy as np
import pcl
import math
from pcl.registration import icp_nl, icp, gicp

teapot = pcl.PointCloud()
teapot.from_file('/home/champ/Documents/Final_PCDS/main_final_teapot.pcd')

teapot = teapot.to_array();

theta_x = 279.173
theta_y = -90
theta_z = 0
radians_x = math.radians(theta_x)
radians_y = math.radians(theta_y)
radians_z = math.radians(theta_z)
cos_x = math.cos(radians_x)
cos_y = math.cos(radians_y)
cos_z = math.cos(radians_z)
sin_x = math.sin(radians_x)
sin_y = math.sin(radians_y)
sin_z = math.sin(radians_z)

rx = np.array([[1, 0, 0], [0, cos_x, sin_x ], [0, sin_x, cos_x]], dtype=np.float32)
ry = np.array([[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]], dtype=np.float32)
rz = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]], dtype=np.float32)

rx_after = np.dot(teapot, rx)
ry_after = np.dot(rx_after, ry)
rz_after = np.dot(ry_after, rz)

new_point_cloud = pcl.PointCloud()
new_point_cloud.from_array(rz_after)
new_point_cloud.to_file('/home/champ/Documents/Final_PCDS/main_expected_teapot.pcd')