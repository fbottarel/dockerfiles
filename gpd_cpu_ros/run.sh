#!/bin/bash

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
touch $XAUTH
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -

# docker run -it --rm \
#   --net=host \
#   --privileged \
#   --user=melodic-dev \
#   --workdir=/home/melodic-dev \
#   -e DISPLAY=$DISPLAY \
#   -e QT_GRAPHICSSYSTEM=native \
#   -e QT_X11_NO_MITSHM=1 \
#   -v "/tmp/.X11-unix:/tmp/.X11-unix" \
#   -v "/etc/group:/etc/group:ro" \
#   -v "/etc/passwd:/etc/passwd:ro" \
#   -v "/etc/shadow:/etc/shadow:ro" \
#   -v "/etc/sudoers.d:/etc/sudoers.d:ro" \
#   --device=/dev/dri:/dev/dri \
#   ros_gpd:dev

docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -e QT_GRAPHICSSYSTEM=native \
    -e QT_X11_NO_MITSHM=1 \
    --volume=$XSOCK:$XSOCK:rw \
    --volume=$XAUTH:$XAUTH:rw \
    --env="XAUTHORITY=${XAUTH}" \
    --device=/dev/dri/card0:/dev/dri/card0 \
    --net=host \
    --privileged \
    --name "gpd-ros-container" \
    ros_gpd:latest
