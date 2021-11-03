"""Type checking on source code."""
from getpass import getpass
from os import getenv
from pathlib import Path
from typing import List

from termcolor import cprint

try:
    import toml
except ImportError:
    print("This script depends on `toml`. Run `poetry add -D toml`.")
    raise

try:
    from packaging.version import Version
except ImportError:
    print("This script depends on `packaging`. Run `poetry add -D packaging`.")
    raise

from invoke import Context, task

from tasks.utils import print_header


def install_emulators(ctx: Context, build_for_platforms: List[str]) -> None:
    """See https://github.com/tonistiigi/binfmt#installing-emulators."""
    emulators = []
    if "linux/arm64" in build_for_platforms:
        emulators.append("arm64")
    if "linux/arm/v7" in build_for_platforms:
        emulators.append("arm")

    if emulators:
        print_header("Installing emulators", level=2, icon="⬇")
        ctx.run("docker run --privileged --rm tonistiigi/binfmt --install " + ",".join(emulators))


@task()
def docker_build(ctx, push=True):
    """Builds a docker image locally and pushes it to the image registry.

    Args:
        ctx (invoke.Context): Invoke context.
        push (bool):
            Push the built image and cache to remote docker image registry. Login is required
            and Personal Access Token will be requested from STDIN if `DOCKERHUB_PERSONAL_ACCESS_TOKEN`
            environment variable is not set.
    """
    print_header("RUNNING DOCKER BUILD")

    flags: List[str] = []

    pyproject = toml.load(Path(__file__).parent.parent / "pyproject.toml")
    project = pyproject["tool"]["poetry"]
    project_name = project["name"]
    project_version = project["version"]

    python_version = Version(project["dependencies"]["python"].strip("<>=~^"))
    flags.append(f"--build-arg PYTHON_VERSION='{python_version.major}.{python_version.minor}'")

    dockerhub = pyproject["tool"]["invoke"]["dockerhub"]
    dockerhub_username = dockerhub["username"]
    build_for_platforms = dockerhub["build_for_platforms"]
    flags.append("--platform " + ",".join(build_for_platforms))

    if push:
        dockerhub_password = getenv("DOCKERHUB_PERSONAL_ACCESS_TOKEN")
        if not dockerhub_password:
            cprint("DOCKERHUB_PERSONAL_ACCESS_TOKEN environment variable not set.", color="yellow")
            dockerhub_password = getpass("Dockerhub Personal Access Token: ")
        ctx.run(f"docker login --username {dockerhub_username} --password {dockerhub_password}")

        flags.append("--output type=image,push=true")

    if getenv("CI"):  # https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables
        flags.append("--progress plain")

    install_emulators(ctx, build_for_platforms)

    # While `docker buildx build` supports multiple `--tag` flags, push of them fails to expose
    # all architectures in `latest`. Multiple pushes fix this.
    for tag in [project_version, "latest"]:
        print_header(f"Build {dockerhub_username}/{project_name}:{tag}", level=2, icon="🔨")

        flags_for_tag = list(flags)
        if tag != "latest" and push:
            flags_for_tag.append(f"--cache-to type=registry,ref={dockerhub_username}/{project_name}")

        ctx.run(
            f"""
                docker buildx build \
                --cache-from type=registry,ref={dockerhub_username}/{project_name} \
                --tag {dockerhub_username}/{project_name}:{tag} \
                {" ".join(flags_for_tag)} \
                .
            """,
            echo=True,
            pty=True,
        )

    if push:
        ctx.run("docker logout")
