from __future__ import annotations
from yamloom.actions.utils import validate_choice

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...expressions import context, StringExpression
from ..._yamloom import Step
from ..._yamloom import action
from ..types import (
    Oboollike,
    Oboolstr,
    Ointlike,
    Ostr,
    Ostrlike,
    StringLike,
    StringOrBoolLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ['setup_python', 'setup_uv', 'SetupPythonOutput', 'SetupUvOutput']


@dataclass(frozen=True)
class SetupPythonOutput:
    """Typed access to outputs produced by the setup_python step.

    Parameters
    ----------
    id
        The ``id`` of the setup_python step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_python`.

    Attributes
    ----------
    python_version
        The installed Python or PyPy version.
    cache_hit
        A boolean value to indicate a cache entry was found.
    python_path
        The absolute path to the Python or PyPy executable.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-python
    """

    id: str

    @property
    def python_version(self) -> StringExpression:
        return context.steps[self.id].outputs['python-version']

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']

    @property
    def python_path(self) -> StringExpression:
        return context.steps[self.id].outputs['python-path']


@dataclass(frozen=True)
class SetupUvOutput:
    """Typed access to outputs produced by the setup_uv step.

    Parameters
    ----------
    id
        The ``id`` of the setup_uv step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_uv`.

    Attributes
    ----------
    uv_version
        The installed uv version.
    uv_path
        The path to the installed uv binary.
    uvx_path
        The path to the installed uvx binary.
    cache_hit
        A boolean value to indicate a cache entry was found.
    cache_key
        The cache key used for storing/restoring the cache.
    venv
        Path to the activated venv if activate-environment is true.
    python_version
        The Python version that was set.
    python_cache_hit
        A boolean value to indicate the Python cache entry was found.

    See Also
    --------
    GitHub repository: https://github.com/astral-sh/setup-uv
    """

    id: str

    @property
    def uv_version(self) -> StringExpression:
        return context.steps[self.id].outputs['uv-version']

    @property
    def uv_path(self) -> StringExpression:
        return context.steps[self.id].outputs['uv-path']

    @property
    def uvx_path(self) -> StringExpression:
        return context.steps[self.id].outputs['uvx-path']

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']

    @property
    def cache_key(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-key']

    @property
    def venv(self) -> StringExpression:
        return context.steps[self.id].outputs.venv

    @property
    def python_version(self) -> StringExpression:
        return context.steps[self.id].outputs['python-version']

    @property
    def python_cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['python-cache-hit']


def setup_python(
    *,
    name: Ostrlike = None,
    version: str = 'v6',
    python_version: StringLike | None = None,
    python_version_file: Ostrlike = None,
    check_latest: Oboollike = None,
    architecture: Ostrlike = None,
    token: Ostrlike = None,
    cache: Ostrlike = None,
    cache_dependency_path: Ostrlike = None,
    update_environment: Oboollike = None,
    allow_prereleases: Oboollike = None,
    freethreaded: Oboollike = None,
    pip_version: Ostrlike = None,
    pip_install: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Set up a specific version of Python and add it to the PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    python_version
        Version range or exact version of Python or PyPy to use.
    python_version_file
        File containing the Python version to use.
    cache
        Package manager for caching in the default directory. Supported values:
        ``pip``, ``pipenv``, ``poetry``.
    architecture
        The target architecture of the Python or PyPy interpreter.
    check_latest
        Check for the latest available version that satisfies the version spec.
    token
        Token used to authenticate when fetching Python distributions.
    cache_dependency_path
        Path to dependency files. Supports wildcards or a list of file names.
    update_environment
        Set this option to update environment variables.
    allow_prereleases
        Allow prerelease versions to satisfy version range.
    freethreaded
        Use the freethreaded version of Python.
    pip_versions
        The version of pip to install with Python.
    pip_install
        Packages to install with pip after setting up Python.
    args
        The inputs for a Docker container which are passed to the container's entrypoint.
        This is a subkey of the ``with`` key of the generated step.
    entrypoint
        Overrides the Docker ENTRYPOINT in the action's Dockerfile or sets one if it was not
        specified. Accepts a single string defining the executable to run (note that this is
        different from Docker's ENTRYPOINT instruction which has both a shell and exec form).
        This is a subkey of the ``with`` key of the generated step.
    condition
        A boolean expression which must be met for the step to run. Note that this represents
        the ``if`` key in the actual YAML file.
    id
        A unique identifier for the step which can be referenced in expressions.
    env
        Used to specify environment variables for the step.
    continue_on_error
        Prevents the job from failing if this step fails.
    timeout_minutes
        The maximum number of minutes to let the step run before GitHub automatically
        cancels it (defaults to 360 if not specified).

    Returns
    -------
    Step
        The generated setup-python step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-python
    """
    options: dict[str, object] = {
        'python-version': python_version,
        'python-version-file': python_version_file,
        'check-latest': check_latest,
        'architecture': architecture,
        'token': token,
        'cache': cache,
        'cache-dependency-path': cache_dependency_path,
        'update-environment': update_environment,
        'allow-prereleases': allow_prereleases,
        'freethreaded': freethreaded,
        'pip-version': pip_version,
        'pip-install': pip_install,
    }

    if cache is not None:
        if isinstance(cache, str):
            lowered = cache.lower()
            if lowered not in {'pip', 'pipenv', 'poetry'}:
                msg = "'cache' must be 'pip', 'pipenv' or 'poetry'"
                raise ValueError(msg)
            options['cache'] = lowered
        else:
            options['cache'] = cache

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup Python'

    return action(
        name,
        'actions/setup-python',
        ref=version,
        with_opts=options or None,
        args=args,
        entrypoint=entrypoint,
        condition=condition,
        id=id,
        env=env,
        continue_on_error=continue_on_error,
        timeout_minutes=timeout_minutes,
    )


def setup_uv(
    *,
    name: Ostrlike = None,
    version: str = 'v7',
    uv_version: Ostrlike = None,
    uv_version_file: Ostrlike = None,
    resolution_strategy: Ostrlike = None,
    python_version: Ostrlike = None,
    activate_environment: Oboollike = None,
    working_directory: Ostrlike = None,
    checksum: Ostrlike = None,
    github_token: Ostrlike = None,
    enable_cache: StringOrBoolLike | None = None,
    cache_dependency_glob: list[StringLike] | None = None,
    restore_cache: Oboollike = None,
    save_cache: Oboollike = None,
    cache_suffix: Ostrlike = None,
    cache_local_path: Ostrlike = None,
    prune_cache: Oboollike = None,
    cache_python: Oboollike = None,
    ignore_nothing_to_cache: Oboollike = None,
    ignore_empty_workdir: Oboollike = None,
    tool_dir: Ostrlike = None,
    tool_bin_dir: Ostrlike = None,
    manifest_file: Ostrlike = None,
    add_problem_matchers: Oboollike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Set up a specific version of uv.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    uv_version
        The version of uv to install.
    uv_version_file
        Path to a file containing the version of uv to install.
    python_version
        The version of Python to set UV_PYTHON to.
    activate_environment
        Use uv venv to activate a venv ready to be used by later steps.
    working_directory
        The directory to execute all commands in and look for files.
    checksum
        The checksum of the uv version to install.
    github_token
        Used to increase the rate limit when retrieving versions and downloading uv.
    enable_cache
        Enable uploading of the uv cache. Accepts ``true``, ``false``, or ``auto``.
    cache_dependency_glob
        Glob pattern list to control the cache.
    restore_cache
        Whether to restore the cache if found.
    save_cache
        Whether to save the cache after the run.
    cache_suffix
        Suffix for the cache key.
    cache_local_path
        Local path to store the cache.
    prune_cache
        Prune cache before saving.
    cache_python
        Upload managed Python installations to the GitHub Actions cache.
    ignore_nothing_to_cache
        Ignore when nothing is found to cache.
    ignore_empty_workdir
        Ignore when the working directory is empty.
    tool_dir
        Custom path to set UV_TOOL_DIR to.
    tool_bin_dir
        Custom path to set UV_TOOL_BIN_DIR to.
    manifest_file
        URL to the manifest file containing available versions and download URLs.
    add_problem_matchers
        Add problem matchers.
    resolution_strategy
        Resolution strategy when resolving version ranges (``highest`` or
        ``lowest``).
    args
        The inputs for a Docker container which are passed to the container's entrypoint.
        This is a subkey of the ``with`` key of the generated step.
    entrypoint
        Overrides the Docker ENTRYPOINT in the action's Dockerfile or sets one if it was not
        specified. Accepts a single string defining the executable to run (note that this is
        different from Docker's ENTRYPOINT instruction which has both a shell and exec form).
        This is a subkey of the ``with`` key of the generated step.
    condition
        A boolean expression which must be met for the step to run. Note that this represents
        the ``if`` key in the actual YAML file.
    id
        A unique identifier for the step which can be referenced in expressions.
    env
        Used to specify environment variables for the step.
    continue_on_error
        Prevents the job from failing if this step fails.
    timeout_minutes
        The maximum number of minutes to let the step run before GitHub automatically
        cancels it (defaults to 360 if not specified).

    Returns
    -------
    Step
        The generated setup-uv step.

    See Also
    --------
    GitHub repository: https://github.com/astral-sh/setup-uv
    """
    options: dict[str, object] = {
        'version': uv_version,
        'version-file': uv_version_file,
        'resolution-strategy': validate_choice(
            'resolution_strategy', resolution_strategy, ['highest', 'lowest']
        ),
        'python-version': python_version,
        'activate-environment': activate_environment,
        'working-directory': working_directory,
        'checksum': checksum,
        'github-token': github_token,
        'enable-cache': enable_cache,
        'cache-dependency-glob': '\n'.join(str(s) for s in cache_dependency_glob)
        if cache_dependency_glob is not None
        else None,
        'restore-cache': restore_cache,
        'save-cache': save_cache,
        'cache-suffix': cache_suffix,
        'cache-local-path': cache_local_path,
        'prune-cache': prune_cache,
        'cache-python': cache_python,
        'ignore-nothing-to-cache': ignore_nothing_to_cache,
        'ignore-empty-workdir': ignore_empty_workdir,
        'tool-dir': tool_dir,
        'tool-bin-dir': tool_bin_dir,
        'manifest-file': manifest_file,
        'add-problem-matchers': add_problem_matchers,
    }

    if enable_cache is not None:
        if isinstance(enable_cache, str):
            if enable_cache.lower() != 'auto':
                msg = "'enable_cache' must be 'auto', true or false"
                raise ValueError(msg)
            options['enable-cache'] = 'auto'
        elif isinstance(enable_cache, bool):
            options['enable-cache'] = enable_cache
        else:
            options['enable-cache'] = enable_cache

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup uv'

    return action(
        name,
        'astral-sh/setup-uv',
        ref=version,
        with_opts=options or None,
        args=args,
        entrypoint=entrypoint,
        condition=condition,
        id=id,
        env=env,
        continue_on_error=continue_on_error,
        timeout_minutes=timeout_minutes,
    )
