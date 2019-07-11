#!/usr/bin/env bats

load helpers

image="${IMAGE_NAME}:10.1-base-${OS}${IMAGE_TAG_SUFFIX}"

function setup() {
    check_runtime
}

function teardown() {
    cleanup
}

@test "nvidia-smi" {
    docker_run --rm --runtime=nvidia ${image} nvidia-smi
    [ "$status" -eq 0 ]
}