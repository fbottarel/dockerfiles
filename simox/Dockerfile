ARG from=ubuntu:bionic

FROM ${from}

MAINTAINER Fabrizio Bottarel <fabrizio.bottarel@iit.it>

# ======================================
# Docker image arguments
# ======================================

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
    cmake-curses-gui

RUN apt install -y python3 python3-dev python3-pip python3-setuptools
RUN pip3 install --upgrade pip

# ======================================
# Setup HW Acceleration for Intel graphic cards
# ======================================

RUN apt-get update &&\
    apt-get install -y \
        libgl1-mesa-glx \
        libgl1-mesa-dri && \
    rm -rf /var/lib/apt/lists/*

# ======================================
# Set up Simox and its dependencies
# ======================================

# Select global compilation options
ARG BUILD_TYPE=Release

# Install Simox dependencies (Qt4)
RUN apt-get update && apt-get install -y build-essential \
                    libboost-all-dev \
                    libeigen3-dev \
                    libsoqt4-dev \
                    libcoin80-dev \
                    cmake \
                    cmake-gui \
                    libqt4-dev \
                    libnlopt-dev

# Build simox v2.3.74
RUN git clone https://gitlab.com/Simox/simox.git

# build directory is versioned
RUN cd simox/build && \
    git checkout v2.3.74 && \
    cmake .. \
    -DCMAKE_BUILD_TYPE=$BUILD_TYPE -DSimox_USE_QT4=ON \
    -DSimox_BUILD_SimDynamics=OFF -DSimDynamics_USE_BULLET=OFF \
    -DSimDynamics_USE_BULLET_USE_GLU=OFF && \
    make -j8 install

ENV Simox_DIR /usr/local
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

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
