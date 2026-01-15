from collections.abc import Mapping, Sequence
from types import ModuleType
from typing import Literal

from typing_extensions import TypeAlias

Ostr: TypeAlias = str | None
Obool: TypeAlias = bool | None
Oint: TypeAlias = int | None


actions: ModuleType


class Step: ...


def script(
    name: str,
    script: str,
    *,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    continue_on_error: Obool = None,
    timeout_seconds: Oint = None,
) -> Step: ...


def action(
    name: str,
    action: str,
    *,
    ref: Ostr = None,
    with_opts: Mapping | None = None,
    args: Ostr = None,
    entrypoint: Ostr = None,
    condition: Ostr = None,
    working_directory: Ostr = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    continue_on_error: Obool = None,
    timeout_seconds: Oint = None,
) -> Step: ...


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
    continue_on_error: Obool = None,
    timeout_seconds: Oint = None,
) -> Step: ...


RW: TypeAlias = Literal['read', 'write', 'none'] | None
RO: TypeAlias = Literal['read', 'none'] | None
WO: TypeAlias = Literal['write', 'none'] | None


class Permissions:
    def __init__(
        self,
        actions: RW = None,
        artifact_metadata: RW = None,
        attestations: RW = None,
        checks: RW = None,
        contents: RW = None,
        deployments: RW = None,
        id_token: WO = None,
        issues: RW = None,
        models: RO = None,
        discussions: RW = None,
        packages: RW = None,
        pages: RW = None,
        pull_requests: RW = None,
        security_events: RW = None,
        statuses: RW = None,
    ) -> None: ...
    @staticmethod
    def none() -> Permissions: ...
    @staticmethod
    def read_all() -> Permissions: ...
    @staticmethod
    def write_all() -> Permissions: ...


class RunsOnSpec:
    def __init__(self, group: str, labels: str) -> None: ...
    @staticmethod
    def group(group: str) -> RunsOnSpec: ...
    @staticmethod
    def labels(labels: str) -> RunsOnSpec: ...


class RunsOn:
    def __init__(self, *args: str) -> None: ...
    @staticmethod
    def spec(spec: RunsOnSpec) -> RunsOn: ...


class Environment:
    def __init__(self, name: str, url: Ostr = None) -> None: ...


class Concurrency:
    def __init__(self, group: str, cancel_in_progress: bool = True) -> None: ...


class Defaults:
    def __init__(self, *, shell: str, working_directory: str) -> None: ...
    @staticmethod
    def shell(shell: str) -> Defaults: ...
    @staticmethod
    def working_directory(working_directory: str) -> Defaults: ...


class Matrix:
    def __init__(
        self, *, include: Sequence | None = None, exclude: Sequence | None = None, matrix: Mapping | None = None
    ) -> None: ...


class Strategy:
    def __init__(self, *, matrix: Matrix | None = None, fast_fail: Obool = None, max_parallel: Oint = None) -> None: ...


class Credentials:
    def __init__(self, username: str, password: str) -> None: ...


class Container:
    def __init__(
        self,
        image: str,
        *,
        credentials: Credentials | None = None,
        env: Mapping[str, str] | None = None,
        ports: Sequence[int] | None = None,
        volumes: Sequence[str] | None = None,
        options: Ostr = None,
    ) -> None: ...


class JobSecrets:
    def __init__(self, secrets: Mapping[str, str]) -> None: ...
    @staticmethod
    def inherit() -> JobSecrets: ...


class Job:
    def __init__(
        self,
        steps: Sequence[Step],
        *,
        name: Ostr = None,
        permissions: Permissions | None = None,
        needs: Sequence[str] | None = None,
        condition: Ostr = None,
        runs_on: RunsOnSpec | Sequence[str] | str | None = None,
        snapshot: Ostr = None,
        environment: Environment | None = None,
        concurrency: Concurrency | None = None,
        outputs: Mapping[str, str] | None = None,
        env: Mapping[str, str] | None = None,
        defaults: Defaults | None = None,
        timeout_minutes: Oint = None,
        strategy: Strategy | None = None,
        continue_on_error: str | bool | None = None,
        container: Container | None = None,
        services: Mapping[str, Container] | None = None,
        uses: Ostr = None,
        with_opts: Mapping | None = None,
        secrets: JobSecrets | None = None,
    ) -> None: ...


class BranchProtectionRuleEvent:
    def __init__(self, *, created: bool = False, edited: bool = False, deleted: bool = False) -> None: ...


class CheckRunEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        rerequested: bool = False,
        completed: bool = False,
        requested_action: bool = False,
    ) -> None: ...


class CheckSuiteEvent:
    def __init__(self, *, created: bool = False) -> None: ...


class DiscussionEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        transferred: bool = False,
        pinned: bool = False,
        unpinned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        category_changed: bool = False,
        answered: bool = False,
        unanswered: bool = False,
    ) -> None: ...


class DiscussionCommentEvent:
    def __init__(self, *, created: bool = False, edited: bool = False, deleted: bool = False) -> None: ...


class ImageVersionEvent:
    def __init__(self, *, names: Sequence[str] | None = None, versions: Sequence[str] | None = None) -> None: ...


class IssueCommentEvent:
    def __init__(self, *, created: bool = False, edited: bool = False, deleted: bool = False) -> None: ...


class IssuesEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        transferred: bool = False,
        pinned: bool = False,
        unpinned: bool = False,
        closed: bool = False,
        reopened: bool = False,
        assigned: bool = False,
        unassigned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        milestoned: bool = False,
        demilestoned: bool = False,
        typed: bool = False,
        untyped: bool = False,
    ) -> None: ...


class LabelEvent:
    def __init__(self, *, created: bool = False, edited: bool = False, deleted: bool = False) -> None: ...


class MergeGroupEvent:
    def __init__(self, *, checks_requested: bool = False) -> None: ...


class MilestoneEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        closed: bool = False,
        opened: bool = False,
        edited: bool = False,
        deleted: bool = False,
    ) -> None: ...


class PullRequestEvent:
    def __init__(
        self,
        *,
        branches: Sequence[str] | None = None,
        branches_ignore: Sequence[str] | None = None,
        paths: Sequence[str] | None = None,
        paths_ignore: Sequence[str] | None = None,
        assigned: bool = False,
        unassigned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        edited: bool = False,
        closed: bool = False,
        reopened: bool = False,
        synchronize: bool = False,
        converted_to_draft: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        enqueued: bool = False,
        dequeued: bool = False,
        milestoned: bool = False,
        demilestoned: bool = False,
        ready_for_review: bool = False,
        review_requested: bool = False,
        review_request_removed: bool = False,
        auto_merge_enabled: bool = False,
        auto_merge_disabled: bool = False,
    ) -> None: ...


class PullRequestReviewEvent:
    def __init__(self, *, submitted: bool = False, edited: bool = False, dismissed: bool = False) -> None: ...


class PullRequestReviewCommentEvent:
    def __init__(self, *, created: bool = False, edited: bool = False, deleted: bool = False) -> None: ...


class PushEvent:
    def __init__(
        self,
        *,
        branches: Sequence[str] | None = None,
        branches_ignore: Sequence[str] | None = None,
        tags: Sequence[str] | None = None,
        tags_ignore: Sequence[str] | None = None,
        paths: Sequence[str] | None = None,
        paths_ignore: Sequence[str] | None = None,
    ) -> None: ...


class RegistryPackageEvent:
    def __init__(self, *, published: bool = False, updated: bool = False) -> None: ...


class ReleaseEvent:
    def __init__(
        self,
        *,
        published: bool = False,
        unpublished: bool = False,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        prereleased: bool = False,
        released: bool = False,
    ) -> None: ...


class RepositoryDispatchEvent:
    def __init__(self, *, types: Sequence[str] | None = None) -> None: ...


class Minute:
    def __init__(self, minute: int | Sequence[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Minute: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Minute: ...


class Hour:
    def __init__(self, minute: int | Sequence[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Hour: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Hour: ...


class Day:
    def __init__(self, minute: int | Sequence[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Day: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Day: ...


class Month:
    def __init__(self, minute: int | Sequence[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Month: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Month: ...


class DayOfWeek:
    def __init__(self, minute: int | Sequence[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> DayOfWeek: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> DayOfWeek: ...


class Cron:
    def __init__(
        self,
        *,
        minute: Minute | None = None,
        hour: Hour | None = None,
        day: Day | None = None,
        month: Month | None = None,
        day_of_week: DayOfWeek | None = None,
    ) -> None: ...


class ScheduleEvent:
    def __init__(self, *, crons: Sequence[Cron] | None = None) -> None: ...


class WatchEvent:
    def __init__(self, *, started: bool = False) -> None: ...


class WorkflowInput:
    @staticmethod
    def boolean(*, description: Ostr = None, default: Obool = None, required: Obool = None) -> WorkflowInput: ...
    @staticmethod
    def number(*, description: Ostr = None, default: Oint = None, required: Obool = None) -> WorkflowInput: ...
    @staticmethod
    def string(*, description: Ostr = None, default: Ostr = None, required: Obool = None) -> WorkflowInput: ...


class WorkflowOutput:
    def __init__(self, value: str, *, description: Ostr = None) -> None: ...


class WorkflowSecret:
    def __init__(self, *, description: Ostr = None, required: Obool = None) -> None: ...


class WorkflowCallEvent:
    def __init__(
        self,
        *,
        inputs: Mapping[str, WorkflowInput] | None = None,
        outputs: Mapping[str, WorkflowOutput] | None = None,
        secrets: Mapping[str, WorkflowSecret] | None = None,
    ) -> None: ...


class WorkflowDispatchInput:
    @staticmethod
    def boolean(
        *, description: Ostr = None, default: Obool = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def choice(
        options: Sequence[str], *, description: Ostr = None, default: Ostr = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def number(*, description: Ostr = None, default: Oint = None, required: Obool = None) -> WorkflowDispatchInput: ...
    @staticmethod
    def environment(*, description: Ostr = None, required: Obool = None) -> WorkflowDispatchInput: ...
    @staticmethod
    def string(*, description: Ostr = None, default: Ostr = None, required: Obool = None) -> WorkflowDispatchInput: ...


class WorkflowDispatchEvent:
    def __init__(self, *, inputs: Mapping[str, WorkflowDispatchInput] | None = None) -> None: ...


class WorkflowRunEvent:
    def __init__(
        self,
        *,
        workflows: Sequence[str] | None = None,
        completed: bool = False,
        requested: bool = False,
        in_progress: bool = False,
        branches: Sequence[str] | None = None,
        branches_ignore: Sequence[str] | None = None,
    ) -> None: ...


class Events:
    def __init__(
        self,
        branch_protection_rule: BranchProtectionRuleEvent | None = None,
        check_run: CheckRunEvent | None = None,
        check_suite: CheckSuiteEvent | None = None,
        create: bool = False,
        delete: bool = False,
        deployment: bool = False,
        deployment_status: bool = False,
        discussion: DiscussionEvent | None = None,
        discussion_comment: DiscussionCommentEvent | None = None,
        fork: bool = False,
        gollum: bool = False,
        image_version: ImageVersionEvent | None = None,
        issue_comment: IssueCommentEvent | None = None,
        issues: IssuesEvent | None = None,
        label: LabelEvent | None = None,
        merge_group: MergeGroupEvent | None = None,
        milestone: MilestoneEvent | None = None,
        page_build: bool = False,
        public: bool = False,
        pull_request: PullRequestEvent | None = None,
        pull_request_review: PullRequestReviewEvent | None = None,
        pull_request_review_comment: PullRequestReviewCommentEvent | None = None,
        pull_request_target: PullRequestEvent | None = None,
        push: PushEvent | None = None,
        registry_package: RegistryPackageEvent | None = None,
        release: ReleaseEvent | None = None,
        schedule: ScheduleEvent | None = None,
        status: bool = False,
        watch: WatchEvent | None = None,
        workflow_call: WorkflowCallEvent | None = None,
        workflow_dispatch: WorkflowDispatchEvent | None = None,
        workflow_run: WorkflowRunEvent | None = None,
    ) -> None: ...


class Workflow:
    def __init__(
        self,
        *,
        jobs: Mapping[str, Job],
        on: Events,
        name: Ostr = None,
        run_name: Ostr = None,
        permissions: Permissions | None = None,
        env: Mapping[str, str] | None = None,
        defaults: Defaults | None = None,
        run_defaults: Defaults | None = None,
        concurrency: Concurrency | None = None,
    ) -> None: ...


__all__ = [
    'BranchProtectionRuleEvent',
    'CheckRunEvent',
    'CheckSuiteEvent',
    'Concurrency',
    'Container',
    'Container',
    'Credentials',
    'Cron',
    'Day',
    'DayOfWeek',
    'Defaults',
    'DiscussionCommentEvent',
    'DiscussionEvent',
    'Environment',
    'Events',
    'Hour',
    'ImageVersionEvent',
    'IssueCommentEvent',
    'IssuesEvent',
    'Job',
    'JobSecrets',
    'LabelEvent',
    'Matrix',
    'MergeGroupEvent',
    'MilestoneEvent',
    'Minute',
    'Month',
    'Permissions',
    'PullRequestEvent',
    'PullRequestReviewCommentEvent',
    'PullRequestReviewEvent',
    'PushEvent',
    'RegistryPackageEvent',
    'ReleaseEvent',
    'RepositoryDispatchEvent',
    'RunsOnSpec',
    'ScheduleEvent',
    'Step',
    'Strategy',
    'WatchEvent',
    'Workflow',
    'WorkflowCallEvent',
    'WorkflowDispatchEvent',
    'WorkflowDispatchInput',
    'WorkflowInput',
    'WorkflowOutput',
    'WorkflowRunEvent',
    'WorkflowSecret',
    'action',
    'script',
]
