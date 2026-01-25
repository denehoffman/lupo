from __future__ import annotations

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

__all__ = ['setup_bun', 'SetupBunOutput']


@dataclass(frozen=True)
class SetupBunOutput:
    """Typed access to outputs produced by the setup_bun step.

    Parameters
    ----------
    id
        The ``id`` of the setup_bun step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`setup_bun`.

    Attributes
    ----------
    bun_version
        The version of Bun that was installed.
    bun_revision
        The revision of Bun that was installed.
    bun_path
        The path to the Bun executable.
    bun_download_url
        The URL from which Bun was downloaded.
    cache_hit
        Whether the Bun version was cached.

    See Also
    --------
    GitHub repository: https://github.com/oven-sh/setup-bun
    """

    id: str

    @property
    def bun_version(self) -> StringExpression:
        return context.steps[self.id].outputs['bun-version']

    @property
    def bun_revision(self) -> StringExpression:
        return context.steps[self.id].outputs['bun-revision']

    @property
    def bun_path(self) -> StringExpression:
        return context.steps[self.id].outputs['bun-path']

    @property
    def bun_download_url(self) -> StringExpression:
        return context.steps[self.id].outputs['bun-download-url']

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']


def setup_bun(
    *,
    name: Ostrlike = None,
    version: str = 'v2',
    bun_version: Ostrlike = None,
    bun_version_file: Ostrlike = None,
    bun_download_url: Ostrlike = None,
    registries: Ostrlike = None,
    no_cache: Oboollike = None,
    token: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Download, install, and set up Bun on the PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    bun_version
        The version of Bun to install (e.g. ``latest``, ``canary``, ``1.0.0``).
    bun_version_file
        The version of Bun to install from file (e.g. ``package.json``,
        ``.bun-version``).
    bun_download_url
        Override the URL to download Bun from.
    registries
        List of package registries with authentication support.
    no_cache
        Disable caching of the Bun executable.
    token
        Personal access token (PAT) used to fetch tags from oven-sh/bun.
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
        The generated setup-bun step.

    See Also
    --------
    GitHub repository: https://github.com/oven-sh/setup-bun
    """
    options: dict[str, object] = {
        'bun-version': bun_version,
        'bun-version-file': bun_version_file,
        'bun-download-url': bun_download_url,
        'registries': registries,
        'no-cache': no_cache,
        'token': token,
    }
    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Setup Bun'

    return action(
        name,
        'oven-sh/setup-bun',
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
