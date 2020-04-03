# ====================================
# Run command.
# Add --network=host and --privileged if connecting to other ROS nodes
# ====================================

XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth

if [ ! -f $XAUTH ]
then
    xauth_list=$(xauth nlist :0 | sed -e 's/^..../ffff/')
    if [ ! -z "$xauth_list" ]
    then
        echo $xauth_list | xauth -f $XAUTH nmerge -
    else
        touch $XAUTH
    fi
    chmod a+r $XAUTH
fi

docker run \
    -it \
    --name="ros-container" \
    -e DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -e USER_UID=1000 \
    -e USER_GID=1000 \
    -e USERNAME=fbottarel \
    -e XAUTHORITY=${XAUTH} \
    --volume=$XSOCK:$XSOCK:rw \
    --volume=$XAUTH:$XAUTH:rw \
    --device /dev/dri \
    --gpus=all \
    --network=host \
    --privileged \
    --rm \
    fbottarel/ros:nvidia \
    bash

# ====================================
# Once the script is running:
# ====================================
# docker exec -it -u [user] ros-container bash
