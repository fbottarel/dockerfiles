# ====================================
# Build command.
# Change the starting image for the recipe if needed
# ====================================

docker build \
    --build-arg from=ubuntu:bionic \
    --rm \
    --pull \
    -t fbottarel/simox .
