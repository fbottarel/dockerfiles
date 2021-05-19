#!/usr/bin/env bash

# Expose the X server on the host.
# This only works if the user is root though!
# If we could create a runtime user, with the same UID/GID  we could get around this problem :)

sudo xhost +local:root
# --rm: Make the container ephemeral (delete on exit).
# -it: Interactive TTY.
# --gpus all: Expose all GPUs to the container.
docker run \
  -it \
  --gpus all \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  fbottarel/cpp:devel \
  bash

sudo xhost -local:root
