docker run \
    -it \
    --name="ros-container" \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --gpus=all \
    --network=host \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --rm \
    fbottarel/ros:nvidia


#export containerId=$(docker ps -l -q)
#xhost +local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`
#docker start $containerId
#docker exec -it $containerId bash
#xhost -local:`docker inspect --format='{{ .Config.Hostname }}' $containerId`




#
# -e USER_UID=$(id -u) \
# -e USER_GID=$(id -g) \
# -e USERNAME=$(whoami) \
