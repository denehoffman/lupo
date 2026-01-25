import pytest

from yamloom import Job, WorkflowInput, script
from yamloom.expressions import context


def test_job_requires_runs_on_or_uses() -> None:
    with pytest.raises(Exception):
        Job(steps=[script('echo hi')])


def test_job_rejects_runs_on_and_uses() -> None:
    with pytest.raises(Exception):
        Job(
            steps=[script('echo hi')],
            runs_on='ubuntu-latest',
            uses='org/repo/.github/workflows/reuse.yml@v1',
        )


def test_job_rejects_uses_with_steps() -> None:
    with pytest.raises(Exception):
        Job(
            steps=[script('echo hi')],
            uses='org/repo/.github/workflows/reuse.yml@v1',
        )


def test_job_rejects_runs_on_without_steps() -> None:
    with pytest.raises(Exception):
        Job(runs_on='ubuntu-latest')


def test_job_rejects_runs_on_with_empty_steps() -> None:
    with pytest.raises(Exception):
        Job(steps=[], runs_on='ubuntu-latest')


def test_job_rejects_runs_on_with_secrets_context() -> None:
    with pytest.raises(Exception):
        Job(steps=[script('echo hi')], runs_on=context.secrets.github_token)


def test_workflow_call_input_default_rejects_secrets() -> None:
    with pytest.raises(Exception):
        WorkflowInput.string(default=context.secrets.github_token)


def test_workflow_call_input_default_allows_github() -> None:
    WorkflowInput.string(default=context.github.actor)
