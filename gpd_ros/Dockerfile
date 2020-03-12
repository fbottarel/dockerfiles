ARG ros_distro=melodic
ARG uid=1000
ARG gid=1000

FROM osrf/ros:${ros_distro}-desktop-full

ARG ros_distro
ARG uid
ARG gid

RUN apt-get update && apt-get install -y locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

RUN apt-get update && \
    apt-get -y install \
        software-properties-common \
        nano \
        curl \
        wget \
        sudo \
        unzip \
        libgl1-mesa-glx \
        libgl1-mesa-dri \
        mesa-utils \
        && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/${ros_distro}-dev && \
    echo "${ros_distro}-dev:x:${uid}:${gid}:Developer,,,:/home/${ros_distro}-dev:/bin/bash" >> /etc/passwd && \
    echo "${ros_distro}-dev:x:${gid}:" >> /etc/group && \
    echo "${ros_distro}-dev ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${ros_distro}-dev && \
    chmod 0440 /etc/sudoers.d/${ros_distro}-dev && \
    chown ${uid}:${gid} -R /home/${ros_distro}-dev

USER ${ros_distro}-dev
ENV HOME /home/${ros_distro}-dev
WORKDIR /home/${ros_distro}-dev
RUN mkdir -p catkin_ws/src
ENV CATKIN_WS /home/${ros_distro}-dev/catkin_ws

# Set up OpenCV dependencies
USER root
RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
RUN apt update
RUN apt-get install -y build-essential cmake unzip pkg-config \
    libjpeg-dev libpng-dev libtiff-dev
RUN apt-get install -y libjasper1 libjasper-dev \
        libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
        libxvidcore-dev libx264-dev libgtk-3-dev \
        libatlas-base-dev gfortran \
        && rm -rf /var/lib/apt/lists/*
USER ${ros_distro}-dev

# Clone and build OpenCV 3.4.x
RUN git clone https://github.com/opencv/opencv.git
WORKDIR /home/${ros_distro}-dev/opencv
RUN git checkout 3.4.9
RUN mkdir build
RUN cd build && cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D WITH_CUDA=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_JAVA=OFF \
    -D BUILD_opencv_python2=OFF \
    -D OPENCV_ENABLE_NONFREE=OFF \
    -D BUILD_EXAMPLES=OFF .. && sudo make -j8 install

WORKDIR /home/${ros_distro}-dev
RUN rm -rf opencv

# Compile and install GPD
RUN git clone https://github.com/fbottarel/gpd.git
WORKDIR /home/${ros_distro}-dev/gpd
RUN sed -i 's/\.\./\/home\/melodic-dev\/gpd/g' cfg/eigen_params.cfg
RUN sed -i 's/\/home\/andreas\/projects\/gpd/\/home\/melodic-dev\/gpd\/models/g' cfg/ros_eigen_params.cfg
RUN mkdir build && cd build && cmake .. && sudo make -j8 install

# Compile and install GPD ROS wrapper with custom stuff
WORKDIR /home/${ros_distro}-dev/catkin_ws/src
RUN git clone https://github.com/fbottarel/gpd_ros.git
COPY gpd_ros_segmented_pc.launch gpd_ros/launch/gpd_ros_segmented_pc.launch
COPY gpd_ros_segmented.rviz gpd_ros/rviz/gpd_ros_segmented.rviz

# Copy the tabletop_segment package
RUN git clone https://github.com/fbottarel/utility-ros-nodes.git
RUN cp -r utility-ros-nodes/src/tabletop_segment .
RUN rm -rf utility-ros-nodes

# Set up other stuff that probably needs to go elsewhere
WORKDIR /home/${ros_distro}-dev
COPY bashrc /home/${ros_distro}-dev/.bashrc

CMD ["bash"]
