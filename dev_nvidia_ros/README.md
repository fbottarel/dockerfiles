Dockerfile for isolated ROS development environments. This docker image includes:

- A full desktop ROS installation
- `Python 2.7` + `pip`
- Build and development tools (`git`, `cmake`, `build-essentials`)
- x11 and OpenGL support for graphical interfaces running inside the container
- Hardware acceleration for both Intel and nVidia graphic cards
- Sudoer user created at runtime.

### Image size and tweaks
The full image (ROS desktop + nVidia CUDA development + OpenGL support) comes in at around 6 GBs, however features can be disabled in order to reduce image size and build time.

#### nVidia hardware support

If you don't have a nVidia card, you don't need most of the stuff in this image. Build the image starting from something lightweight like `ubuntu:bionic` or `ubuntu:xenial` and keep the Intel hardware acceleration.

If you need nVidia hardware support, I got your back. This image by default includes most stuff you might need, however you can scale back and reduce image size. The [nVidia image repos](https://gitlab.com/nvidia/container-images) feature plenty of choice:

- different versions of [CUDA](https://gitlab.com/nvidia/container-images/cuda), i.e. `base`, `runtime` or `devel` with CUDA 9 and 10
- different versions of [CUDA+OpenGL](https://gitlab.com/nvidia/container-images/cudagl)
- just [OpenGL](https://gitlab.com/nvidia/container-images/opengl) support

To change the base image file, change the line
```
--build-arg from=nvidia/cudagl:10.0-devel-ubuntu18.04 \
```
in `build.sh` to whatever suits your needs.

#### ROS

By changing the base ubuntu image, you can install any ROS distribution you might need. Just change the line
```
--build-arg ros_distro=melodic \
```
to fit your needs. I tested this with both Kinetic+Xenial and Melodic+Bionic.
If you do not need the full ROS installation you can change the instruction
```
RUN apt-get update && apt-get install -y \
    ros-${ros_distro}-desktop-full \
    && rm -rf /var/lib/apt/lists/*
```
Suitable options are
- `ros-${ros_distro}-desktop-full`
- `ros-${ros_distro}-desktop`
- `ros-${ros_distro}-ros-base`

### How to operate the image

Build the image first (change build-args if needed)
```
chmod a+x build.sh
./build.sh
```

and then create a container
```
chmod a+x
./run.sh `whoami` ros-container fbottarel/ros:nvidia
```

Docker will spin up a container, creating a user inside it with name, group-id and user-id corresponding to the host system current user. The run script also takes care of checking whether the container already exists in a stopped state and just needs to be spun up. It also creates a Xauthority file to ensure proper autentication.

Once the container is running, you can work on it with
```
docker exec -it -u `whoami` ros-container bash
```

You might want to mount different volumes. To do so, change or add paths with `--volume`.

Add or remove stuff to the `bashrc` before building the image if you need so.

You can start a ros master inside the container or use one somewhere in your local network. In this case, you will need to add the `--network=host` and `--privileged` flags to the `run.sh` and declare a `ROS_MASTER_URI` env variable in the shell. Without the flags, nodes running in the container will see the master but not the other way around.

### Credits
Thanks to [Diego Ferigo](https://github.com/diegoferigo) for the help! I stole most of this stuff from him, anyways.
