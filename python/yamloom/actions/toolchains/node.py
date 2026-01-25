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
    BoolLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ['setup_node', 'setup_pnpm', 'SetupNodeOutput', 'SetupPnpmOutput']


@dataclass(frozen=True)
class SetupNodeOutput:
    """Typed access to outputs produced by the setup_node step.

    Parameters
    ----------
    id
        The ``id`` of the setup_node step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_node`.

    Attributes
    ----------
    cache_hit
        A boolean value to indicate if a cache was hit.
    node_version
        The installed Node.js version.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-node
    """

    id: str

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']

    @property
    def node_version(self) -> StringExpression:
        return context.steps[self.id].outputs['node-version']


@dataclass(frozen=True)
class SetupPnpmOutput:
    """Typed access to outputs produced by the setup_pnpm step.

    Parameters
    ----------
    id
        The ``id`` of the setup_pnpm step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_pnpm`.

    Attributes
    ----------
    dest
        Expanded path of ``dest``.
    bin_dest
        Location of ``pnpm`` and ``pnpx`` command.

    See Also
    --------
    GitHub repository: https://github.com/pnpm/action-setup
    """

    id: str

    @property
    def dest(self) -> StringExpression:
        return context.steps[self.id].outputs.dest

    @property
    def bin_dest(self) -> StringExpression:
        return context.steps[self.id].outputs.bin_dest


def setup_node(
    *,
    name: Ostrlike = None,
    version: str = 'v6',
    node_version: Ostrlike = None,
    node_version_file: Ostrlike = None,
    check_latest: Oboollike = None,
    architecture: Ostrlike = None,
    token: Ostrlike = None,
    cache: Ostrlike = None,
    package_manager_cache: Oboollike = None,
    cache_dependency_path: Ostrlike = None,
    registry_url: Ostrlike = None,
    scope: Ostrlike = None,
    mirror: Ostrlike = None,
    mirror_token: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Set up a Node.js environment.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    node_version
        Version spec of the version to use (e.g. ``12.x``).
    node_version_file
        File containing the version spec to use (e.g. ``.nvmrc``).
    architecture
        Target architecture for Node to use.
    check_latest
        Check for the latest available version that satisfies the version spec.
    registry_url
        Optional registry to set up for auth.
    scope
        Optional scope for authenticating against scoped registries.
    token
        Used to pull Node distributions from node-versions.
    cache
        Package manager for caching in the default directory. Supported values:
        ``npm``, ``yarn``, ``pnpm``.
    package_manager_cache
        Set to false to disable automatic caching.
    cache_dependency_path
        Path to a dependency file (package-lock.json, yarn.lock, etc.).
    mirror
        Alternative mirror to download Node.js binaries from.
    mirror_token
        Token used as Authorization header when fetching from the mirror.
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
        The generated setup-node step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-node
    """
    options: dict[str, object] = {
        'node-version': node_version,
        'node-version-file': node_version_file,
        'check-latest': check_latest,
        'architecture': architecture,
        'token': token,
        'cache': validate_choice('cache', cache, ['npm', 'yarn', 'pnpm']),
        'package-manager-cache': package_manager_cache,
        'cache-dependency-path': cache_dependency_path,
        'registry-url': registry_url,
        'scope': scope,
        'mirror': mirror,
        'mirror-token': mirror_token,
    }

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup Node'

    return action(
        name,
        'actions/setup-node',
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


def setup_pnpm(
    *,
    name: Ostrlike = None,
    version: str = 'v4',
    pnpm_version: Ostrlike = None,
    dest: Ostrlike = None,
    run_install: StringLike | BoolLike | None = None,
    cache: Oboollike = None,
    cache_dependency_path: Ostrlike | list[StringLike] = None,
    package_json_file: Ostrlike = None,
    standalone: Oboollike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Install pnpm package manager.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    pnpm_version
        Version of pnpm to install.
    dest
        Where to store pnpm files.
    run_install
        If specified, run ``pnpm install``.
    cache
        Whether to cache the pnpm store directory.
    cache_dependency_path
        File path to the pnpm lockfile for caching.
    package_json_file
        File path to the package.json to read ``packageManager`` configuration.
    standalone
        When true, installs @pnpm/exe to allow pnpm usage without Node.js.
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
        The generated setup-pnpm step.

    See Also
    --------
    GitHub repository: https://github.com/pnpm/action-setup
    """
    options: dict[str, object] = {
        'version': pnpm_version,
        'dest': dest,
        'run_install': run_install,
        'cache': cache,
        'cache_dependency_path': cache_dependency_path,
        'package_json_file': package_json_file,
        'standalone': standalone,
    }

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup pnpm'

    return action(
        name,
        'pnpm/action-setup',
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
