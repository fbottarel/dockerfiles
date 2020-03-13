# gpd_ros

The purpose of this directory is to host whatever is necessary to build and run a ROS Docker container to test the GPD algorithm on tabletop-segmented point clouds. **NO GPU ACCELERATION IS SUPPORTED AT THE MOMENT**. This will not work if you have an nvidia graphics card active.

### Usage

1. Use the `build_image.sh` shell script to locally build the image. At the moment, the image has lots of excess fat and weighs around 5 gigs. I am absolutely sure that it can be trimmed down a lot, but at the moment it shall do. You can skip the build phase if you wish, the image is already compiled and ready to download on DockerHub.

2. Use the `run.sh` script to run the X11 accelerated container. Foolproof.

3. To open additional shells in the container, use `docker exec -it gpd-ros-container bash`. This container features a full ROS desktop installation, so you can use stuff like RViz, Gazebo, moveIT!, rqt, and such.

4. Build the catkin workspace and the two packages included. The first compiled package is the ROS wrapper for GPD, the other is a custom tabletop point cloud segmentation node.
```
$ cd /home/melodic-dev/catkin_ws
$ catkin_make
$ source devel/setup.bash
```
5. You can attach to a running ROS master in the same network by setting the master IP inside the container shell `export ROS_MASTER_URI=http://[master_ip_here]`.

6. Make sure you have scene point clouds being published to some topic. In case you have a RealSense camera connected to some machine, run its ROS node. `roslaunch realsense2_camera rs_camera.launch filters:=pointcloud`. It will publish point clouds on topic `/camera/depth/color/points`.

6. Spin up the gpd_ros and segmentation nodes (remapping the input cloud topic if you are running a realsense)
```
roslaunch gpd_ros gpd_ros_segmented_pc.launch
rosrun tabletop_segment tabletop_segment_node input_cloud:=/camera/depth/color/points
```
7. You can visualize the output with the .rviz file included in `/home/melodic-dev/catkin_ws/gpd_ros/visualization.rviz`. Below is a sample of what you should see in RViz.

[![Screenshot from 2020-03-05 11-58-18](https://user-images.githubusercontent.com/33027628/75975712-4f536100-5ed9-11ea-92c1-0c6036415d3d.png)](https://www.youtube.com/watch?v=ZrfUKIUpgSA)
