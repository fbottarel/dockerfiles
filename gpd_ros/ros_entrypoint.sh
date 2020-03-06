#!/bin/bash
set -e

# setup ros environment
source "/opt/ros/$ROS_DISTRO/setup.bash"

# if catkin workspace is built, source the setup file
if [ -f ${CATKIN_WS}/devel/setup.bash ]; then
  source     ${CATKIN_WS}/devel/setup.bash
fi

export LD_LIBRARY_PATH="/usr/lib:/usr/local/lib:$LD_LIBRARY_PATH"

exec "$@"
