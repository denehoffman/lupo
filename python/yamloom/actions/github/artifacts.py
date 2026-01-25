from __future__ import annotations
from yamloom.actions.utils import validate_choice, check_string

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

WARN_RETENTION_DAYS: int = 90
MAX_COMPRESSION_LEVEL: int = 9

__all__ = [
    'download_artifact',
    'upload_artifact',
    'upload_artifact_merge',
    'DownloadArtifactOutput',
    'UploadArtifactOutput',
    'UploadArtifactMergeOutput',
]


@dataclass(frozen=True)
class UploadArtifactOutput:
    """Typed access to outputs produced by the upload_artifact step.

    Parameters
    ----------
    id
        The ``id`` of the upload_artifact step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`upload_artifact`.

    Attributes
    ----------
    artifact_id
        A unique identifier for the artifact that was just uploaded. Empty if the
        artifact upload failed.
    artifact_url
        A download URL for the artifact that was just uploaded. Empty if the artifact
        upload failed. This URL is valid only while the artifact, workflow run, and
        repository exist.
    artifact_digest
        SHA-256 digest for the artifact that was just uploaded. Empty if the artifact
        upload failed.

    See Also
    --------
    GitHub repository: https://github.com/actions/upload-artifact
    """

    id: str

    @property
    def artifact_id(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-id']

    @property
    def artifact_url(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-url']

    @property
    def artifact_digest(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-digest']


@dataclass(frozen=True)
class UploadArtifactMergeOutput:
    """Typed access to outputs produced by the upload_artifact_merge step.

    Parameters
    ----------
    id
        The ``id`` of the upload_artifact_merge step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`upload_artifact_merge`.

    Attributes
    ----------
    artifact_id
        A unique identifier for the artifact that was just uploaded. Empty if the
        artifact upload failed.
    artifact_url
        A download URL for the artifact that was just uploaded. Empty if the artifact
        upload failed. This URL is valid only while the artifact, workflow run, and
        repository exist.
    artifact_digest
        SHA-256 digest for the artifact that was just uploaded. Empty if the artifact
        upload failed.

    See Also
    --------
    GitHub repository: https://github.com/actions/upload-artifact
    """

    id: str

    @property
    def artifact_id(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-id']

    @property
    def artifact_url(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-url']

    @property
    def artifact_digest(self) -> StringExpression:
        return context.steps[self.id].outputs['artifact-digest']


@dataclass(frozen=True)
class DownloadArtifactOutput:
    """Typed access to outputs produced by the download_artifact step.

    Parameters
    ----------
    id
        The ``id`` of the download_artifact step whose outputs should be referenced.
        This should match the ``id`` passed to :func:`download_artifact`.

    Attributes
    ----------
    download_path
        Path of artifact download.

    See Also
    --------
    GitHub repository: https://github.com/actions/download-artifact
    """

    id: str

    @property
    def download_path(self) -> StringExpression:
        return context.steps[self.id].outputs['download-path']


def upload_artifact(
    *,
    path: StringLike,
    name: Ostrlike = None,
    version: str = 'v6',
    artifact_name: Ostrlike = None,
    if_no_files_found: Ostrlike = None,
    retention_days: Ointlike = None,
    compression_level: Ointlike = None,
    overwrite: Oboollike = None,
    include_hidden_files: Oboollike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Upload a build artifact that can be used by subsequent workflow steps.

    Parameters
    ----------
    path
        A file, directory or wildcard pattern that describes what to upload.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    artifact_name
        Artifact name.
    if_no_files_found
        The desired behavior if no files are found using the provided path. Available
        options are ``warn``, ``error``, and ``ignore``.
    retention_days
        Duration after which artifact will expire in days. ``0`` means using default
        retention. Minimum 1 day. Maximum 90 days unless changed from the repository
        settings page.
    compression_level
        The level of compression for Zlib to be applied to the artifact archive.
        The value can range from 0 to 9, where 0 is no compression and 9 is best
        compression. Higher levels take longer to complete.
    overwrite
        If true, an artifact with a matching name will be deleted before a new one
        is uploaded. If false, the action will fail if an artifact for the given name
        already exists. Does not fail if the artifact does not exist.
    include_hidden_files
        If true, hidden files will be included in the artifact. If false, hidden files
        will be excluded from the artifact.
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
        The generated upload artifact step.

    See Also
    --------
    GitHub repository: https://github.com/actions/upload-artifact
    """
    options: dict[str, object] = {
        'path': path,
        'name': artifact_name,
        'if_no_files_found': validate_choice(
            'if_no_files_found', if_no_files_found, ['warn', 'error', 'ignore']
        ),
        'retention-days': retention_days,
        'compression-level': compression_level,
        'overwrite': overwrite,
        'include-hidden-files': include_hidden_files,
    }

    if retention_days is not None:
        if isinstance(retention_days, int) and not isinstance(retention_days, bool):
            if retention_days < 1:
                msg = 'retention days must be > 0'
                raise ValueError(msg)
            if retention_days > WARN_RETENTION_DAYS:
                print(
                    f'Warning: retention days should be <= {WARN_RETENTION_DAYS} unless a higher limit is made in the repository settings!'
                )
        options['retention-days'] = retention_days

    if compression_level is not None:
        if (
            isinstance(compression_level, int)
            and not isinstance(compression_level, bool)
        ) and (compression_level < 0 or compression_level > MAX_COMPRESSION_LEVEL):
            msg = f'compression level must be in the range 0-{MAX_COMPRESSION_LEVEL}'
            raise ValueError(msg)
        options['compression-level'] = compression_level

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        artifact_str = check_string(options.get('artifact_name'))
        if artifact_str:
            name = f'Upload {artifact_str}'
        else:
            name = 'Upload Artifact'

    return action(
        name,
        'actions/upload-artifact',
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


def upload_artifact_merge(
    *,
    pattern: Ostrlike = None,
    name: Ostrlike = None,
    version: str = 'v6',
    artifact_name: Ostrlike = None,
    separate_directories: Oboollike = None,
    delete_merged: Oboollike = None,
    retention_days: Ointlike = None,
    compression_level: Ointlike = None,
    include_hidden_files: Oboollike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Merge one or more build artifacts.

    Parameters
    ----------
    pattern
        A glob pattern matching the artifact names that should be merged.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    artifact_name
        The name of the artifact that the artifacts will be merged into.
    separate_directories
        When multiple artifacts are matched, this changes the behavior of how they are
        merged in the archive. If true, the matched artifacts are extracted into
        individual named directories within the specified path. If false, the matched
        artifacts are combined in the same directory.
    delete_merged
        If true, the artifacts that were merged will be deleted. If false, the artifacts
        will still exist.
    retention_days
        Duration after which artifact will expire in days. ``0`` means using default
        retention. Minimum 1 day. Maximum 90 days unless changed from the repository
        settings page.
    compression_level
        The level of compression for Zlib to be applied to the artifact archive.
        The value can range from 0 to 9, where 0 is no compression and 9 is best
        compression. Higher levels take longer to complete.
    include_hidden_files
        If true, hidden files will be included in the merged artifact. If false, hidden
        files will be excluded from the merged artifact.
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
        The generated upload merge step.

    See Also
    --------
    GitHub repository: https://github.com/actions/upload-artifact
    """
    options: dict[str, object] = {
        'name': artifact_name,
        'pattern': pattern,
        'separate-directories': separate_directories,
        'delete-merged': delete_merged,
        'retention-days': retention_days,
        'compression-level': compression_level,
        'include-hidden-files': include_hidden_files,
    }

    if retention_days is not None:
        if isinstance(retention_days, int) and not isinstance(retention_days, bool):
            if retention_days < 1:
                msg = 'retention days must be > 0'
                raise ValueError(msg)
            if retention_days > WARN_RETENTION_DAYS:
                print(
                    f'Warning: retention days should be <= {WARN_RETENTION_DAYS} unless a higher limit is made in the repository settings!'
                )
        options['retention-days'] = retention_days

    if compression_level is not None:
        if (
            isinstance(compression_level, int)
            and not isinstance(compression_level, bool)
        ) and (compression_level < 0 or compression_level > MAX_COMPRESSION_LEVEL):
            msg = f'compression level must be in the range 0-{MAX_COMPRESSION_LEVEL}'
            raise ValueError(msg)
        options['compression-level'] = compression_level

    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        artifact_str = check_string(options.get('artifact_name'))
        if artifact_str:
            name = f'Upload (merged) {artifact_str}'
        else:
            name = 'Upload (merged) Artifact'

    return action(
        name,
        'actions/upload-artifact/merge',
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


def download_artifact(
    *,
    path: Ostrlike = None,
    name: Ostrlike = None,
    version: str = 'v7',
    artifact_name: Ostrlike = None,
    artifact_ids: list[StringLike] | None = None,
    pattern: Ostrlike = None,
    merge_multiple: Oboollike = None,
    github_token: Ostrlike = None,
    repository: Ostrlike = None,
    run_id: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step:
    """Download a build artifact that was previously uploaded in the workflow.

    Parameters
    ----------
    path
        Destination path. Supports basic tilde expansion. Defaults to ``$GITHUB_WORKSPACE``.
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    artifact_name
        Name of the artifact to download. If unspecified, all artifacts for the run
        are downloaded.
    artifact_ids
        IDs of the artifacts to download. Either ``artifact_ids`` or ``artifact_name``
        can be used, but not both.
    pattern
        A glob pattern matching the artifacts that should be downloaded. Ignored if
        ``artifact_name`` is specified.
    merge_multiple
        When multiple artifacts are matched, this changes the behavior of the
        destination directories. If true, the downloaded artifacts will be in the
        same directory specified by path. If false, the downloaded artifacts will be
        extracted into individual named directories within the specified path.
    github_token
        The GitHub token used to authenticate with the GitHub API. This is required
        when downloading artifacts from a different repository or from a different
        workflow run. If this is not specified, the action will attempt to download
        artifacts from the current repository and the current workflow run.
    repository
        The repository owner and the repository name joined together by ``/``. If
        ``github_token`` is specified, this is the repository that artifacts will be
        downloaded from.
    run_id
        The id of the workflow run where the desired download artifact was uploaded
        from. If ``github_token`` is specified, this is the run that artifacts will be
        downloaded from.
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
        The generated download artifact step.

    See Also
    --------
    GitHub repository: https://github.com/actions/download-artifact
    """
    options: dict[str, object] = {
        'name': artifact_name,
        'artifact-ids': ','.join(str(s) for s in artifact_ids)
        if artifact_ids is not None
        else None,
        'pattern': pattern,
        'path': path,
        'merge-multiple': merge_multiple,
        'github-token': github_token,
        'repository': repository,
        'run-id': run_id,
    }
    options = {key: value for key, value in options.items() if value is not None}

    if name is None:
        artifact_str = check_string(options.get('artifact_name'))
        if artifact_str:
            name = f'Download {artifact_str}'
        else:
            name = 'Download Artifact'

    return action(
        name,
        'actions/download-artifact',
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
