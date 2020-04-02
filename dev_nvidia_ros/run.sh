# ====================================
# Run command.
# Add --network=host and --privileged if connecting to other ROS nodes. This
# however somehow breaks GUIs like rViz and rqt if using GPUs.
# ====================================

docker run \
    -it \
    --init \
    --name="ros-container" \
    -e DISPLAY \
    -e QT_X11_NO_MITSHM=1 \
    -e USER_UID=1000 \
    -e USER_GID=1000 \
    -e USERNAME=ros-dev \
    -e XAUTORITY=/tmp/.rl.xauth \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v /tmp/.rl.xauth \
    --device /dev/dri \
    --gpus=all \
    --rm \
    fbottarel/ros:nvidia

# ====================================
# Alternative run script
# ====================================
#docker run --gpus all --init -it --device /dev/dri -e USER_UID=1000 -e USER_GID=1000 -e DISPLAY -e XAUTORITY=/tmp/.rl.xauth -v /tmp/.X11-unix:/tmp/.X11-unix:rw -v /tmp/.rl.xauth --rm fbottarel/ros:nvidia su -c "bash" ros-dev

# ====================================
# Once the script is running: 
# ====================================
# docker exec -it -u ros-dev ros-container bash
