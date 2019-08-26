ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-devel-ubi8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.3.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=352557346d8111e2f954c494be1a90207103d316b8777c33e62b3a7f7b708961 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.3/cudnn-10.1-linux-x64-v7.6.3.30.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.1-linux-x64-v7.6.3.30.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.1-linux-x64-v7.6.3.30.tgz -C /usr/local && \
    rm cudnn-10.1-linux-x64-v7.6.3.30.tgz && \
    ldconfig
