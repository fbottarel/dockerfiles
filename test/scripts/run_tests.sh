#!/bin/bash

set -x
set -e

# run tests one by one in the remote tests directory.

cp "test/helpers.bash" "build/${OS}/${CUDA_VERSION}/test/"

for test in $(find "build/${OS}/${CUDA_VERSION}/test/" -iname "*.bats"); do
  dir=$(dirname ${test})
  name=$(basename ${test})
  curDir=${PWD}
  cd ${dir}
  echo "# Running test script '${test}'"
  /usr/local/bin/bats --tap ${name}
  cd ${curDir}
done
