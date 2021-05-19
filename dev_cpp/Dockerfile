ARG from=ubuntu:focal

FROM ${from}

# Dependencies for glvnd and X11.
RUN apt-get update \
  && apt-get install -y -qq --no-install-recommends \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libxext6 \
    libx11-6 \
    glmark2 \
  && rm -rf /var/lib/apt/lists/*

# Set up cpp dev environment
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
  && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    nano \
    curl \
    cmake \
    cmake-curses-gui \
    wget \
    unzip \
    gcc \
    g++ \
  && rm -rf /var/lib/apt/lists/*

# Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
