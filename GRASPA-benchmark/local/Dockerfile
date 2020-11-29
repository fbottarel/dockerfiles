FROM ubuntu:bionic
LABEL maintainer="fabrizio.bottarel@iit.it"

# Non-interactive installation mode
ENV DEBIAN_FRONTEND=noninteractive

# Update apt database
RUN apt update

# Install essentials
RUN apt install -y apt-utils software-properties-common sudo psmisc lsb-release \
                   tmux nano wget curl build-essential git gitk cmake cmake-curses-gui \
                   libedit-dev libxml2-dev autoconf mlocate

# Install graphics
RUN apt install -y xfce4 xfce4-goodies xserver-xorg-video-dummy xserver-xorg-legacy firefox
RUN sed -i 's/allowed_users=console/allowed_users=anybody/' /etc/X11/Xwrapper.config
COPY xorg.conf /etc/X11/xorg.conf

# We need the most recent x11vnc
RUN sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list && \
    apt update
RUN git clone https://github.com/LibVNC/x11vnc.git /opt/x11vnc && \
    cd /opt/x11vnc && \
    apt build-dep -y x11vnc && \
    autoreconf -fiv && \
    ./configure && \
    make && make install && \
    rm -Rf /opt/x11vnc

# Install terminator
RUN apt install -y terminator

# Install python3
#RUN add-apt-repository ppa:deadsnakes/ppa -y && \
#    apt dist-upgrade -y && \
RUN apt install -y python3 python3-dev python3-pip python3-setuptools
RUN pip3 install --upgrade pip

# Install websockify
RUN git clone https://github.com/novnc/websockify.git /opt/websockify && \
    cd /opt/websockify && git checkout v0.9.0 && \
    python3 setup.py install

# Clone noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/novnc
RUN echo "<html><head><meta http-equiv=\"Refresh\" content=\"0; url=vnc.html\"></head></html>" > /opt/novnc/index.html

# Select global compilation options
ARG BUILD_TYPE=Release

# Install Simox dependencies (Qt4)
RUN apt-get install -y build-essential libboost-all-dev libeigen3-dev libsoqt4-dev \
                        libcoin80-dev cmake cmake-gui libqt4-dev libnlopt-dev

# Build simox v2.3.74
RUN git clone https://gitlab.com/Simox/simox.git
# build directory is versioned
RUN cd simox/build && \
    git checkout v2.3.74 && \
    cmake .. \
    -DCMAKE_BUILD_TYPE=$BUILD_TYPE -DSimox_USE_QT4=ON \
    -DSimox_BUILD_SimDynamics=OFF -DSimDynamics_USE_BULLET=OFF \
    -DSimDynamics_USE_BULLET_USE_GLU=OFF && \
    make install
RUN rm -Rf simox

# Create environmental variable for simox
RUN export Simox_DIR=/usr/local

# Use the /workspace directory as entry point
RUN mkdir workspace
WORKDIR /workspace

# Clone the GRASPA benchmark repository (only for docker local)
RUN git clone https://github.com/robotology/GRASPA-benchmark
RUN mkdir GRASPA-benchmark/build && cd GRASPA-benchmark/build && \
    cmake .. && make install

# Install the Python packages (only for docker local)
RUN pip3 install -r GRASPA-benchmark/requirements.txt

# Clone the experiment data repository
RUN git clone https://github.com/robotology-playground/GRASPA-test.git

# Set up .bashrc for root user
RUN echo "alias python='/usr/bin/python3.6'" >> ~/.bashrc
RUN echo "PS1='\[\e]0;\u \w\a\]\[\033[01;32m\]\u\[\033[00m\] \[\033[01;34m\]\w\[\033[00m\] \$ '" >> ~/.bashrc
RUN echo "export GRASPA_DIR=/workspace/GRASPA-benchmark" >> ~/.bashrc
RUN echo "export GRASPA_TEST_DIR=/workspace/GRASPA-test/experiment_data/right_arm" >> ~/.bashrc
RUN echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib" >> ~/.bashrc

# Set environmental variables
ENV DISPLAY=:1

# Set up script to launch graphics and vnc
COPY start-vnc-session.sh /usr/bin/start-vnc-session.sh
RUN chmod +x /usr/bin/start-vnc-session.sh

# Manage x11vnc port
EXPOSE 5901

# Manage noVNC port
EXPOSE 6080

# Launch bash from workspace directory
CMD ["bash"]

# docker user must be take care of
# - clone benchmark repo
#RUN git clone https://github.com/robotology/GRASPA-benchmark
# - compile benchmark repo
#RUN mkdir GRASPA-benchmark/build && cd GRASPA-benchmark/build && \
#    cmake .. && make
# - install python packages
#RUN pip3 install -r GRASPA-benchmark/requirements.txt
# - clone benchmark test repo
#RUN git clone https://github.com/robotology-playground/GRASPA-test.git
# - create env variable for grasp experiment data
