from pathlib import Path

from yamloom.__main__ import main, resolve_target


GENERATOR = """
from yamloom import Events, Job, PushEvent, Workflow, script, sync

workflow = Workflow(
    on=Events(push=PushEvent()),
    jobs={'check': Job(runs_on='ubuntu-latest', steps=[script('true')])},
)

sync({'check.yml': workflow})
"""


def test_cli_sync_and_check(tmp_path: Path, monkeypatch) -> None:
    generator = tmp_path / '.yamloom.py'
    generator.write_text(GENERATOR)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('sys.argv', ['yamloom', 'sync'])
    assert main() == 0
    workflow = tmp_path / '.github/workflows/check.yml'
    assert workflow.exists()

    monkeypatch.setattr('sys.argv', ['yamloom', 'check'])
    assert main() == 0
    workflow.write_text(f'{workflow.read_text()}# drift\n')
    assert main() == 1


def test_cli_rejects_dump_only_generator(tmp_path: Path, monkeypatch) -> None:
    generator = tmp_path / '.yamloom.py'
    generator.write_text('value = 1\n')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr('sys.argv', ['yamloom', 'sync'])
    assert main() == 2


def test_resolve_target_precedence(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / '.yamloom.py').write_text('')
    (tmp_path / 'explicit.py').write_text('')
    assert resolve_target('explicit.py') == Path('explicit.py')
    assert resolve_target(None) == Path('.yamloom.py')
