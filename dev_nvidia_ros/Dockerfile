ARG from=ubuntu:bionic
ARG ros_distro=melodic
ARG uid=1000
ARG gid=1000

FROM ${from}

MAINTAINER Fabrizio Bottarel <fabrizio.bottarel@iit.it>

# ======================================
# Docker image arguments
# ======================================

ARG ros_distro
ARG uid
ARG gid
ARG username=${ros_distro}-dev

# ======================================
# Set up locales
# ======================================

RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && apt-get install -q -y tzdata && rm -rf /var/lib/apt/lists/*

# ======================================
# Set up some basic packages
# ======================================

RUN apt-get update && apt-get install -y \
    nano \
    curl \
    lsb-release \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# ======================================
# Set up development stuff
# ======================================

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    cmake-curses-gui \
    python \
    python-pip

# ======================================
# Set up ROS full desktop installation
# ======================================
# From https://github.com/osrf/docker_images/blob/master/ros/melodic/ubuntu/bionic/ros-core/Dockerfile
# ======================================

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list

RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init && \
    rosdep update

RUN apt-get update && apt-get install -y \
    ros-${ros_distro}-desktop-full \
    && rm -rf /var/lib/apt/lists/*

ENV ROS_DISTRO ${ros_distro}

# ======================================
# Set up non-root user (TENTATIVE)
# ======================================

RUN groupadd -f -g ${gid} ${username}

RUN adduser \
    --uid ${uid} \
    --gid ${gid} \
    ${username}

# ======================================
# Setup HW Acceleration for Intel graphic cards
# ======================================

RUN apt-get update &&\
    apt-get install -y \
        libgl1-mesa-glx \
        libgl1-mesa-dri \
        &&\
    rm -rf /var/lib/apt/lists/*

# ======================================
# Other stuff
# ======================================

# Some QT-Apps/Gazebo don't show controls without this
ENV QT_X11_NO_MITSHM 1

# ======================================
# Setup an additional entrypoint script
# ======================================

COPY entrypoint.sh /usr/sbin/entrypoint.sh
RUN chmod 755 /usr/sbin/entrypoint.sh
ENTRYPOINT ["/usr/sbin/entrypoint.sh"]
CMD ["bash"]
