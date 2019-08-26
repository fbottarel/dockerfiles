ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.0-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.3.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=e19e156a10f6ccd57e3323cdb38290ac7c786907c669283130dc2b8a47fbf83b && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.3/cudnn-10.0-linux-x64-v7.6.3.30.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.0-linux-x64-v7.6.3.30.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.0-linux-x64-v7.6.3.30.tgz -C /usr/local && \
    rm cudnn-10.0-linux-x64-v7.6.3.30.tgz && \
    ldconfig
