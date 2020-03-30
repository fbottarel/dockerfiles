docker build \
    --build-arg from=nvidia/cudagl:10.0-devel-ubuntu18.04 \
    --build-arg ros-distro=melodic \
    --build-arg uid=$(id -u) \
    --build-arg gid=$(id -g) \
    --rm \
    --pull \
    -t fbottarel/ros:nvidia .
