# Scripts for testing CUDA Docker

## Requirements

### Bash Automated Test System

https://github.com/bats-core/bats-core

See install script (mentioned below).

## Globals

Globals that are used by the tests scripts.

* `REGISTRY`: The docker image registry to use in the image names.

   Default is unset which the docker command resolves to hub.docker.com automatically when pushing
   or pulling.

* `REGISTRY_USER`: The user to login to the docker registry as.

   Default is nvcr.io

* `IMAGE_TAG`: The tag of the image being tested.

## Usage

### Setup

```sh
sudo test/scripts/bats_install.sh
```

### Usage

```sh
sudo test/scripts/run_tests.sh
```

## Running tests on AWS

### Install Terraform

```sh
wget https://releases.hashicorp.com/terraform/0.10.2/terraform_0.10.2_linux_amd64.zip
unzip terraform_0.10.2_linux_amd64.zip
export PATH="$PATH:$(pwd)"
cd /usr/bin && sudo ln -s /path/to/terraform terraform
```

Generate ssh keys in keys folder and name public key "aws_terraform.pub" and private key "aws_terraform"

```sh
export AWS_ACCESS_KEY_ID="***"
export AWS_SECRET_ACCESS_KEY="***"
cd ubuntu16.04
terraform init && terraform apply && terraform destroy -force
cd centos
terraform init && terraform apply && terraform destroy -force
```
