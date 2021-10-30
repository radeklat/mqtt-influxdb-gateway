"""Type checking on source code."""
from getpass import getpass
from os import getenv
from pathlib import Path

try:
    import toml
except ImportError:
    print("This script depends on `toml`. Run `poetry add -D toml`.")
    raise

from invoke import task

from tasks.utils import print_header


@task()
def docker_build(ctx, login=True, push=True):
    """Builds a docker image locally and pushes it to the image registry.

    Args:
        ctx (invoke.Context): Invoke context.
        login (bool): Login to dockerhub.
        push (bool): Push to remote docker image registry.
    """
    print_header("RUNNING DOCKER BUILD")

    pyproject = toml.load(Path(__file__).parent.parent / "pyproject.toml")
    project = pyproject["tool"]["poetry"]
    project_name = project["name"]
    project_version = project["version"]

    dockerhub_username = pyproject["tool"]["invoke"]["dockerhub"]["username"]

    running_in_ci = getenv("CI")  # https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables

    if login:
        dockerhub_password = getenv("DOCKERHUB_PERSONAL_ACCESS_TOKEN")
        if not dockerhub_password:
            dockerhub_password = getpass("Dockerhub Personal Access Token: ")
        ctx.run(f"docker login --username {dockerhub_username} --password {dockerhub_password}")

    ctx.run(
        f"""
            docker buildx build \
            --platform linux/amd64,linux/arm64,linux/arm/v7 \
            --cache-to type=registry,ref={dockerhub_username}/{project_name} \
            --cache-from type=registry,ref={dockerhub_username}/{project_name} \
            --tag {dockerhub_username}/{project_name}:latest \
            --tag {dockerhub_username}/{project_name}:{project_version} \
            {'--progress plain' if running_in_ci else ''} \
            {'--push' if push else ''} \
            .
        """,
        echo=True,
        pty=True,
    )

    if login:
        ctx.run("docker logout")
