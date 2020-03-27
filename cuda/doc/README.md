## NVIDIA CUDA

[![build status](https://gitlab.com/nvidia/container-images/cuda/badges/master/pipeline.svg)](https://gitlab.com/nvidia/container-images/cuda/commits/master)

CUDA is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical processing units (GPUs). With CUDA, developers can dramatically speed up computing applications by harnessing the power of GPUs.

The CUDA Toolkit from NVIDIA provides everything you need to develop GPU-accelerated applications. The CUDA Toolkit includes GPU-accelerated libraries, a compiler, development tools and the CUDA runtime.

The CUDA container images on Docker Hub provide an easy-to-use distribution for CUDA supported platforms and architectures.

*Maintained by the NVIDIA CUDA Installer Team*

### NVIDIA License Agreements

By downloading these images, you agree to the terms of the license agreements for NVIDIA software included in the images.

#### CUDA Toolkit License

To view the license for the CUDA Toolkit included in this image, click [*here*](http://docs.nvidia.com/cuda/eula/index.html)

#### cuDNN Toolkit

To view the license for the cuDNN Toolkit included in this image, click [*here*](https://docs.nvidia.com/deeplearning/sdk/cudnn-sla/index.html)

### NVIDIA Container Runtime

The [NVIDIA Container Runtime](https://github.com/NVIDIA/nvidia-docker) for Docker is required to run CUDA images.

For CUDA 10.0, nvida-docker2 or greater is required. Older versions of the NVIDIA runtime work but an un-supported.

### How to report a problem

Read [NVIDIA Container Runtime Frequently Asked Questions](https://github.com/NVIDIA/nvidia-docker/wiki/Frequently-Asked-Questions) to see if the problem has been encountered before.

After it has been determined the problem is not with the NVIDIA runtime, report an issue at the [CUDA Container Image Issue Tracker](https://github.com/NVIDIA/nvidia-docker/issues/new).

## Supported tags

Supported tags are updated to the latest CUDA and cuDNN versions. These tags are also periodically updated to fix CVE vulnerabilities.

For a full list of supported tags, click [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md).

## LATEST CUDA 10.2

### Ubuntu 18.04

- [`10.2-base`, `10.2-base-ubuntu18.04` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.2/base/Dockerfile)
- [`10.2-runtime`, `10.2-runtime-ubuntu18.04` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime`, `10.2-cudnn7-runtime-ubuntu18.04` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.2/runtime/cudnn7/Dockerfile)
- [`latest`, `10.2-devel`, `10.2-devel-ubuntu18.04` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel`, `10.2-cudnn7-devel-ubuntu18.04` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu18.04/10.2/devel/cudnn7/Dockerfile)

### Ubuntu 16.04

- [`10.2-base-ubuntu16.04` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.2/base/Dockerfile)
- [`10.2-runtime-ubuntu16.04` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime-ubuntu16.04` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.2/runtime/cudnn7/Dockerfile)
- [`10.2-devel-ubuntu16.04` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel-ubuntu16.04` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubuntu16.04/10.2/devel/cudnn7/Dockerfile)

### Red Hat UBI 8

- [`10.2-base-ubi8` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi8/10.2/base/Dockerfile)
- [`10.2-runtime-ubi8` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi8/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime-ubi8` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi8/10.2/runtime/cudnn7/Dockerfile)
- [`10.2-devel-ubi8` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi8/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel-ubi8` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi8/10.2/devel/cudnn7/Dockerfile)

### Red Hat UBI 7

- [`10.2-base-ubi7` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi7/10.2/base/Dockerfile)
- [`10.2-runtime-ubi7` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi7/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime-ubi7` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi7/10.2/runtime/cudnn7/Dockerfile)
- [`10.2-devel-ubi7` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi7/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel-ubi7` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/ubi7/10.2/devel/cudnn7/Dockerfile)

### Centos 7

- [`10.2-base-centos7` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos7/10.2/base/Dockerfile)
- [`10.2-runtime-centos7` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos7/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime-centos7` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos7/10.2/runtime/cudnn7/Dockerfile)
- [`10.2-devel-centos7` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos7/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel-centos7` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos7/10.2/devel/cudnn7/Dockerfile)

### Centos 6

- [`10.2-base-centos6` (*10.2/base/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos6/10.2/base/Dockerfile)
- [`10.2-runtime-centos6` (*10.2/runtime/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos6/10.2/runtime/Dockerfile)
- [`10.2-cudnn7-runtime-centos6` (*10.2/runtime/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos6/10.2/runtime/cudnn7/Dockerfile)
- [`10.2-devel-centos6` (*10.2/devel/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos6/10.2/devel/Dockerfile)
- [`10.2-cudnn7-devel-centos6` (*10.2/devel/cudnn7/Dockerfile*)](https://gitlab.com/nvidia/container-images/cuda/blob/master/dist/centos6/10.2/devel/cudnn7/Dockerfile)

### Unsupported tags

A list of tags that are no longer supported can be found [*here*](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/unsupported-tags.md)

### How to contribute

Contributing to the CUDA Container Image sources would require you sign and submit a Contributor License Agreement to NVIDIA.

An example of the CLA can be seen at https://gitlab.com/nvidia/container-toolkit/nvidia-docker/blob/master/CONTRIBUTING.md

### Source of this description

This [Readme](https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/README.md) is located in the `doc` directory of the CUDA Container Image source repository. ([history](https://gitlab.com/nvidia/container-images/cuda/commits/master/doc/README.md))
