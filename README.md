# Nvidia CUDA Linux Container Image Sources

Usage of the container images require the nvidia-docker v2 runtime.

Container images are available from:

- https://ngc.nvidia.com/catalog/containers/nvidia:cuda

- https://hub.docker.com/r/nvidia/cuda

## Building from source

The container image scripts are archived in the `dist/` directory and are available for all
supported distros and cuda versions.

Here is an example on how to build an image set for ubuntu16.04 and CUDA 9.0,

```bash
#/bin/bash

export IMAGE_NAME="nvidia/cuda"
export CUDA_VERSION="9.0"
export OS="ubuntu16.04"

docker build -t "${IMAGE_NAME}:${CUDA_VERSION}-base-${OS}" "dist/${OS}/${CUDA_VERSION}/base"
docker build -t "${IMAGE_NAME}:${CUDA_VERSION}-runtime-${OS}" --build-arg "IMAGE_NAME=${IMAGE_NAME}" "dist/${OS}/${CUDA_VERSION}/runtime"
docker build -t "${IMAGE_NAME}:${CUDA_VERSION}-devel-${OS}" --build-arg "IMAGE_NAME=${IMAGE_NAME}" "dist/${OS}/${CUDA_VERSION}/devel"
```

## manager.py

The python script is used to generate container sources and tests from templates.

### Setup

1. Install poetry. See https://poetry.eustace.io/docs/#installation

1. Install the dependencies with `poetry install`

1. Enter the virtual environment with `poetry shell`

Once in the virtual environment, run the script with:


```
python manager.py
```

## Triggering pipelines

Pipelines can be triggered automatically or explicitly via commit message.

The pipeline mechanism used for this project within gitlab is a workround [until multiple pipelines per gitlab-ci.yaml file is implemented in gitlab.](https://gitlab.com/gitlab-org/gitlab-ce/issues/22972)

### dry-run

To run the pipeline without publishing to the registries indicated in `manifest.yml`:

1. Go to the [pipelines](https://gitlab.com/nvidia/cuda/pipelines) page and click "Run Pipeline".

1. Input variable should be "DRY_RUN"; set it to "1" or whatever. It just needs to be set.

1. Click "Run Pipeline"

### Automatic triggering

By default on the master branch, the manifest.yaml file is compared against the previous version from the last commit. The changed keys within the manifest are then used to trigger builds via the gitlab api.

### Explicit triggering

Pipeline triggering can be overridden via the git commit message with:

```
ci.trigger = <pipeline>[,...]
```

Where pipeline can be:

- `all`: All of the pipelines are built.
- `<distro><distro_version>_cuda<major>_<minor>`: A specific cuda version for a specific cuda version.
- **TODO**: `<distro><distro_version>`: all cuda versions for a distro version.
- **TODO**: `cuda<major>_<minor>`: A cuda version for all distros.
- **TODO**: `cudnn<version>`: A cudnn version for all distros.

## manifest.yaml

Configuration of Dockerfile and Test output for the numerous platforms and architectures supported by CUDA Docker is defined in manifest.yaml.

### Image definition

To define a new image:

```
ubi7:
  template_path: redhat
  cuda:
    repo_url: "http://developer.download.nvidia.com/compute/cuda/repos/rhel6/x86_64"
    v10.0:
      build_version: 130
      cuda_requires: "brand=tesla,driver>=384,driver<385 brand=tesla,driver>=410,driver<411"
      cudnn7:
        version: "7.6.0.64"
        sha256sum: "c4e1ee4168f4cadabaa989487a47bed09f34d34e35398b6084a2699d11bd2560"
```

Notable keys:

* **template_path**: The path to search in for templates for this image. The path should be in the same directory as manager.py.

* **cuda**: Controls the versions of cuda supported by this image definition. It is possible to define multiple cuda versions as well as multiple cudnn versions.

* **repo_url**: A variable used in the container source templates.

And to generate the image:

```
python manager.py generate --os ubi --os-version 7 --cuda-version 10.1
```

### Container Push Repos

The container repos that manager.py can push are defined on a global level and can be excluded on a image level.

If `only_if` is defined on the repo object in manifest.yaml, manager.py will only use that repo if the defined value is also present in the global environment. For example:

```
docker_repos:
  docker.io:
    only_if: REGISTRY_TOKEN
```

will result in manager.py pushing to docker.io only if the `REGISTRY_TOKEN` global variable is defined in the environment.

#### Excluding push repos based on image

If an image root object in `manifest.yaml` contains the `exclude_repos` key, then manager.py will not push to that repo for that image. For example,

```
ubi7:
  base_image: registry.access.redhat.com/ubi7/ubi:latest
  exclude_repos:
    - docker.io
```

manager.py will not push the UBI-7 images to docker.io.
