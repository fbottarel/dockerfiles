ARG IMAGE_NAME
FROM ${IMAGE_NAME}:10.1-runtime-ubi8
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.2.24
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=afbfd6a61e774beb3851742452c007de4f65f8ec0592d583bc6806f8d386cd1f && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.2/cudnn-10.1-linux-x64-v7.6.2.24.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-10.1-linux-x64-v7.6.2.24.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-10.1-linux-x64-v7.6.2.24.tgz -C /usr/local --wildcards 'cuda/lib64/libcudnn.so.*' && \
    rm cudnn-10.1-linux-x64-v7.6.2.24.tgz && \
    ldconfig
