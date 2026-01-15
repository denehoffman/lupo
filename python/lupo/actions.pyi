from collections.abc import Mapping, Sequence
from typing import Literal, TypeAlias

from lupo import Step

Ostr: TypeAlias = str | None
Obool: TypeAlias = bool | None
Oint: TypeAlias = int | None


def checkout(
    *,
    name: Ostr = None,
    version: str = 'v6',
    repository: Ostr = None,
    ref: Ostr = None,
    token: Ostr = None,
    ssh_key: Ostr = None,
    ssh_known_hosts: Ostr = None,
    ssh_strict: Obool = None,
    ssh_user: Ostr = None,
    persist_credentials: Obool = None,
    path: Ostr = None,
    clean: Obool = None,
    filter: Ostr = None,  # noqa: A002
    sparse_checkout: Ostr = None,
    sparse_checkout_cone_mode: Obool = None,
    fetch_depth: Oint = None,
    fetch_tags: Obool = None,
    show_progress: Obool = None,
    lfs: Obool = None,
    submodules: Obool = None,
    get_safe_directory: Obool = None,
    github_server_url: Ostr = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Obool = None,
    timeout_seconds: Oint = None,
) -> Step: ...


def release(
    *,
    name: Ostr,
    version: str,
    body: Ostr,
    body_path: Ostr,
    draft: Obool,
    prerelease: Obool,
    preserve_order: Obool,
    files: Ostr,
    overwrite_files: Obool,
    release_name: Ostr,
    tag_name: Ostr,
    fail_on_unmatched_files: Obool,
    repository: Ostr,
    target_commitish: Ostr,
    token: Ostr,
    discussion_category_name: Ostr,
    generate_release_notes: Obool,
    append_body: Obool,
    make_latest: Ostr,
    args: Ostr,
    entrypoint: Ostr,
    condition: Ostr,
    working_directory: Ostr,
    shell: Ostr,
    id: Ostr,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Obool,
    timeout_seconds: Oint,
) -> Step: ...


def cache(
    *,
    key: str,
    name: Ostr = None,
    version: Ostr = 'v5',
    path: Sequence[str] | None = None,
    restore_keys: Sequence[str] | None = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
) -> Step: ...


def cache_save(
    *,
    key: str,
    name: Ostr = None,
    version: Ostr = 'v5',
    path: Sequence[str] | None = None,
    restore_keys: Sequence[str] | None = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
) -> Step: ...


def cache_restore(
    *,
    key: str,
    name: Ostr = None,
    version: Ostr = 'v5',
    path: Sequence[str] | None = None,
    restore_keys: Sequence[str] | None = None,
    enable_cross_os_archive: Obool = None,
    fail_on_cache_miss: Obool = None,
    lookup_only: Obool = None,
    segment_download_timeout_mins: Oint = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
) -> Step: ...


def upload_artifact(
    *,
    path: str,
    name: Ostr = None,
    version: str = 'v6',
    artifact_name: Ostr = None,
    if_no_files_found: Literal['warn', 'error', 'ignore'] | None = None,
    retention_days: Oint = None,
    compression_level: Oint = None,
    overwrite: Obool = None,
    include_hidden_files: Obool = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
) -> Step: ...


def upload_artifact_merge(
    *,
    pattern: Ostr = None,
    name: Ostr = None,
    version: str = 'v6',
    artifact_name: Ostr = None,
    separate_directories: Obool = None,
    delete_merged: Obool = None,
    retention_days: Oint = None,
    compression_level: Oint = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
) -> Step: ...


def download_artifact(
    *,
    path: Ostr = None,
    name: Ostr = None,
    version='v7',
    artifact_name: Ostr = None,
    artifact_ids: Sequence[str] | None = None,
    pattern: Ostr = None,
    merge_multiple: Obool = None,
    github_token: Ostr = None,
    repository: Ostr = None,
    run_id: Ostr = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, str] | None = None,
    continue_on_error: Ostr = None,
    timeout_minutes: Ostr = None,
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
