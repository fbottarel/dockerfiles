ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.4.38
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=32091d115c0373027418620a09ebec3658a6bc467d011de7cdd0eb07d644b099 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.4/cudnn-10.1-linux-x64-v7.6.4.38.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.1-linux-x64-v7.6.4.38.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.1-linux-x64-v7.6.4.38.tgz -C /usr/local && \
    rm cudnn-10.1-linux-x64-v7.6.4.38.tgz && \
    ldconfig
