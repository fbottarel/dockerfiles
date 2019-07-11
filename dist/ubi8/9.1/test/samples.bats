
#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:9.1-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

function teardown() {
    cleanup
}

@test "deviceQuery" {
    cat <<EOF > Dockerfile
    FROM ${image}
    RUN dnf install -y make gcc-c++ git
    RUN git clone https://github.com/NVIDIA/cuda-samples.git
    WORKDIR cuda-samples/Samples/deviceQuery/
    RUN git checkout v9.2
    RUN make
    CMD ./deviceQuery
EOF
    docker_build -t "${image}-${BATS_TEST_NAME}" .
    docker_run --rm --runtime=nvidia ${image}-${BATS_TEST_NAME}
    [ "$status" -eq 0 ]
}

@test "vectorAdd {
    cat <<EOF > Dockerfile
    FROM $image
    RUN dnf install -y make gcc-c++ git
    RUN git clone https://github.com/NVIDIA/cuda-samples.git
    WORKDIR cuda-samples/Samples/vectorAdd_nvrtc
    RUN git checkout v9.2
    RUN make
    CMD ./vectorAdd_nvrtc
EOF
    docker_build -t "${image}-${BATS_TEST_NAME}" .
    docker_run --rm --runtime=nvidia ${image}-${BATS_TEST_NAME}
    [ "$status" -eq 0 ]
}

