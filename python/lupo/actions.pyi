from collections.abc import Mapping, Sequence
from typing import TypeAlias

from lupo import Step
from lupo.expressions import BooleanExpression, NumberExpression, StringExpression

Ostr: TypeAlias = str | None
Obool: TypeAlias = bool | None
Oint: TypeAlias = int | None
StringLike: TypeAlias = str | StringExpression
BoolLike: TypeAlias = bool | BooleanExpression
IntLike: TypeAlias = int | NumberExpression
Ostrlike: TypeAlias = StringLike | None
Oboolstr: TypeAlias = BooleanExpression | str | None
Oboollike: TypeAlias = BoolLike | None
Ointlike: TypeAlias = IntLike | None

def checkout(
    *,
    name: Ostrlike = None,
    version: str = 'v6',
    repository: Ostrlike = None,
    ref: Ostrlike = None,
    token: Ostrlike = None,
    ssh_key: Ostrlike = None,
    ssh_known_hosts: Ostrlike = None,
    ssh_strict: Oboollike = None,
    ssh_user: Ostrlike = None,
    persist_credentials: Oboollike = None,
    path: Ostrlike = None,
    clean: Oboollike = None,
    filter: Ostrlike = None,  # noqa: A002
    sparse_checkout: Ostrlike = None,
    sparse_checkout_cone_mode: Oboollike = None,
    fetch_depth: Ointlike = None,
    fetch_tags: Oboollike = None,
    show_progress: Oboollike = None,
    lfs: Oboollike = None,
    submodules: Oboollike = None,
    get_safe_directory: Oboollike = None,
    github_server_url: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def release(
    *,
    name: Ostrlike = None,
    version: str = 'v2',
    body: Ostr = None,
    body_path: Ostr = None,
    draft: Obool = None,
    prerelease: Obool = None,
    preserve_order: Obool = None,
    files: Ostr = None,
    overwrite_files: Obool = None,
    release_name: Ostr = None,
    tag_name: Ostr = None,
    fail_on_unmatched_files: Obool = None,
    repository: Ostr = None,
    target_commitish: Ostr = None,
    token: Ostr = None,
    discussion_category_name: Ostr = None,
    generate_release_notes: Obool = None,
    append_body: Obool = None,
    make_latest: Ostr = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def cache(
    *,
    key: str,
    name: Ostrlike = None,
    version: str = 'v5',
    path: Sequence[str] | None = None,
    restore_keys: Sequence[str] | None = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def cache_save(
    *,
    key: str,
    name: Ostrlike = None,
    version: str = 'v5',
    path: Sequence[str] | None = None,
    restore_keys: Sequence[str] | None = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def cache_restore(
    *,
    key: StringLike,
    name: Ostrlike = None,
    version: str = 'v5',
    path: Sequence[StringLike] | None = None,
    restore_keys: Sequence[StringLike] | None = None,
    enable_cross_os_archive: Oboollike = None,
    fail_on_cache_miss: Oboollike = None,
    lookup_only: Oboollike = None,
    segment_download_timeout_mins: Ointlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
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
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
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
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def download_artifact(
    *,
    path: Ostrlike = None,
    name: Ostrlike = None,
    version: str = 'v7',
    artifact_name: Ostrlike = None,
    artifact_ids: Sequence[StringLike] | None = None,
    pattern: Ostrlike = None,
    merge_multiple: Oboollike = None,
    github_token: Ostrlike = None,
    repository: Ostrlike = None,
    run_id: Ostrlike = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...

__all__ = [
    'cache',
    'cache_restore',
    'cache_save',
    'checkout',
    'download_artifact',
    'release',
    'upload_artifact',
    'upload_artifact_merge',
]
