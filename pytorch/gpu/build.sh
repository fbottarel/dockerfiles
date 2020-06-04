# ====================================
# Build command.
# Change the distro and starting image for the recipe if needed
# ====================================

docker build \
    --build-arg from=nvidia/cudagl:10.1-devel-ubuntu18.04 \
    --rm \
    --pull \
    -t fbottarel/pytorch:gpu .
