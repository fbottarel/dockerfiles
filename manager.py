#!/usr/bin/env python3

# @author Jesus Alvarez <sw-cuda-installer@nvidia.com>

"""Dockerfile template injector and pipeline trigger."""

#
# !! IMPORTANT !!
#
# Editors of this file should use https://github.com/python/black for auto formatting.
#

import re
import os
import pathlib
import logging
import logging.config
import shutil
import glob
import sys
import io

import jinja2
from jinja2 import Template
from plumbum import cli
from plumbum.cmd import rm
import yaml
import glom
import docker
import git
import deepdiff
import requests


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

    def _load_yaml(self):
        """Load the manifest and gitlab ci yaml files"""
        self._load_manifest_yaml()
        self._load_ci_yaml()

    def triggered(self):
        """Triggers pipelines on gitlab"""
        pass

    def cudnn_versions(self):
        obj = []
        for k, _ in self.cuda.items():
            if k.startswith("cudnn"):
                obj.append(k)
        return obj

    def supported_distro_list(self):
        rgx = re.compile(fr"([a-z]+)([\d+\.]+)?")
        ls = []
        for key in self.parent.manifest.keys():
            if rgx.match(key):
                ls.append(key)
        return ls

    def ci_distro_variables(self, distro):
        rgx = re.compile(fr"^\s+- \$(?!all)({distro}[\w]+) == \"true\"$")
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def main(self):
        self._load_app_config()
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            log.error("No subcommand given!")
            print()
            self.help()
            return 1
        log.info("cuda ci manager start")
        self._load_yaml()


@Manager.subcommand("trigger")
class ManagerTrigger(Manager):
    DESCRIPTION = "Trigger for changes."

    repo = None
    manifest_current = None
    manifest_previous = None
    changed = set()
    trigger_all = False
    trigger_explicit = []

    dry_run = cli.Flag(
        ["-n", "--dry-run"], help="Show output but don't make any changes."
    )

    def check_explicit_trigger(self):
        # FIXME: Need to unit test this!
        self.repo = git.Repo(pathlib.Path("."))
        commit = self.repo.commit("HEAD")
        rgx = re.compile(r"ci\.trigger = (.*)")
        log.debug("Commit message: %s", repr(commit.message))
        match = rgx.search(commit.message)
        if match:
            log.info("Explicit trigger found in commit message")
            pipeline = match.groups(0)[0].lower()
            if "all" in pipeline:
                log.info("Triggering ALL of the jobs!")
                self.trigger_all = True
                return True
            else:
                jobs = []
                jobs.append(pipeline)
                if "," in pipeline:
                    jobs = pipeline.split(",")
                for job in jobs:
                    if "_cuda" not in job:
                        for cvar in self.ci_distro_variables(job):
                            log.info("Triggering '%s'", cvar)
                            self.trigger_explicit.append(cvar)
                    else:
                        log.info("Triggering '%s'", job)
                        self.trigger_explicit.append(job)
                return True
        log.debug("No explicit trigger found in commit message.")
        return False

    def load_last_manifest(self):
        self.repo = git.Repo(pathlib.Path("."))
        # XXX: HEAD~1 would not work for merges...
        commit = self.repo.commit("HEAD~1")
        log.debug("getting previous manifest from git commit %s", commit.hexsha)
        blob = commit.tree / "manifest.yaml"
        with io.BytesIO(blob.data_stream.read()) as f:
            tf = f.read().decode("utf-8")
        self.manifest_previous = yaml.load(tf, yaml.Loader)

    def load_current_manifest(self):
        log.debug(
            "current manifest from git commit %s", self.repo.commit("HEAD").hexsha
        )
        with open("manifest.yaml", "r") as f:
            self.manifest_current = yaml.load(f, yaml.Loader)

    # Remove stuff we don't care about before compare. Typically yaml placeholders.
    def prune_objects(self):
        for manifest in [self.manifest_current, self.manifest_previous]:
            manifest.pop("redhat7")
            manifest.pop("redhat6")
            manifest.pop("docker_repos")

    # returns true if changes have been detected
    def deep_compare(self):
        rgx = re.compile(r"root\['([\w\.\d]*)'\]\['cuda'\]\['v(\d+\.\d+)")

        # Uncomment this to see the files being compared in the logs
        #  log.debug("manifest previous: %s", self.manifest_previous)
        #  log.debug("manifest current: %s", self.manifest_current)

        ddiff = deepdiff.DeepDiff(
            self.manifest_previous,
            self.manifest_current,
            verbose_level=0,
            exclude_paths=[
                "root['redhat6']",
                "root['redhat7']",
                "root['redhat8']",
                "root['docker_repos']",
            ],
        ).to_dict()

        if not ddiff:
            log.info("No changes detected! 🍺")
            return False

        #  from pprint import pprint

        #  pprint(self.manifest_previous)
        #  pprint(self.manifest_current)
        log.debug("Have ddif: %s", ddiff)

        items_added = ddiff.get("dictionary_item_added", None)
        items_removed = ddiff.get("dictionary_item_removed", None)
        items_changed = ddiff.get("values_changed", None)

        # FIXME: not DRY
        if items_added and items_removed:
            # parse added or removed items
            for obj in ddiff["dictionary_item_added"].union(
                ddiff["dictionary_item_removed"]
            ):
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))
        elif items_added:
            for obj in items_added:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))
        elif items_removed:
            for obj in items_removed:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))

        if items_changed:
            for obj in items_changed:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))

        log.debug("manifest root changes: %s", self.changed)
        return True

    def kickoff(self):
        url = os.getenv("CI_API_V4_URL")
        project_id = os.getenv("CI_PROJECT_ID")
        dry_run = os.getenv("DRY_RUN")
        token = os.getenv("CI_JOB_TOKEN")
        ref = os.getenv("CI_COMMIT_REF_NAME")
        payload = {"token": token, "ref": ref, "variables[TRIGGER]": "true"}
        if self.trigger_all:
            payload["variables[all]"] = "true"
        elif self.trigger_explicit:
            for job in self.trigger_explicit:
                payload[f"variables[{job}]"] = "true"
        else:
            for job in self.changed:
                payload[f"variables[{job}]"] = "true"
        if dry_run:
            payload[f"variables[DRY_RUN]"] = "true"
        log.debug("payload %s", payload)
        if not self.dry_run:
            r = requests.post(
                f"{url}/projects/{project_id}/trigger/pipeline", data=payload
            )
            log.debug("response status code %s", r.status_code)
            log.debug("response body %s", r.json())
        else:
            log.info("In dry-run mode so not making gitlab trigger POST")

    def main(self):
        if not self.check_explicit_trigger():
            self.load_last_manifest()
            self.load_current_manifest()
        if self.trigger_all or self.trigger_explicit or self.deep_compare():
            self.kickoff()


@Manager.subcommand("docker-push")
class ManagerDockerPush(Manager):
    DESCRIPTION = "Login and push to the docker registries"

    image_name = cli.SwitchAttr(
        "--image-name", str, help="The image name to tag", default="", mandatory=True
    )

    distro = cli.SwitchAttr(
        "--os", str, help="The distro to use.", default=None, mandatory=True
    )

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None, mandatory=True
    )

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
        default="",
    )
    client = None
    repos = []
    tags = []

    def docker_login(self):
        manifest = self.parent.manifest["docker_repos"]
        repo_excludes = []
        for repo in manifest:
            if manifest[repo].get("only_if", False) and not os.getenv(
                manifest[repo]["only_if"]
            ):
                log.debug("repo: '%s' only_if requirement not satisfied", repo)
                continue
            try:
                repo_excludes = glom.glom(
                    self.parent.manifest,
                    glom.Path(f"{self.distro}{self.distro_version}", "exclude_repos"),
                )
                if repo in repo_excludes:
                    log.debug("Repo %s has been excluded in the manifest!", repo)
                    continue
            except glom.PathAccessError:
                pass
            user = os.getenv(manifest[repo]["user"])
            passwd = os.getenv(manifest[repo]["pass"])
            if not user:
                user = manifest[repo]["user"]
            if not passwd:
                passwd = manifest[repo]["pass"]
            registry = manifest[repo]["registry"]
            if self.client.login(username=user, password=passwd, registry=registry):
                self.repos.append(registry)
                log.info("Logged into %s", registry)
        if not self.repos:
            log.fatal(
                "Docker login failed! Did not log into any repositories. Environment not set?"
            )
            sys.exit(1)

    # Check the image tag to see if it contains a suffix. This is used for special builds.
    # A tag with a suffix looks like:
    #
    #  10.0-cudnn7-devel-centos6-patched
    #  10.0-devel-centos6-patched
    #
    def _tag_contains_suffix(self, img):
        if len(img.tags) == 0:
            log.debug("img has no tags!")
            return False
        fields = img.tags[0].split(":")[1].split("-")
        is_cudnn = [s for s in fields if "cudnn" in s]
        if (is_cudnn and len(fields) > 4) or (not is_cudnn and len(fields) > 3):
            log.debug("tag contains suffix")
            return True
        elif len(fields) == 2 or f"{self.distro}{self.distro_version}" in fields[:-1]:
            log.debug("tag does not contain suffix")
            return False
        elif f"{self.distro}{self.distro_version}" in fields[:-1]:
            log.debug("tag contains suffix")
            return True
        log.debug("tag does not contain suffix")

    def _should_push_image(self, img):
        if len(img.tags) == 0:
            log.debug("img has no tags!")
            return False
        # Ensure the tag contains the target cuda version and distro version
        match = all(
            key in str(img.tags)
            for key in [self.cuda_version, f"{self.distro}{self.distro_version}"]
        )
        # If the tag has a suffix but we are not expecting one, then fail
        if not self.tag_suffix and self._tag_contains_suffix(img):
            log.debug("Tag suffix detected in image tag")
            match = False
        # All together now
        if (
            not match
            # ignore test images
            or "-test_" in str(img.tags)
            # a suffix is expected but the image does not contain what we expect
            or (self.tag_suffix and self.tag_suffix not in str(img.tags))
        ):
            return False
        return True

    def push_images(self):
        for img in self.client.images.list(
            name=self.image_name, filters={"dangling": False}
        ):
            log.debug("img: %s", str(img.tags))
            if not self._should_push_image(img):
                log.debug("Skipping")
                continue
            log.info("Processing image: %s, id: %s", img.tags, img.short_id)
            for repo in self.repos:
                for k, v in [[x, y] for tag in img.tags for (x, y) in [tag.split(":")]]:
                    print(k, v)
                    tag = v
                    new_repo = "{}/{}".format(repo, k)
                    if repo == "docker.io":
                        new_repo = k
                    if self.dry_run:
                        log.info(
                            "Tagged %s:%s (%s), %s", new_repo, tag, img.short_id, False
                        )
                        log.info("Would have pushed: %s:%s", new_repo, tag)
                        continue
                    tagged = img.tag(new_repo, tag)
                    log.info(
                        "Tagged %s:%s (%s), %s", new_repo, tag, img.short_id, tagged
                    )
                    if tagged:
                        # FIXME: only push if the image has changed
                        for line in self.client.images.push(
                            new_repo, tag, stream=True, decode=True
                        ):
                            log.info(line)

    def main(self):
        log.debug("dry-run: %s", self.dry_run)
        self.client = docker.DockerClient(
            base_url="unix://var/run/docker.sock", timeout=600
        )
        self.docker_login()
        self.push_images()
        log.info("Done")


@Manager.subcommand("generate")
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    cuda = {}
    output_path = {}

    generate_all = cli.Flag(
        ["all"],
        excludes=["--os", "--os-version", "--cuda-version", "--tag-suffix"],
        help="Generate all of the templates.",
    )

    distro = cli.SwitchAttr("--os", str, help="The distro to use.", default=None)

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        help="The cuda version to use. Example: '10.1'",
        default=None,
    )

    tag_suffix = cli.SwitchAttr(
        "--tag-suffix",
        str,
        help="The suffix to append to the tag name. Use for special builds. Example 10.1-base-centos6<suffix>",
        default="",
    )

    # extracts arbitrary keys and inserts them into the templating context
    def extract_keys(self, val):
        rgx = re.compile(r"^v\d+\.\d")
        for k, v in val.items():
            if rgx.match(k):
                # Do not copy cuda version keys
                continue
            # These top level keys should be ignored since they are processed elsewhere
            if k in ["cuda", "exclude_repos", "build_version"]:
                continue
            self.cuda[k] = v

    # For cudnn templates, we need a custom template context
    def output_cudnn_template(self, cudnn_version, template_path, output_path):
        new_ctx = {
            "cudnn": self.cuda[cudnn_version],
            "version": self.cuda["version"],
            "tag_suffix": self.cuda["tag_suffix"],
            "os": self.cuda["os"],
        }
        log.debug("cudnn template context: %s", new_ctx)
        self.output_template(
            template_path=template_path, output_path=output_path, ctx=new_ctx
        )

    def output_template(self, template_path, output_path, ctx=None):
        ctx = ctx if ctx is not None else self.cuda
        rgx = re.compile(r"^[\w]+-")
        # If the template path contains "{distro_name}-" and it does not match the target distro, skip the template
        if any(distro in template_path.name for distro in self.supported_distro_list()):
            if not rgx.match(template_path.name):
                # The template is for a specific distro and not the current target, so skip it
                log.debug(
                    "Skipping template '%s', distro requirement '%s' not met",
                    template_path,
                    self.distro,
                )
                return
        with open(template_path) as f:
            log.debug("Processing template %s", template_path)
            new_output_path = pathlib.Path(output_path)
            new_filename = template_path.name[:-6]
            if rgx.match(template_path.name):
                new_filename = template_path.name[len(f"{self.distro}-") : -6]
                log.debug("'%s' is renamed to '%s'", template_path.name, new_filename)
            template = Template(f.read())
            if not new_output_path.exists():
                log.debug(f"Creating {new_output_path}")
                new_output_path.mkdir(parents=True)
            log.info(f"Writing {new_output_path}/{new_filename}")
            with open(f"{new_output_path}/{new_filename}", "w") as f2:
                f2.write(template.render(cuda=ctx))

    def write_test(self, template_path, output_path):
        with open(template_path) as f:
            basename = template_path.name
            test_output_path = pathlib.Path(output_path)
            template = Template(f.read())
            if not test_output_path.exists():
                log.debug(f"Creating {test_output_path}")
                test_output_path.mkdir(parents=True)
            log.info(f"Writing {test_output_path}/{basename[:-6]}")
            log.debug("test template context: %s", self.cuda)
            with open(f"{test_output_path}/{basename[:-6]}", "w") as f2:
                f2.write(template.render(cuda=self.cuda))

    # Get data from a object by dotted path. Example "cuda."v10.0".cuda_requires"
    def get_data(self, obj, *path, can_skip=False):
        try:
            data = glom.glom(obj, glom.Path(*path))
        except glom.PathAccessError:
            if can_skip:
                return
            raise glom.PathAccessError
        return data

    def prepare_context(self):
        conf = self.parent.manifest
        major = self.cuda_version.split(".")[0]
        minor = self.cuda_version.split(".")[1]

        build_version = self.get_data(
            conf,
            f"{self.distro}{self.distro_version}",
            "cuda",
            f"v{self.cuda_version}",
            "build_version",
        )

        # The templating context. This data structure is used to fill the templates.
        self.cuda = {
            "version": {
                "full": f"{self.cuda_version}.{build_version}",
                "major": major,
                "minor": minor,
            },
            "os": {"distro": self.distro, "version": self.distro_version},
            "tag_suffix": self.tag_suffix,
        }

        # Users of manifest.yaml are allowed to set arbitrary keys for inclusion in the templates
        # and the discovered keys are injected into the template context.
        # We only checks at three levels in the manifest
        self.extract_keys(self.get_data(conf, f"{self.distro}{self.distro_version}"))
        self.extract_keys(
            self.get_data(conf, f"{self.distro}{self.distro_version}", "cuda")
        )
        self.extract_keys(
            self.get_data(
                conf, f"{self.distro}{self.distro_version}", "cuda", f"v{major}.{minor}"
            )
        )
        log.info("cuda version %s", glom.glom(self.cuda, glom.Path("version")))
        log.debug("template context %s", self.cuda)

    # CUDA 8 uses a deprecated image layout
    def generate_dockerscripts_cuda_8(self):
        for img in ["devel", "runtime"]:
            base = img
            if img == "runtime":
                # for CUDA 8, runtime == base
                base = "base"
            # cuda image
            temp_path = self.parent.manifest[f"{self.distro}{self.distro_version}"][
                "template_path"
            ]
            log.debug("temp_path: %s, output_path: %s", temp_path, self.output_path)
            self.output_template(
                template_path=pathlib.Path(f"{temp_path}/{base}/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )
            # We need files in the base directory
            for filename in pathlib.Path(f"{temp_path}/{base}").glob("*"):
                if "Dockerfile" in filename.name:
                    continue
                log.debug("Checking %s", filename)
                if ".jinja" in filename.name:
                    self.output_template(filename, f"{self.output_path}/{img}")
                else:
                    log.info(f"Copying {filename} to {self.output_path}/{img}")
                    shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            for vers in self.cudnn_versions():
                self.cuda[vers]["target"] = img
                self.output_cudnn_template(
                    cudnn_version=vers,
                    template_path=pathlib.Path(f"{temp_path}/cudnn/Dockerfile.jinja"),
                    output_path=pathlib.Path(f"{self.output_path}/{img}/{vers}"),
                )

    def generate_dockerscripts(self):
        for img in ["base", "devel", "runtime"]:
            # cuda image
            temp_path = self.parent.manifest[f"{self.distro}{self.distro_version}"][
                "template_path"
            ]
            log.debug("temp_path: %s, output_path: %s", temp_path, self.output_path)
            self.output_template(
                template_path=pathlib.Path(f"{temp_path}/{img}/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )
            # copy files
            for filename in pathlib.Path(f"{temp_path}/{img}").glob("*"):
                if "Dockerfile" in filename.name:
                    continue
                log.debug("Checking %s", filename)
                if ".jinja" in filename.name:
                    self.output_template(filename, f"{self.output_path}/{img}")
                else:
                    log.info(f"Copying {filename} to {self.output_path}/{img}")
                    shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            if img in ["runtime", "devel"]:
                for vers in self.cudnn_versions():
                    self.cuda[vers]["target"] = img
                    self.output_cudnn_template(
                        cudnn_version=vers,
                        template_path=pathlib.Path(
                            f"{temp_path}/cudnn/Dockerfile.jinja"
                        ),
                        output_path=pathlib.Path(f"{self.output_path}/{img}/{vers}"),
                    )

    def generate_testscripts(self):
        for filename in pathlib.Path("test").glob("*/*.jinja"):
            log.debug("Processing test '%s'", filename)
            # Check for distro specific tests
            if any(distro in filename.name for distro in self.supported_distro_list()):
                if not self.distro in filename.name:
                    log.debug(
                        "Skipping test '%s', distro requirement '%s' not met",
                        filename,
                        f"{self.distro}{self.distro_version}",
                    )
                    continue
            log.debug("Have special test: %s", "special" in str(filename.parents[0]))
            skip = not self.tag_suffix or self.tag_suffix not in filename.name
            log.debug("tag_suffix: '%s', skip match: %s", self.tag_suffix, skip)
            if "special" in str(filename.parents[0]) and skip:
                log.debug(f"Skipping {filename} {self.tag_suffix}")
                continue
            self.write_test(filename, f"{self.output_path}/test")

    def target_all(self):
        log.debug("Generating all docker scripts!")
        rgx = re.compile(r"^([a-zA-Z]*)([\d\.]*)-v([\d\.]*)")
        for k, _ in self.parent.ci.items():
            match = rgx.match(k)
            if match:
                self.distro = match.group(1)
                self.distro_version = match.group(2)
                self.cuda_version = match.group(3)
                self.targeted()

    def targeted(self):
        log.debug("Have distro: %s version: %s", self.distro, self.distro_version)
        target = f"{self.distro}{self.distro_version}"
        self.output_path = pathlib.Path(f"dist/{target}/{self.cuda_version}")
        if self.output_path.exists:
            log.debug(f"Removing {self.output_path}")
            rm["-rf", self.output_path]()
        log.debug(f"Creating {self.output_path}")
        self.output_path.mkdir(parents=True, exist_ok=False)
        self.prepare_context()
        if self.cuda_version == "8.0":
            self.generate_dockerscripts_cuda_8()
        else:
            self.generate_dockerscripts()
        self.generate_testscripts()

    def main(self):
        if self.generate_all:
            self.target_all()
        else:
            self.targeted()
        log.info("Done")


if __name__ == "__main__":
    Manager.run()
