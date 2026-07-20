from __future__ import annotations

import argparse
import os
import runpy
import sys
from pathlib import Path

from .converter import ConversionError, convert_workflow
from ._sync import _begin_execution, _end_execution

DEFAULT_CANDIDATES = ('.yamloom.py', 'yamloom.py')
ENV_VAR = 'YAMLOOM_FILE'


def resolve_target(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    env_value = os.getenv(ENV_VAR)
    if env_value:
        return Path(env_value)
    for candidate in DEFAULT_CANDIDATES:
        path = Path(candidate)
        if path.exists():
            return path
    candidates = ', '.join(DEFAULT_CANDIDATES)
    raise FileNotFoundError(
        f'Could not find workflow generator. Tried: {candidates}. '
        f'Set --file or {ENV_VAR} to override.'
    )


def _run_generator(mode: str, filename: str | None) -> int:
    try:
        target = resolve_target(filename).resolve()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if not target.exists():
        print(f'Workflow generator not found: {target}', file=sys.stderr)
        return 2

    # Workflow paths are deliberately anchored to the invocation directory. This is
    # deterministic in hooks and avoids accidentally adopting an unrelated parent repo.
    root = Path.cwd().resolve()
    _begin_execution(mode, root, target)  # type: ignore[arg-type]
    try:
        runpy.run_path(str(target), run_name='__main__')
    except Exception as exc:
        print(f'Yamloom generator failed: {exc}', file=sys.stderr)
        return 1
    finally:
        execution = _end_execution()

    if execution.calls == 0:
        print(
            'Generator did not call yamloom.sync(). Replace Workflow.dump() calls with '
            "sync({'workflow.yml': workflow, ...}).",
            file=sys.stderr,
        )
        return 2
    assert execution.result is not None
    if mode == 'check' and not execution.result.clean:
        print('Generated workflows are stale; run `yamloom sync`.', file=sys.stderr)
        return 1
    return 0


def _convert(args: argparse.Namespace) -> int:
    source_path = Path(args.input)
    try:
        generated = convert_workflow(
            source_path.read_text(encoding='utf-8'), workflow_name=source_path.name
        )
    except (OSError, ConversionError, ValueError) as exc:
        print(f'Could not convert workflow: {exc}', file=sys.stderr)
        return 2
    if args.output is None:
        print(generated, end='')
        return 0
    output = Path(args.output)
    if output.exists() and not args.force:
        print(
            f'Output already exists: {output}; pass --force to overwrite it.',
            file=sys.stderr,
        )
        return 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generated, encoding='utf-8')
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Generate and maintain GitHub workflows.'
    )
    parser.add_argument('--file', dest='legacy_file', help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(dest='command')
    for command, description in (
        ('sync', 'Write generated workflows and remove stale owned files.'),
        ('check', 'Check generated workflows without modifying files.'),
    ):
        subparser = subparsers.add_parser(command, help=description)
        subparser.add_argument('--file', help='Path to the workflow generator script.')
    converter = subparsers.add_parser(
        'convert', help='Convert workflow YAML to Yamloom Python.'
    )
    converter.add_argument('input', help='Input .yml or .yaml workflow.')
    converter.add_argument(
        '-o', '--output', help='Output Python file; defaults to stdout.'
    )
    converter.add_argument(
        '--force', action='store_true', help='Overwrite an existing output.'
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == 'convert':
        return _convert(args)
    command = args.command or 'sync'
    filename = getattr(args, 'file', None) or args.legacy_file
    return _run_generator(command, filename)


if __name__ == '__main__':
    raise SystemExit(main())
