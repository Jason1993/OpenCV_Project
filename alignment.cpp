#include <boost/make_shared.hpp>
#include <pcl/point_types.h>
#include <pcl/point_cloud.h>
#include <pcl/point_representation.h>
#include <pcl/registration/ia_ransac.h>
#include <pcl/io/pcd_io.h>

#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/filter.h>

#include <pcl/features/normal_3d.h>

#include <pcl/registration/icp.h>
#include <pcl/registration/icp_nl.h>
#include <pcl/registration/transforms.h>

#include <pcl/visualization/pcl_visualizer.h>

typedef pcl::PointXYZ PointT;
typedef pcl::PointCloud<PointT> PointCloud;
typedef pcl::PointNormal PointNormalT;
typedef pcl::PointCloud<PointNormalT> PointCloudWithNormals;

int main()
{

char *file1="/home/wenqing/Desktop/results/Teapot_V2/transformed_CAM-Depth_0335.pcd";
char *file2="/home/wenqing/Desktop/results/Teapot_V2/transformed_CAM-Depth_0336.pcd";
//char *file1="/home/sgk333/Documents/DR/milk.pcd";
//char *file2="/home/sgk333/Documents/DR/milk_cartoon_all_small_clorox.pcd"
int min_sample_distance=10;
int max_correspondence_distance=10;
int nr_iterations=10;
int distance=1;
int transformation_epsilon=1e-6;
int max_iterations=10;
PointCloud::Ptr source_points(new PointCloud), target_points(new PointCloud);
pcl::io::loadPCDFile (file1, *source_points);
pcl::io::loadPCDFile (file2, *target_points);

pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
ne.setInputCloud (source_points);

  // Create an empty kdtree representation, and pass it to the normal estimation object.
  // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ> ());
ne.setSearchMethod (tree);

  // Output datasets
pcl::PointCloud<pcl::Normal>::Ptr source_descriptors(new pcl::PointCloud<pcl::Normal>);

  // Use all neighbors in a sphere of radius 3cm
  //ne.setRadiusSearch (0.001);
  ne.setKSearch (30);
  // Compute the features
  ne.compute (*source_descriptors);


ne.setInputCloud (target_points);

  // Create an empty kdtree representation, and pass it to the normal estimation object.
  // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
ne.setSearchMethod (tree);

  // Output datasets
pcl::PointCloud<pcl::Normal>::Ptr target_descriptors(new pcl::PointCloud<pcl::Normal>);

  // Use all neighbors in a sphere of radius 3cm
  //ne.setRadiusSearch (0.03);
  ne.setKSearch (30);
  // Compute the features
  ne.compute (*target_descriptors);

printf("Initial Alignment");
pcl::SampleConsensusInitialAlignment<PointT, PointT,pcl::Normal> sac;
sac.setMinSampleDistance (min_sample_distance);
sac.setMaxCorrespondenceDistance (max_correspondence_distance);
sac.setMaximumIterations (nr_iterations);
sac.setInputCloud (source_points);

sac.setSourceFeatures (source_descriptors);
sac.setInputTarget (target_points);
sac.setTargetFeatures (target_descriptors);
PointCloud::Ptr aligned_source(new PointCloud);
sac.align (*aligned_source);
Eigen::Matrix4f initial_T = sac.getFinalTransformation();
pcl::io::savePCDFile ("initial.pcd",*aligned_source, true);

printf("Iterative closest point");
pcl::IterativeClosestPoint<PointT, PointT> icp;
//icp.setMaxCorrespondenceDistance (distance);
//icp.setRANSACOutlierRejectionThreshold (distance);
//icp.setTransformationEpsilon (transformation_epsilon);
icp.setMaximumIterations (max_iterations);
icp.setInputCloud (aligned_source); // from (1)
icp.setInputTarget (target_points);
PointCloud registration_output;
icp.align (registration_output);
Eigen::Matrix4f refined_T =icp.getFinalTransformation () * initial_T;
pcl::io::savePCDFile ("registered.pcd",registration_output, true);
return 0;
}
