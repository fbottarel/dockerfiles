ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-devel-centos6
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.1.34
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=0d38735b06a1daf518c7ad4977fdb987a470f7793d95542ac9897e214ab1b006 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.1/cudnn-9.2-linux-x64-v7.6.1.34.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.2-linux-x64-v7.6.1.34.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.2-linux-x64-v7.6.1.34.tgz -C /usr/local && \
    rm cudnn-9.2-linux-x64-v7.6.1.34.tgz && \
    ldconfig
