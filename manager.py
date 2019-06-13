#!/usr/bin/env python3

# @author Jesus Alvarez <sw-cuda-installer@nvidia.com>

"""Dockerfile template injector and pipeline trigger."""

# Dependencies:
# pip install pipenv
# pipenv install
# pipenv shell
# python manager.py

import re
import os
import pathlib
import logging
import logging.config
import shutil
import glob
import sys

import jinja2
from jinja2 import Template

from plumbum import cli
from plumbum.cmd import rm
import yaml

import glom

import docker


log = logging.getLogger()


class Manager(cli.Application):
    """CUDA CI Manager"""

    PROGNAME = "manager.py"
    VERSION = "0.0.1"

    manifest = None
    ci = None
    changed = False

    def _load_manifest_yaml(self):
        with open("manifest.yaml", "r") as f:
            self.manifest = yaml.load(f, yaml.Loader)

    def _load_ci_yaml(self):
        with open(".gitlab-ci.yml", "r") as f:
            self.ci = yaml.load(f, yaml.Loader)

    def _load_app_config(self):
        with open("manager-config.yaml", "r") as f:
            logging.config.dictConfig(yaml.safe_load(f.read())["logging"])

    def _config_check(self):
        """Check if the config has changed in the latest git commit"""
        pass

    def _load_yaml(self):
        """Load the manifest and gitlab ci yaml files"""
        self._load_manifest_yaml()
        self._load_ci_yaml()

    def triggered(self):
        """Triggers pipelines on gitlab"""
        pass

    def main(self):
        self._load_app_config()
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            log.error("No subcommand given!")
            print()
            self.help()
            return 1
        log.info("cuda ci manager start")
        self._load_yaml()


@Manager.subcommand("check")
class ManagerCheck(Manager):
    DESCRIPTION = "Check for changes."

    def main(self):
        # - python manager.py docker-login
        # - if [[ ! -z $NV_CI_INTERNAL ]]; then
        #     export IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}";
        #     docker login -u "gitlab-ci-token" -p "${CI_JOB_TOKEN}" "gitlab-master.nvidia.com:5005";
        #     fi
        # - if [[ ! -z $NVCR_TOKEN ]]; then
        #     docker login -u "\$oauthtoken" -p "${NVCR_TOKEN}" "nvcr.io/nvidian";
        #     fi
        # # Used on gitlab.com to push to docker hub
        # - if [[ ! -z $REGISTRY_TOKEN ]]; then
        #     docker login -u "${REGISTRY_USER}" -p "${REGISTRY_TOKEN}" "${REGISTRY}";
        #     fi
        pass


@Manager.subcommand("docker-push")
class ManagerDockerPush(Manager):
    DESCRIPTION = "Login and push to the docker registries"

    image_name = cli.SwitchAttr(
        "--image-name", str, help="The image name to tag", default=None, mandatory=True
    )

    distro = cli.SwitchAttr(
        "--os", str, help="The distro to use.", default=None, mandatory=True
    )

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None, mandatory=True
    )

    latest = cli.Flag("--push-latest", help="The distro version")
    dry_run = cli.Flag(["-n", "--dry-run"], help="Show output but don't do anything!")

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        help="The cuda version to use. Example: '10.1'",
        default=None,
        mandatory=True,
    )

    tag_suffix = cli.SwitchAttr(
        "--tag-suffix",
        str,
        help="The suffix to append to the tag name. Example 10.1-base-centos6<suffix>",
        default=None,
    )
    client = None
    repos = []
    tags = []

    def _docker_login(self):
        # FIXME: move metadata to manifest and simplify this function
        if os.getenv("NVCR_TOKEN"):
            registry = "nvcr.io/nvidian"
            if self.client.login(
                username="$oauthtoken",
                password=os.getenv("NVCR_TOKEN"),
                registry=registry,
            ):
                self.repos.append(registry)
                log.info("Logged into %s", registry)
        if os.getenv("REGISTRY_TOKEN"):
            registry = "docker.io"
            if self.client.login(
                username=os.getenv("REGISTRY_USER"),
                password=os.getenv("REGISTRY_TOKEN"),
                registry=registry,
            ):
                self.repos.append(registry)
                log.info("Logged into %s", registry)
        if os.getenv("NV_CI_INTERNAL"):
            registry = "gitlab-master.nvidia.com:5005"
            if self.client.login(
                username="gitlab-ci-token",
                password=os.getenv("CI_JOB_TOKEN"),
                registry=registry,
            ):
                self.repos.append(registry)
                log.info("Logged into %s", registry)
        if not self.repos:
            log.fatal(
                "Docker login failed! Did not log into any repositories. Environment not set?"
            )
            sys.exit(1)

    def _push_images(self):
        for img in self.client.images.list(
            name=self.image_name, filters={"dangling": False}
        ):
            log.info("Processing image: %s, id: %s", img.tags, img.short_id)
            match = all(
                key in str(img.tags)
                for key in [
                    self.cuda_version,
                    f"{self.distro}{self.distro_version}",
                    self.tag_suffix,
                ]
            )
            if self.latest and "latest" in img.tags:
                match = True
            log.debug("tag: %s, match: %s", img, match)
            for repo in self.repos:
                tag = img.tags[0].split(":")[1]
                new_repo = "{}/{}".format(repo, img.tags[0].split(":")[0])
                if self.dry_run:
                    log.info(
                        "Tagged %s:%s (%s), %s", new_repo, tag, img.short_id, False
                    )
                    log.info("Would have pushed: %s:%s", new_repo, tag)
                else:
                    tagged = img.tag(new_repo, tag)
                    log.info(
                        "Tagged %s:%s (%s), %s", new_repo, tag, img.short_id, tagged
                    )
                    if tagged:
                        for line in self.client.images.push(
                            new_repo, tag, stream=True, decode=True
                        ):
                            log.info(line)

    def main(self):
        log.debug("dry-run: %s", self.dry_run)
        self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
        self._docker_login()
        self._push_images()
        log.info("Done")


@Manager.subcommand("generate")
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    cuda = {}
    output_path = {}

    distro = cli.SwitchAttr(
        "--os", str, help="The distro to use.", default=None, mandatory=True
    )

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None, mandatory=True
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        help="The cuda version to use. Example: '10.1'",
        default=None,
        mandatory=True,
    )

    def output_template(self, template_path, output_path):
        with open(template_path) as f:
            new_output_path = pathlib.Path(output_path)
            new_filename = template_path.name[:-6]
            template = Template(f.read())
            if not new_output_path.exists():
                log.debug(f"Creating {new_output_path}")
                new_output_path.mkdir(parents=True)
            log.info(f"Writing {new_output_path}/{new_filename}")
            with open(f"{new_output_path}/{new_filename}", "w") as f2:
                f2.write(template.render(cuda=self.cuda))

    def write_test(self, template_path, output_path):
        with open(template_path) as f:
            basename = template_path.name
            test_output_path = pathlib.Path(output_path)
            template = Template(f.read())
            if not test_output_path.exists():
                log.debug(f"Creating {test_output_path}")
                test_output_path.mkdir(parents=True)
            log.info(f"Writing {test_output_path}/{basename[:-6]}")
            with open(f"{test_output_path}/{basename[:-6]}", "w") as f2:
                f2.write(template.render(cuda=self.cuda))

    def build_cuda_dict(self):
        conf = self.parent.manifest
        major = self.cuda_version[:2]
        minor = self.cuda_version[3]
        build_version = glom.glom(
            conf,
            glom.Path(
                f"{self.distro}{self.distro_version}",
                "cuda",
                f"v{self.cuda_version}",
                "build_version",
            ),
        )
        self.cuda = {
            "tag_suffix": os.getenv("IMAGE_TAG_SUFFIX"),
            "repo_url": glom.glom(
                conf,
                glom.Path(f"{self.distro}{self.distro_version}", "cuda", "repo_url"),
            ),
            "version": {
                "full": f"{self.cuda_version}.{build_version}",
                "major": major,
                "minor": minor,
            },
            "requires": glom.glom(
                conf,
                glom.Path(
                    f"{self.distro}{self.distro_version}",
                    "cuda",
                    f"v{major}.{minor}",
                    "cuda_requires",
                ),
            ),
            "os": {"distro": self.distro, "version": self.distro_version},
            "arch": "x86_64",
            "cudnn7": {
                "version": glom.glom(
                    conf,
                    glom.Path(
                        f"{self.distro}{self.distro_version}",
                        "cuda",
                        f"v{major}.{minor}",
                        "cudnn7",
                        "version",
                    ),
                ),
                "sha256sum": glom.glom(
                    conf,
                    glom.Path(
                        f"{self.distro}{self.distro_version}",
                        "cuda",
                        f"v{major}.{minor}",
                        "cudnn7",
                        "sha256sum",
                    ),
                ),
                "target": "",
            },
        }
        log.debug("cuda version %s", glom.glom(self.cuda, glom.Path("version")))

    def generate_dockerscripts(self):
        for img in ["base", "devel", "runtime"]:
            # cuda image
            self.output_template(
                template_path=pathlib.Path(f"{self.distro}/{img}/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )
            # copy files
            for filename in pathlib.Path(f"{self.distro}/{img}").glob(
                "*[!Dockerfile].*"
            ):
                if ".jinja" in filename.name:
                    self.output_template(filename, f"{self.output_path}/{img}")
                else:
                    log.info(f"Copying {filename} to {self.output_path}/{img}")
                    shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            if img in ["runtime", "devel"]:
                self.cuda["cudnn7"]["target"] = img
                self.output_template(
                    template_path=pathlib.Path(
                        f"{self.distro}/cudnn7/Dockerfile.jinja"
                    ),
                    output_path=pathlib.Path(f"{self.output_path}/{img}/cudnn7"),
                )

    def supported_distro_list(self):
        rgx = re.compile(r"[a-z]+[\d+\.]+")
        ls = []
        for key in self.parent.manifest.keys():
            match = rgx.match(key)
            if match:
                ls.append(key)
        return ls

    def generate_testscripts(self):
        for filename in pathlib.Path("test").glob("*/*.jinja"):
            # Check for distro specific tests
            if any(distro in str(filename) for distro in self.supported_distro_list()):
                if not self.distro in str(filename):
                    continue
            self.write_test(filename, f"{self.output_path}/test")

    def main(self):
        log.debug("Have distro: %s version: %s", self.distro, self.distro_version)
        target = f"{self.distro}{self.distro_version}"
        self.output_path = pathlib.Path(f"build/{target}/{self.cuda_version}")
        if self.output_path.exists:
            log.debug(f"Removing {self.output_path}")
            rm["-rf", self.output_path]()
        log.debug(f"Creating {self.output_path}")
        self.output_path.mkdir(parents=True, exist_ok=False)
        self.build_cuda_dict()
        self.generate_dockerscripts()
        self.generate_testscripts()
        log.info("Done")


if __name__ == "__main__":
    Manager.run()
