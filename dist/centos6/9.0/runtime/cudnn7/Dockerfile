ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.0-runtime-centos6
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.3.30
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=00b4664a36fca4778ed245fe766a13ececef94797720e15e24efcde02fc4c230 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.3/cudnn-9.0-linux-x64-v7.6.3.30.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.0-linux-x64-v7.6.3.30.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.0-linux-x64-v7.6.3.30.tgz -C /usr/local --wildcards 'cuda/lib64/libcudnn.so.*' && \
    rm cudnn-9.0-linux-x64-v7.6.3.30.tgz && \
    ldconfig
