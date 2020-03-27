ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.1-base-ubuntu16.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

ENV NCCL_VERSION 2.2.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    cuda-libraries-$CUDA_PKG_VERSION \
libnccl2=$NCCL_VERSION-1+cuda9.1 && \
    apt-mark hold libnccl2 && \
    rm -rf /var/lib/apt/lists/*