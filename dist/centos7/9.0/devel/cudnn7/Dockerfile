ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.0-devel-centos7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.4.38
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=8db78c3623c192d4f03f3087b41c32cb0baac95e13408b5d9dabe626cb4aab5d && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.4/cudnn-9.0-linux-x64-v7.6.4.38.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.0-linux-x64-v7.6.4.38.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.0-linux-x64-v7.6.4.38.tgz -C /usr/local && \
    rm cudnn-9.0-linux-x64-v7.6.4.38.tgz && \
    ldconfig
