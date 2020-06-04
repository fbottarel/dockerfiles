# ====================================
# Build command.
# Change the distro and starting image for the recipe if needed
# ====================================

docker build \
    --build-arg from=ubuntu:bionic \
    --rm \
    --pull \
    -t fbottarel/pytorch:cpu .
