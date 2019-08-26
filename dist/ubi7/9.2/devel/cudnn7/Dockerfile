ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-devel-ubi7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.3.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=d72d276d2e15cbf443fa1f1041a6457a0b238cb321eee36fe80638791f059007 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.3/cudnn-9.2-linux-x64-v7.6.3.30.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.2-linux-x64-v7.6.3.30.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.2-linux-x64-v7.6.3.30.tgz -C /usr/local && \
    rm cudnn-9.2-linux-x64-v7.6.3.30.tgz && \
    ldconfig
