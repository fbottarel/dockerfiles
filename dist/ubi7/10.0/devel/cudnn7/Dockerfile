ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.0-devel-ubi7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.2.24
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=86d87c426537a55dbdbe416b92f8afa1e49361a759c3d17f119e431767a88432 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.2/cudnn-10.0-linux-x64-v7.6.2.24.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.0-linux-x64-v7.6.2.24.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.0-linux-x64-v7.6.2.24.tgz -C /usr/local && \
    rm cudnn-10.0-linux-x64-v7.6.2.24.tgz && \
    ldconfig
