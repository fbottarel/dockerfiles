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

import jinja2
from jinja2 import Template

from plumbum import cli
from plumbum.cmd import rm
import yaml

import glom


log = logging.getLogger()


class Manager(cli.Application):
    """CUDA CI Manager"""

    PROGNAME = "manager.py"
    VERSION = "0.0.1"

    manifest = None
    ci = None
    changed = False

    # FIXME: implement dry-run
    #  dry_run = cli.Flag(["--dry-run"], help="Run without making changes")

    def _load_manifest_yaml(self):
        with open("manifest.yaml", "r") as f:
            self.manifest = yaml.load(f, yaml.Loader)
            #  import pprint

            #  pprint.pprint(self.manifest)

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
        #  self._check_for_changes()
        #  if self.changed:
        #  self.triggered()

        # rgx = re.compile(r"^(\w+)-v([\d\.]+)")
        # for key in self.ci:
        #     match = rgx.match(key)
        #     if match and len(match.groups()) > 1:
        #         print(match.group(1), match.group(2))


@Manager.subcommand("check")
class ManagerCheck(Manager):
    DESCRIPTION = "Check for changes."

    def main(self):
        pass


@Manager.subcommand("generate")
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    distro = cli.SwitchAttr(
        "--os",
        str,
        help="The distro to generate Dockerfiles for",
        default=None,
        mandatory=True,
    )

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None, mandatory=True
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        help="The cuda version to generate scripts for. Example: '10.1'",
        default=None,
        mandatory=True,
    )

    cuda = {}
    output_path = {}

    def write_dockerfile(self, template_path, output_path):
        with open(template_path) as f:
            dockerfile_output_path = pathlib.Path(output_path)
            template = Template(f.read())
            if not dockerfile_output_path.exists():
                log.debug(f"Creating {dockerfile_output_path}")
                dockerfile_output_path.mkdir(parents=True)
            log.info(f"Writing {dockerfile_output_path}/Dockerfile")
            with open(f"{dockerfile_output_path}/Dockerfile", "w") as f2:
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

    def generate_dockerscripts(self):
        for img in ["base", "devel", "runtime"]:
            # cuda image
            self.write_dockerfile(
                template_path=f"{self.distro}/{img}/Dockerfile.jinja",
                output_path=f"{self.output_path}/{img}",
            )
            # copy files
            for filename in pathlib.Path(f"{self.distro}/{img}").glob("*.*[!jinja]"):
                log.info(f"Copying {filename} to {self.output_path}/{img}")
                shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            if img in ["runtime", "devel"]:
                self.cuda["cudnn7"]["target"] = img
                self.write_dockerfile(
                    template_path=f"{self.distro}/cudnn7/Dockerfile.jinja",
                    output_path=f"{self.output_path}/{img}/cudnn7",
                )

    def generate_testscripts(self):
        for filename in pathlib.Path("test").glob("*/*.jinja"):
            self.write_test(filename, f"{self.output_path}/test")

    def main(self):
        log.debug("Have distro: %s version: %s", self.distro, self.distro_version)
        target = f"{self.distro}{self.distro_version}"
        self.output_path = pathlib.Path(f"build/{target}")
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
