ARG from=nvidia/cudagl:10.1-devel-ubuntu18.04

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
# Set up development packages
# ======================================

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gdb \
    cmake \
    cmake-curses-gui \
    python3 \
    python3-pip

# ======================================
# Install pytorch
# ======================================

RUN pip3 install torch==1.5.0+cu101 torchvision==0.6.0+cu101 -f https://download.pytorch.org/whl/torch_stable.html

# ======================================
# Setup an additional entrypoint script
# ======================================

COPY entrypoint.sh /usr/sbin/entrypoint.sh
RUN chmod 755 /usr/sbin/entrypoint.sh
ENTRYPOINT ["/usr/sbin/entrypoint.sh"]
CMD ["bash"]
