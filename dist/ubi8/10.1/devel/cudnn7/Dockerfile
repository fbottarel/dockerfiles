ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-devel-ubi8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.1.34
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=9885e38e71fa9844b3e4fb7c7211af41b24c9f76a9014f9d5e1768ddff2087dc && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.1/cudnn-10.1-linux-x64-v7.6.1.34.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.1-linux-x64-v7.6.1.34.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.1-linux-x64-v7.6.1.34.tgz -C /usr/local && \
    rm cudnn-10.1-linux-x64-v7.6.1.34.tgz && \
    ldconfig
