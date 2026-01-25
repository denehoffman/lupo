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
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ['install_rust_tool', 'setup_rust', 'SetupRustOutput']


@dataclass(frozen=True)
class SetupRustOutput:
    """Typed access to outputs produced by the setup_rust step.

    Parameters
    ----------
    id
        The ``id`` of the setup_rust step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_rust`.

    Attributes
    ----------
    rustc_version
        Version as reported by ``rustc --version``.
    cargo_version
        Version as reported by ``cargo --version``.
    rustup_version
        Version as reported by ``rustup --version``.
    cachekey
        Short hash of the rustc version, appropriate for use as a cache key.

    See Also
    --------
    GitHub repository: https://github.com/actions-rust-lang/setup-rust-toolchain
    """

    id: str

    @property
    def rustc_version(self) -> StringExpression:
        return context.steps[self.id].outputs['rustc-version']

    @property
    def cargo_version(self) -> StringExpression:
        return context.steps[self.id].outputs['cargo-version']

    @property
    def rustup_version(self) -> StringExpression:
        return context.steps[self.id].outputs['rustup-version']

    @property
    def cachekey(self) -> StringExpression:
        return context.steps[self.id].outputs.cachekey


def setup_rust(
    *,
    name: Ostrlike = None,
    version: str = 'v1',
    toolchain: Ostrlike = None,
    target: Ostrlike = None,
    components: list[StringLike] | None = None,
    cache: Oboollike = None,
    cache_directories: list[StringLike] | None = None,
    cache_workspaces: list[StringLike] | None = None,
    cache_on_failure: Oboollike = None,
    cache_key: Ostrlike = None,
    cache_shared_key: Ostrlike = None,
    cache_bin: Oboollike = None,
    cache_provider: Ostrlike = None,
    cache_all_crates: Oboollike = None,
    cache_workspace_crates: Oboollike = None,
    matcher: Oboollike = None,
    rustflags: Ostrlike = None,
    override: Oboollike = None,
    rust_src_dir: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Set up Rust toolchains with optional caching.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    toolchain
        Comma-separated list of Rust toolchain specifications. The last version
        becomes the default.
    target
        Target triple to install for this toolchain.
    components
        Comma-separated list of components to install.
    cache
        Automatically configure Rust cache.
    cache_workspaces
        Paths to multiple Cargo workspaces and their target directories,
        separated by newlines.
    cache_directories
        Additional non-workspace directories to be cached, separated by newlines.
    cache_on_failure
        Cache even if the build fails.
    cache_key
        Additional cache key to add alongside the automatic job-based key.
    cache_shared_key
        Cache key used instead of the automatic job-based key.
    cache_bin
        Whether to cache ``${CARGO_HOME}/bin``.
    cache_provider
        Cache provider (``github``, ``buildjet``, ``warpbuild``).
    cache_all_crates
        If true, cache all crates; otherwise cache dependent crates.
    cache_workspace_crates
        If true, cache all workspace crates; otherwise dependent crates only.
    matcher
        Enable the Rust problem matcher.
    rustflags
        Set RUSTFLAGS environment variable.
    override
        Setup the last installed toolchain as the default via ``rustup override``.
    rust_src_dir
        Path from root directory to the Rust source directory.
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
        The generated setup-rust step.

    See Also
    --------
    GitHub repository: https://github.com/actions-rust-lang/setup-rust-toolchain
    """
    options: dict[str, object] = {
        'toolchain': toolchain,
        'target': target,
        'components': ','.join(str(s) for s in components)
        if components is not None
        else None,
        'cache': cache,
        'cache-directories': '\n'.join(str(s) for s in cache_directories)
        if cache_directories is not None
        else None,
        'cache-workspaces': '\n'.join(str(s) for s in cache_workspaces)
        if cache_workspaces is not None
        else None,
        'cache-on-failure': cache_on_failure,
        'cache-key': cache_key,
        'cache-shared-key': cache_shared_key,
        'cache-bin': cache_bin,
        'cache-provider': validate_choice(
            'cache_provider', cache_provider, ['github', 'buildjet', 'warpbuild']
        ),
        'cache-all-crates': cache_all_crates,
        'cache-workspace-crates': cache_workspace_crates,
        'matcher': matcher,
        'rustflags': rustflags,
        'override': override,
        'rust-src-dir': rust_src_dir,
    }

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup Rust'

    return action(
        name,
        'actions-rust-lang/setup-rust-toolchain',
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


def install_rust_tool(
    *,
    tool: list[StringLike],
    name: Ostrlike = None,
    version: str = 'v2',
    checksum: Oboollike = None,
    fallback: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Install development tools.

    Parameters
    ----------
    tool
        Tools to install (whitespace or comma separated list).
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    checksum
        Whether to enable checksums.
    fallback
        Whether to use fallback (``none``, ``cargo-binstall``, ``cargo-install``).
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
        The generated install-rust-tool step.

    See Also
    --------
    GitHub repository: https://github.com/taiki-e/install-action
    """
    if not tool:
        msg = "at least one 'tool' must be specified"
        raise ValueError(msg)

    options: dict[str, object] = {
        'tool': ','.join(str(s) for s in tool),
        'checksum': checksum,
        'fallback': validate_choice(
            'fallback', fallback, ['none', 'cargo-binstall', 'cargo-install']
        ),
    }

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        suffix = 's' if len(tool) > 1 else ''
        name = f'Install Rust Tool{suffix}'

    return action(
        name,
        'taiki-e/install-action',
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
