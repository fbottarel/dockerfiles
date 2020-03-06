# gpd_ros

The purpose of this directory is to host whatever is necessary to build and run a ROS Docker container to test the GPD algorithm on tabletop-segmented point clouds. **NO GPU ACCELERATION IS SUPPORTED AT THE MOMENT**. This will not work if you have an nvidia graphics card active.

### Usage

1. Use the `build_image.sh` shell script to locally build the image. At the moment, the image has lots of excess fat and weighs around 5 gigs. I am absolutely sure that it can be trimmed down a lot, but at the moment it shall do. 

2. Use the `run.sh` script to run the X11 accelerated container. Foolproof.

3. To open additional shells in the container, use `docker exec -it gpd-ros-container bash`
