pcl_transform_point_cloud ZDepth-0000.pcd ZDepth-0000_flip.pcd -quat 0,0,1,0
pcl_transform_point_cloud ZDepth-0000_flip.pcd ZDepth-0000_flip2.pcd -quat 0,1,0,0
pcl_transform_point_cloud ZDepth-0000_flip2.pcd ZDepth-0000_init.pcd -quat 0.70711,0,0,-0.70711
pcl_transform_point_cloud ZDepth-0000_init.pcd ZDepth-0000_off.pcd -trans 0,-10,0
pcl_transform_point_cloud ZDepth-0000_off.pcd ZDepth-0000_rot.pcd -quat 0.64832,0,0,0.76137
pcl_transform_point_cloud ZDepth-0000_rot.pcd ZDepth-0000_rot2.pcd -quat 0,0.70711,0,0.70711
pcl_transform_point_cloud ZDepth-0000_rot2.pcd ZDepth-0000_pos.pcd -trans -1622.489,1346.200,6720.560

pcl_transform_point_cloud ZDepth-0001.pcd ZDepth-0001_flip.pcd -quat 0,0,1,0
pcl_transform_point_cloud ZDepth-0001_flip.pcd ZDepth-0001_flip2.pcd -quat 0,1,0,0
pcl_transform_point_cloud ZDepth-0001_flip2.pcd ZDepth-0001_init.pcd -quat 0.70711,0,0,-0.70711
pcl_transform_point_cloud ZDepth-0001_init.pcd ZDepth-0001_off.pcd -trans 0,-10,0
pcl_transform_point_cloud ZDepth-0001_off.pcd ZDepth-0001_rot.pcd -quat 0.64832,0,0,0.76137
pcl_transform_point_cloud ZDepth-0001_rot.pcd ZDepth-0001_rot2.pcd -quat 0,0.70711,0,-0.70711
pcl_transform_point_cloud ZDepth-0001_rot2.pcd ZDepth-0001_pos.pcd -trans -4438.232,1346.200,6720.560

pcl_transform_point_cloud ZDepth-0002.pcd ZDepth-0002_flip.pcd -quat 0,0,1,0
pcl_transform_point_cloud ZDepth-0002_flip.pcd ZDepth-0002_flip2.pcd -quat 0,1,0,0
pcl_transform_point_cloud ZDepth-0002_flip2.pcd ZDepth-0002_init.pcd -quat 0.70711,0,0,-0.70711
pcl_transform_point_cloud ZDepth-0002_init.pcd ZDepth-0002_off.pcd -trans 0,-10,0
pcl_transform_point_cloud ZDepth-0002_off.pcd ZDepth-0002_rot.pcd -quat 0.65618,0,0,0.75461
pcl_transform_point_cloud ZDepth-0002_rot.pcd ZDepth-0002_rot2.pcd -quat 0,1,0,0.00159
pcl_transform_point_cloud ZDepth-0002_rot2.pcd ZDepth-0002_rot3.pcd -quat 0,1,0,0
pcl_transform_point_cloud ZDepth-0002_rot3.pcd ZDepth-0002_pos.pcd -trans -3013.107,1346.200,8517.22i
