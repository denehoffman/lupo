from pathlib import Path

import pytest

from yamloom import Events, Job, PushEvent, Workflow, script, sync
from yamloom._sync import _begin_execution, _end_execution


def workflow(command: str = 'true') -> Workflow:
    return Workflow(
        on=Events(push=PushEvent()),
        jobs={'check': Job(runs_on='ubuntu-latest', steps=[script(command)])},
    )


def execute(root: Path, mode: str, workflows: dict[str, Workflow]):
    source = root / '.yamloom.py'
    _begin_execution(mode, root, source)  # ty:ignore[invalid-argument-type]
    try:
        return sync(workflows)  # ty:ignore[invalid-argument-type]
    finally:
        _end_execution()


def test_sync_writes_idempotently_and_prunes_only_owned_files(tmp_path: Path) -> None:
    output = tmp_path / '.github/workflows'
    output.mkdir(parents=True)
    manual = output / 'manual.yml'
    manual.write_text('on: push\njobs: {}\n')

    first = execute(tmp_path, 'sync', {'check.yml': workflow()})
    generated = output / 'check.yml'
    assert first.missing == (generated,)
    assert generated.read_text().startswith('# yamloom: generated from .yamloom.py\n')
    assert generated.stat().st_mode & 0o777 == 0o644
    assert execute(tmp_path, 'sync', {'check.yml': workflow()}).clean

    stale = execute(tmp_path, 'sync', {})
    assert stale.stale == (generated,)
    assert not generated.exists()
    assert manual.exists()


def test_check_reports_without_mutating(tmp_path: Path) -> None:
    execute(tmp_path, 'sync', {'check.yml': workflow('old')})
    path = tmp_path / '.github/workflows/check.yml'
    before = path.read_text()
    result = execute(tmp_path, 'check', {'check.yml': workflow('new')})
    assert result.changed == (path,)
    assert path.read_text() == before


@pytest.mark.parametrize(
    'name', ['../bad.yml', 'nested/bad.yml', '/bad.yml', 'bad.txt']
)
def test_sync_rejects_unsafe_names(tmp_path: Path, name: str) -> None:
    with pytest.raises(ValueError):
        execute(tmp_path, 'sync', {name: workflow()})


def test_other_generator_marker_is_preserved(tmp_path: Path) -> None:
    output = tmp_path / '.github/workflows'
    output.mkdir(parents=True)
    other = output / 'other.yml'
    other.write_text('# yamloom: generated from other.py\non: push\njobs: {}\n')
    execute(tmp_path, 'sync', {})
    assert other.exists()
