ARG IMAGE_NAME
FROM ${IMAGE_NAME}:9.2-runtime-ubi7
LABEL maintainer "NVIDIA CORPORATION <sw-cuda-installer@nvidia.com>"

ENV CUDNN_VERSION 7.6.4.38
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

# cuDNN license: https://developer.nvidia.com/cudnn/license_agreement
RUN CUDNN_DOWNLOAD_SUM=c79156531e641289b6a6952888b9637059ef30defd43c3cf82acf38d67f60a27 && \
    curl -fsSL http://developer.download.nvidia.com/compute/redist/cudnn/v7.6.4/cudnn-9.2-linux-x64-v7.6.4.38.tgz -O && \
    echo "$CUDNN_DOWNLOAD_SUM  cudnn-9.2-linux-x64-v7.6.4.38.tgz" | sha256sum -c - && \
    tar --no-same-owner -xzf cudnn-9.2-linux-x64-v7.6.4.38.tgz -C /usr/local --wildcards 'cuda/lib64/libcudnn.so.*' && \
    rm cudnn-9.2-linux-x64-v7.6.4.38.tgz && \
    ldconfig
