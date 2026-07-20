from yamloom.actions.toolchains.rust import SetupRust
from yamloom.actions.github.artifacts import DownloadArtifact
from yamloom.actions.github.release import ReleasePlease
from yamloom.actions.toolchains.python import SetupUV
from yamloom.actions.github.scm import Checkout
from yamloom.expressions import context
from yamloom.workflows.maturin import MaturinBuildSuite
from yamloom import (
    Workflow,
    Events,
    PushEvent,
    PullRequestEvent,
    WorkflowDispatchEvent,
    Permissions,
    Job,
    script,
    Environment,
    sync,
)


build_condition = context.github.ref.startswith('refs/tags/') | (
    context.github.event_name == 'workflow_dispatch'
)
build_jobs = MaturinBuildSuite(
    python_profile='all',
    needs=['build-test-check'],
    condition=build_condition,
    sccache=~context.github.ref.startswith('refs/tags/'),
    minimum_python='3.10',
).jobs()


release_workflow = Workflow(
    name='Build and Release',
    on=Events(
        push=PushEvent(branches=['main'], tags=['*']),
        pull_request=PullRequestEvent(),
        workflow_dispatch=WorkflowDispatchEvent(),
    ),
    jobs={
        'build-test-check': Job(
            steps=[
                Checkout(),
                SetupRust(components=['clippy']),
                SetupUV(python_version='3.10'),
                script('cargo clippy'),
                script('cargo test'),
                script(
                    'uv venv',
                    '. .venv/bin/activate',
                    'echo PATH=$PATH >> $GITHUB_ENV',
                    'uvx maturin develop --uv',
                ),
                script('uv pip install pytest'),
                script('uvx ruff check'),
                script('uvx ty check'),
                script('uv run pytest'),
            ],
            runs_on='ubuntu-latest',
        ),
        **build_jobs,
        'release': Job(
            steps=[
                DownloadArtifact(),
                SetupUV(),
                script(
                    'uv publish --trusted-publishing always wheels-*/*',
                    permissions=Permissions(id_token='write', contents='write'),
                ),
            ],
            name='Release',
            runs_on='ubuntu-22.04',
            condition=context.github.ref.startswith('refs/tags/')
            | (context.github.event_name == 'workflow_dispatch'),
            needs=['linux', 'musllinux', 'windows', 'macos', 'sdist'],
            environment=Environment('pypi'),
        ),
    },
)

version_workflow = Workflow(
    name='Release Please',
    on=Events(
        push=PushEvent(
            branches=['main'],
        ),
    ),
    jobs={
        'release-please': Job(
            steps=[
                ReleasePlease(
                    token=context.secrets.RELEASE_PLEASE,
                    config_file='release-please-config.json',
                    manifest_file='.release-please-manifest.json',
                )
            ],
            runs_on='ubuntu-latest',
        )
    },
)


if __name__ == '__main__':
    sync(
        {
            'release.yml': release_workflow,
            'release-please.yml': version_workflow,
        }
    )
