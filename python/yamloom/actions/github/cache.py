from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from ...expressions import context, StringExpression
from ..._yamloom import Step
from ..._yamloom import action
from ..types import (
    Obool,
    Oboollike,
    Oboolstr,
    Oint,
    Ointlike,
    Ostr,
    Ostrlike,
    StringLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = [
    'cache',
    'cache_restore',
    'cache_save',
    'CacheOutput',
    'CacheRestoreOutput',
]


@dataclass(frozen=True)
class CacheOutput:
    """Typed access to outputs produced by the cache step.

    Parameters
    ----------
    id
        The ``id`` of the cache step whose outputs should be referenced. This
        should match the ``id`` passed to :func:`cache`.

    Attributes
    ----------
    cache_hit
        A boolean value to indicate an exact match was found for the primary key.

    See Also
    --------
    GitHub repository: https://github.com/actions/cache
    """

    id: str

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']


@dataclass(frozen=True)
class CacheRestoreOutput:
    """Typed access to outputs produced by the cache_restore step.

    Parameters
    ----------
    id
        The ``id`` of the cache_restore step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`cache_restore`.

    Attributes
    ----------
    cache_hit
        A boolean value to indicate an exact match was found for the primary key.
    cache_primary_key
        A resolved cache key for which cache match was attempted.
    cache_matched_key
        Key of the cache that was restored, either the primary key on cache-hit
        or a partial/complete match of one of the restore keys.

    See Also
    --------
    GitHub repository: https://github.com/actions/cache
    """

    id: str

    @property
    def cache_hit(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-hit']

    @property
    def cache_primary_key(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-primary-key']

    @property
    def cache_matched_key(self) -> StringExpression:
        return context.steps[self.id].outputs['cache-matched-key']


def cache(
    *,
    key: str,
    name: Ostrlike = None,
    version: str = 'v5',
    path: list[str] | None = None,
    restore_keys: list[str] | None = None,
    upload_chunk_size: Ointlike = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    save_always: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Cache artifacts like dependencies and build outputs.

    Parameters
    ----------
    key
        An explicit key for restoring and saving the cache.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    path
        A list of files, directories, and wildcard patterns to cache and restore.
    restore_keys
        An ordered multiline string listing the prefix-matched keys that are used
        for restoring stale cache if no cache hit occurred for ``key``. Note
        ``cache_hit`` returns false in this case.
    upload_chunk_size
        The chunk size used to split up large files during upload, in bytes.
    enable_cross_os_archive
        An optional boolean when enabled, allows Windows runners to save or
        restore caches that can be restored or saved respectively on other
        platforms.
    fail_on_cache_miss
        Fail the workflow if cache entry is not found.
    lookup_only
        Check if a cache entry exists for the given input(s) (``key``,
        ``restore_keys``) without downloading the cache.
    save_always
        Run the post step to save the cache even if another step before fails.
        This does not work as intended and will be removed in a future release.
        A separate ``actions/cache/restore`` step should be used instead.
    segment_download_timeout_mins
        The download segment timeout (in minutes) used by the cache action.
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
        The generated cache step.

    See Also
    --------
    GitHub repository: https://github.com/actions/cache
    """
    options: dict[str, object] = {
        'key': key,
        'path': list(path) if path is not None else None,
        'restore-keys': list(restore_keys) if restore_keys is not None else None,
        'upload-chunk-size': upload_chunk_size,
        'enableCrossOsArchive': enable_cross_os_archive,
        'fail-on-cache-miss': fail_on_cache_miss,
        'lookup-only': lookup_only,
        'save-always': save_always,
    }
    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Save/Restore Cache'

    if segment_download_timeout_mins is not None:
        merged_env = dict(env or {})
        merged_env['SEGMENT_DOWNLOAD_TIMEOUT_MINS'] = str(segment_download_timeout_mins)
        env = merged_env

    return action(
        name,
        'actions/cache',
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


def cache_save(
    *,
    key: str,
    name: Ostrlike = None,
    version: str = 'v5',
    path: list[str] | None = None,
    upload_chunk_size: Ointlike = None,
    enable_cross_os_archive: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Save cache artifacts like dependencies and build outputs.

    Parameters
    ----------
    key
        An explicit key for saving the cache.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    path
        A list of files, directories, and wildcard patterns to cache.
    upload_chunk_size
        The chunk size used to split up large files during upload, in bytes.
    enable_cross_os_archive
        An optional boolean when enabled, allows Windows runners to save caches
        that can be restored on other platforms.
    segment_download_timeout_mins
        The download segment timeout (in minutes) used by the cache action.
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
        The generated cache save step.

    See Also
    --------
    GitHub repository: https://github.com/actions/cache
    """
    options: dict[str, object] = {
        'key': key,
        'path': list(path) if path is not None else None,
        'upload-chunk-size': upload_chunk_size,
        'enableCrossOsArchive': enable_cross_os_archive,
    }
    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Save Cache'

    if segment_download_timeout_mins is not None:
        merged_env = dict(env or {})
        merged_env['SEGMENT_DOWNLOAD_TIMEOUT_MINS'] = str(segment_download_timeout_mins)
        env = merged_env

    return action(
        name,
        'actions/cache/save',
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


def cache_restore(
    *,
    key: StringLike,
    name: Ostrlike = None,
    version: str = 'v5',
    path: list[StringLike] | None = None,
    restore_keys: list[StringLike] | None = None,
    enable_cross_os_archive: Oboollike = None,
    fail_on_cache_miss: Oboollike = None,
    lookup_only: Oboollike = None,
    segment_download_timeout_mins: Ointlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Restore cache artifacts like dependencies and build outputs.

    Parameters
    ----------
    key
        An explicit key for restoring the cache.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    path
        A list of files, directories, and wildcard patterns to restore.
    restore_keys
        An ordered multiline string listing the prefix-matched keys that are used
        for restoring stale cache if no cache hit occurred for ``key``. Note
        ``cache_hit`` returns false in this case.
    enable_cross_os_archive
        An optional boolean when enabled, allows Windows runners to restore caches
        that were saved on other platforms.
    fail_on_cache_miss
        Fail the workflow if cache entry is not found.
    lookup_only
        Check if a cache entry exists for the given input(s) (``key``,
        ``restore_keys``) without downloading the cache.
    segment_download_timeout_mins
        The download segment timeout (in minutes) used by the cache action.
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
        The generated cache restore step.

    See Also
    --------
    GitHub repository: https://github.com/actions/cache
    """
    options: dict[str, object] = {
        'key': key,
        'path': list(path) if path is not None else None,
        'restore-keys': list(restore_keys) if restore_keys is not None else None,
        'enableCrossOsArchive': enable_cross_os_archive,
        'fail-on-cache-miss': fail_on_cache_miss,
        'lookup-only': lookup_only,
    }
    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        name = 'Restore Cache'

    if segment_download_timeout_mins is not None:
        merged_env = dict(env or {})
        merged_env['SEGMENT_DOWNLOAD_TIMEOUT_MINS'] = str(segment_download_timeout_mins)
        env = merged_env

    return action(
        name,
        'actions/cache/restore',
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
