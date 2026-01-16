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
StringOrBoolLike: TypeAlias = StringLike | BoolLike

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
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def setup_python(
    *,
    name: Ostrlike = None,
    version: str = 'v6',
    python_version: Ostrlike = None,
    python_version_file: Ostrlike = None,
    check_latest: Oboollike = None,
    architecture: Ostrlike = None,
    token: Ostrlike = None,
    cache: Ostrlike = None,
    package_manager_cache: Oboollike = None,
    cache_dependency_path: Ostrlike = None,
    update_environment: Oboollike = None,
    allow_prereleases: Oboollike = None,
    freethreaded: Oboollike = None,
    pip_versions: Ostrlike = None,
    pip_install: Ostrlike = None,
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
def setup_go(
    *,
    name: Ostrlike = None,
    version: str = 'v6',
    go_version: Ostrlike = None,
    go_version_file: Ostrlike = None,
    check_latest: Oboollike = None,
    architecture: Ostrlike = None,
    token: Ostrlike = None,
    cache: Oboollike = None,
    cache_dependency_path: Ostrlike = None,
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
def setup_rust(
    *,
    name: Ostrlike = None,
    version: str = 'v1',
    toolchain: Ostrlike = None,
    target: Ostrlike = None,
    components: Sequence[StringLike] | None = None,
    cache: Oboollike = None,
    cache_directories: Sequence[StringLike] | None = None,
    cache_workspaces: Sequence[StringLike] | None = None,
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
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def install_rust_tool(
    *,
    tool: Sequence[StringLike],
    name: Ostrlike = None,
    version: str = 'v1',
    checksum: Oboollike = None,
    fallback: Ostrlike = None,
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
def setup_uv(
    *,
    name: Ostrlike = None,
    version: str = 'v7',
    uv_version: Ostrlike = None,
    uv_version_file: Ostrlike = None,
    resolution_strategy: Ostrlike = None,
    python_version: Ostrlike = None,
    activate_environment: Oboollike = None,
    uv_working_directory: Ostrlike = None,
    checksum: Ostrlike = None,
    github_token: Ostrlike = None,
    enable_cache: StringOrBoolLike | None = None,
    cache_dependency_glob: Sequence[StringLike] | None = None,
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
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...

__all__ = ['install_rust_tool', 'setup_go', 'setup_node', 'setup_python', 'setup_rust', 'setup_uv']
