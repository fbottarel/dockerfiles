ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-base-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

RUN yum install -y \
        cuda-libraries-$CUDA_PKG_VERSION \
cuda-nvtx-$CUDA_PKG_VERSION \
    libcublas10-10.2.1.243-1 \
    && \
    rm -rf /var/cache/yum/*