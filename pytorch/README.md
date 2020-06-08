Dockerfile for isolated PyTorch development environments. This docker image includes:

- `Python 3` + `pip`
- Build and development tools (`git`, `cmake`, `build-essentials`)
- x11 and OpenGL support for graphical interfaces running inside the container
- Hardware acceleration for both Intel and nVidia graphic cards
- System-wide Pytorch installation
- Sudoer user created at runtime.


| | Base image  | Image name |
|-------------| ------------- | ------------- |
|[![](https://images.microbadger.com/badges/version/fbottarel/pytorch.svg)](https://microbadger.com/images/fbottarel/pytorch "Get your own version badge on microbadger.com")| `nvidia/cudagl:10.1-devel-ubuntu18.04`  | [fbottarel/pytorch:gpu](https://hub.docker.com/layers/fbottarel/pytorch/gpu/images/sha256-27f7c7b91ca7e4e95a3a0ba6ee8755fdebc6e6a1a14a2937c3891092b364914a?context=repo) |
|[![](https://images.microbadger.com/badges/version/fbottarel/pytorch:cpu.svg)](https://microbadger.com/images/fbottarel/pytorch:cpu "Get your own version badge on microbadger.com")| `ubuntu:bionic`  | [fbottarel/pytorch:cpu](https://hub.docker.com/layers/fbottarel/pytorch/cpu/images/sha256-89489b54e9583bfa4d85c3012326da00a0645fb73ddd208b80d8cbdea44cc8a3?context=repo)  |


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

### How to operate the image

Build the image first (change build-args if needed)
```
chmod a+x build.sh
./build.sh
```

and then create a container
```
chmod a+x
./run.sh `whoami` ros-container fbottarel/pytorch:cpu
```

Docker will spin up a container, creating a user inside it with name, group-id and user-id corresponding to the host system current user. The run script also takes care of checking whether the container already exists in a stopped state and just needs to be spun up. It also creates a Xauthority file to ensure proper autentication.

Once the container is running, you can work on it with
```
docker exec -it -u `whoami` pytorch bash
```

You might want to mount different volumes. To do so, change or add paths with `--volume`.

### Credits
Thanks to [Diego Ferigo](https://github.com/diegoferigo) for the help! I stole most of this stuff from him, anyways.
