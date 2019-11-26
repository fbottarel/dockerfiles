#!/usr/bin/env bats

load helpers


image="${IMAGE_NAME}:10.2-devel-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

@test "check_LD_LIBRARY_PATH" {
    docker_run --rm --runtime=nvidia ${image} bash -c "printenv | grep -q 'LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64'"
    [ "$status" -eq 0 ]
}