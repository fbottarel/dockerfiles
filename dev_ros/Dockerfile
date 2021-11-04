ARG from=ubuntu:bionic
ARG ros_distro=melodic

FROM ${from}

MAINTAINER Fabrizio Bottarel <fabrizio.bottarel@iit.it>

# ======================================
# Docker image arguments
# ======================================

ARG ros_distro

# ======================================
# Set up some basic packages
# ======================================

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    nano \
    curl \
    lsb-release \
    wget \
    unzip \
    locales \
    software-properties-common \
    tree \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# ======================================
# Set up locales
# ======================================

RUN sed -i 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen && \
    locale-gen &&\
    update-locale LANG="en_US.UTF-8"

# ======================================
# Set up development stuff
# ======================================

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gdb \
    cmake \
    cmake-curses-gui \
    python \
    python-pip

# ======================================
# Setup HW Acceleration for Intel graphic cards
# ======================================

    RUN apt-get update &&\
        apt-get install -y \
            libgl1-mesa-glx \
            libgl1-mesa-dri &&\
        rm -rf /var/lib/apt/lists/*

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
    python-catkin-tools \
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init && \
    rosdep update

RUN apt-get update && apt-get install -y \
    ros-${ros_distro}-desktop-full \
    && rm -rf /var/lib/apt/lists/*

ENV ROS_DISTRO ${ros_distro}

# ======================================
# Set up sudo user (don't do this if you don't want a sudo user)
# ======================================

#Add new sudo user
# ENV USERNAME fbottarel
# RUN useradd -m $USERNAME && \
#         echo "$USERNAME:$USERNAME" | chpasswd && \
#         usermod --shell /bin/bash $USERNAME && \
#         usermod -aG sudo $USERNAME && \
#         echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME && \
#         chmod 0440 /etc/sudoers.d/$USERNAME && \
#         # Replace 1000 with your user/group id
#         usermod  --uid 1000 $USERNAME && \
#         groupmod --gid 1000 $USERNAME

# ======================================
# Other stuff
# ======================================

# Some QT-Apps/Gazebo don't show controls without this
ENV QT_X11_NO_MITSHM 1

# ======================================
# Setup an additional entrypoint script
# ======================================

COPY entrypoint.sh /usr/sbin/entrypoint.sh
COPY bashrc /root/.bashrc
RUN chmod 755 /usr/sbin/entrypoint.sh
ENTRYPOINT ["/usr/sbin/entrypoint.sh"]
CMD ["bash"]
