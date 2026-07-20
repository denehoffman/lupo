from __future__ import annotations

import difflib
import inspect
import os
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from ._yamloom import Workflow

Mode = Literal['sync', 'check']
DEFAULT_DIRECTORY = Path('.github/workflows')
MARKER_PREFIX = '# yamloom: generated from '


@dataclass(frozen=True)
class SyncResult:
    changed: tuple[Path, ...] = ()
    missing: tuple[Path, ...] = ()
    stale: tuple[Path, ...] = ()

    @property
    def clean(self) -> bool:
        return not (self.changed or self.missing or self.stale)


@dataclass
class _Execution:
    mode: Mode
    root: Path
    source: Path
    calls: int = 0
    result: SyncResult | None = None


_execution: _Execution | None = None


def _source_name(source: Path, root: Path) -> str:
    try:
        return source.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return source.resolve().as_posix()


def _marker(source: Path, root: Path) -> str:
    return f'{MARKER_PREFIX}{_source_name(source, root)}'


def _validate_name(name: str | os.PathLike[str]) -> str:
    value = os.fspath(name)
    path = PurePath(value)
    if (
        not value
        or path.is_absolute()
        or len(path.parts) != 1
        or path.name in {'.', '..'}
        or path.suffix.lower() not in {'.yml', '.yaml'}
    ):
        raise ValueError(
            f'Workflow key must be a .yml or .yaml filename without directories: {value!r}'
        )
    return value


def _caller_source() -> Path:
    frame = inspect.currentframe()
    assert frame is not None
    sync_frame = frame.f_back
    caller = sync_frame.f_back if sync_frame is not None else None
    filename = caller.f_globals.get('__file__') if caller is not None else None
    return Path(filename or '.yamloom.py')


def _render(workflow: Workflow, marker: str, *, validate: bool) -> str:
    if validate:
        workflow.validate()
    body = str(workflow)
    return f'{marker}\n{body.rstrip()}\n'


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _report_difference(path: Path, actual: str, expected: str) -> None:
    print(f'Workflow differs: {path}')
    print(
        ''.join(
            difflib.unified_diff(
                actual.splitlines(keepends=True),
                expected.splitlines(keepends=True),
                fromfile=str(path),
                tofile=f'{path} (generated)',
            )
        ),
        end='',
    )


def sync(
    workflows: Mapping[str | os.PathLike[str], Workflow],
    *,
    directory: str | os.PathLike[str] = DEFAULT_DIRECTORY,
    validate: bool = True,
) -> SyncResult:
    """Synchronize a complete, explicitly owned set of GitHub workflows."""
    global _execution

    execution = _execution
    if execution is None:
        root = Path.cwd()
        source = _caller_source()
        mode: Mode = 'sync'
    else:
        execution.calls += 1
        if execution.calls > 1:
            raise RuntimeError(
                'A workflow generator must call yamloom.sync() exactly once'
            )
        root, source, mode = execution.root, execution.source, execution.mode

    output_directory = Path(directory)
    if output_directory.is_absolute():
        raise ValueError('Workflow directory must be relative to the project root')
    output_directory = root / output_directory
    marker = _marker(source, root)

    rendered: dict[Path, str] = {}
    for raw_name, workflow in workflows.items():
        name = _validate_name(raw_name)
        target = output_directory / name
        if target in rendered:
            raise ValueError(f'Duplicate workflow output: {name}')
        rendered[target] = _render(workflow, marker, validate=validate)

    changed: list[Path] = []
    missing: list[Path] = []
    for target, expected in rendered.items():
        if not target.exists():
            missing.append(target)
            if mode == 'check':
                print(f'Missing generated workflow: {target}')
            else:
                _atomic_write(target, expected)
            continue
        actual = target.read_text(encoding='utf-8')
        if actual != expected:
            changed.append(target)
            if mode == 'check':
                _report_difference(target, actual, expected)
            else:
                _atomic_write(target, expected)

    stale: list[Path] = []
    if output_directory.exists():
        for candidate in sorted(output_directory.iterdir()):
            if candidate in rendered or candidate.suffix.lower() not in {
                '.yml',
                '.yaml',
            }:
                continue
            try:
                with candidate.open(encoding='utf-8') as stream:
                    first_line = stream.readline().rstrip('\n')
            except OSError:
                continue
            if first_line == marker:
                stale.append(candidate)
                if mode == 'check':
                    print(f'Stale generated workflow: {candidate}')
                else:
                    candidate.unlink()

    result = SyncResult(tuple(changed), tuple(missing), tuple(stale))
    if execution is not None:
        execution.result = result
    return result


def _begin_execution(mode: Mode, root: Path, source: Path) -> None:
    global _execution
    _execution = _Execution(mode, root, source)


def _end_execution() -> _Execution:
    global _execution
    if _execution is None:
        raise RuntimeError('No Yamloom generator is running')
    execution = _execution
    _execution = None
    return execution


__all__ = ['SyncResult', 'sync']
