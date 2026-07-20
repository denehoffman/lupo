from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

from yamloom import Job, Matrix, Step, Strategy, script
from yamloom.actions.github.artifacts import UploadArtifact
from yamloom.actions.github.scm import Checkout
from yamloom.actions.packaging.python import Maturin
from yamloom.actions.toolchains.python import SetupPython
from yamloom.actions.types import Oboollike, Oboolstr
from yamloom.expressions import context

PythonProfile = Literal['cpython', 'free-threaded', 'pypy', 'all']
SetupSteps = Callable[['MaturinPlatform'], Sequence[Step]]
MaturinOptions = Callable[['MaturinPlatform'], Mapping[str, object]]

CPYTHON_VERSIONS = ('3.9', '3.10', '3.11', '3.12', '3.13', '3.14')
FREE_THREADED_VERSIONS = ('3.14t',)
PYPY_VERSIONS = ('pypy3.11',)


@dataclass(frozen=True)
class MaturinTarget:
    runner: str
    target: str
    python_arch: str | None = None
    skip_python_versions: tuple[str, ...] = ()


@dataclass(frozen=True)
class MaturinPlatform:
    key: str
    name: str
    targets: tuple[MaturinTarget, ...]
    compatibility: str | None = None


DEFAULT_MATURIN_PLATFORMS = (
    MaturinPlatform(
        'linux',
        'Build Linux Wheels',
        tuple(
            MaturinTarget('ubuntu-22.04', target)
            for target in ('x86_64', 'x86', 'aarch64', 'armv7', 's390x', 'ppc64le')
        ),
        '2014',
    ),
    MaturinPlatform(
        'musllinux',
        'Build musllinux Wheels',
        tuple(
            MaturinTarget('ubuntu-22.04', target)
            for target in ('x86_64', 'x86', 'aarch64', 'armv7')
        ),
        'musllinux_1_2',
    ),
    MaturinPlatform(
        'windows',
        'Build Windows Wheels',
        (
            MaturinTarget('windows-latest', 'x64', 'x64'),
            MaturinTarget('windows-latest', 'x86', 'x86', ('pypy3.11',)),
            MaturinTarget(
                'windows-11-arm',
                'aarch64',
                'arm64',
                ('3.9', '3.10', '3.11', '3.14t', 'pypy3.11'),
            ),
        ),
    ),
    MaturinPlatform(
        'macos',
        'Build macOS Wheels',
        (
            MaturinTarget('macos-15-intel', 'x86_64'),
            MaturinTarget('macos-latest', 'aarch64'),
        ),
    ),
)


def _version_number(version: str) -> tuple[int, int] | None:
    normalized = version.removeprefix('pypy').removesuffix('t')
    try:
        major, minor = normalized.split('.', 1)
        return int(major), int(minor)
    except ValueError:
        return None


@dataclass
class MaturinBuildSuite:
    """Create portable Maturin wheel and source-distribution jobs."""

    package_name: str = 'wheels'
    manifest_path: str | None = None
    python_profile: PythonProfile = 'cpython'
    python_versions: Sequence[str] | None = None
    minimum_python: str | None = None
    platforms: Sequence[MaturinPlatform] = DEFAULT_MATURIN_PLATFORMS
    args: Sequence[str] = ('--release', '--out', 'dist')
    artifact_prefix: str | None = None
    needs: Sequence[str] | None = None
    condition: Oboolstr = None
    upload: bool = True
    sdist: bool = True
    sccache: Oboollike = None
    action_version: str = 'v1'
    setup_steps: SetupSteps | None = None
    maturin_options: MaturinOptions | None = None
    _resolved_versions: tuple[str, ...] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        profiles = {
            'cpython': CPYTHON_VERSIONS,
            'free-threaded': FREE_THREADED_VERSIONS,
            'pypy': PYPY_VERSIONS,
            'all': CPYTHON_VERSIONS + FREE_THREADED_VERSIONS + PYPY_VERSIONS,
        }
        if self.python_versions is not None:
            versions = tuple(self.python_versions)
        else:
            try:
                versions = profiles[self.python_profile]
            except KeyError as exc:
                raise ValueError(
                    f'Unknown Python profile: {self.python_profile}'
                ) from exc
        if self.minimum_python is not None:
            minimum = _version_number(self.minimum_python)
            if minimum is None:
                raise ValueError(
                    f'Invalid minimum Python version: {self.minimum_python}'
                )
            versions = tuple(
                version
                for version in versions
                if (number := _version_number(version)) is None or number >= minimum
            )
        if not versions:
            raise ValueError('Maturin build suite resolved to no Python versions')
        self._resolved_versions = versions

    @property
    def resolved_python_versions(self) -> tuple[str, ...]:
        return self._resolved_versions

    def _platform_entry(self, target: MaturinTarget) -> dict[str, object]:
        skipped = set(target.skip_python_versions)
        versions = [
            version for version in self._resolved_versions if version not in skipped
        ]
        if not versions:
            raise ValueError(
                f'Target {target.target} has no compatible Python versions'
            )
        entry: dict[str, object] = {
            'runner': target.runner,
            'target': target.target,
            'python_versions': versions,
        }
        if target.python_arch is not None:
            entry['python_arch'] = target.python_arch
        return entry

    def _wheel_job(self, platform: MaturinPlatform) -> Job:
        interpreter = context.matrix.platform.python_versions.as_array().join(' ')
        build_args = [*self.args]
        if self.manifest_path is not None:
            build_args.extend(('--manifest-path', self.manifest_path))
        build_args.extend(('--interpreter', str(interpreter)))
        options: dict[str, object] = {
            'name': 'Build wheels',
            'version': self.action_version,
            'target': context.matrix.platform.target.as_str(),
            'args': ' '.join(build_args),
            'manylinux': platform.compatibility,
            'sccache': self.sccache,
        }
        if self.maturin_options is not None:
            options.update(self.maturin_options(platform))

        steps: list[Step] = [
            Checkout(),
            script(f'printf "%s\\n" {interpreter} > .yamloom-python-versions'),
            SetupPython(
                python_version_file='.yamloom-python-versions',
                architecture=context.matrix.platform.python_arch.as_str()
                if any(target.python_arch for target in platform.targets)
                else None,
            ),
        ]
        if self.setup_steps is not None:
            steps.extend(self.setup_steps(platform))
        steps.append(Maturin(**options))  # ty:ignore[invalid-argument-type]
        if self.upload:
            prefix = self.artifact_prefix or self.package_name
            steps.append(
                UploadArtifact(
                    path='dist',
                    artifact_name=f'{prefix}-{platform.key}-{context.matrix.platform.target}',
                )
            )
        return Job(
            name=platform.name,
            steps=steps,
            runs_on=context.matrix.platform.runner.as_str(),
            strategy=Strategy(
                fast_fail=False,
                matrix=Matrix(
                    platform=[
                        self._platform_entry(target) for target in platform.targets
                    ]
                ),
            ),
            needs=list(self.needs) if self.needs is not None else None,
            condition=self.condition,
        )

    def _sdist_job(self) -> Job:
        args = ['--out', 'dist']
        if self.manifest_path is not None:
            args.extend(('--manifest-path', self.manifest_path))
        steps: list[Step] = [
            Checkout(),
            Maturin(
                name='Build source distribution',
                version=self.action_version,
                command='sdist',
                args=' '.join(args),
            ),
        ]
        if self.upload:
            steps.append(
                UploadArtifact(
                    path='dist',
                    artifact_name=f'{self.artifact_prefix or self.package_name}-sdist',
                )
            )
        return Job(
            name='Build Source Distribution',
            steps=steps,
            runs_on='ubuntu-22.04',
            needs=list(self.needs) if self.needs is not None else None,
            condition=self.condition,
        )

    def jobs(self) -> dict[str, Job]:
        jobs = {platform.key: self._wheel_job(platform) for platform in self.platforms}
        if self.sdist:
            jobs['sdist'] = self._sdist_job()
        return jobs


__all__ = [
    'CPYTHON_VERSIONS',
    'DEFAULT_MATURIN_PLATFORMS',
    'FREE_THREADED_VERSIONS',
    'MaturinBuildSuite',
    'MaturinPlatform',
    'MaturinTarget',
    'PYPY_VERSIONS',
    'PythonProfile',
]
