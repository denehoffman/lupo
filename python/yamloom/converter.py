from __future__ import annotations

import inspect
import json
import pprint
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Union, get_args, get_origin, get_type_hints

from ._yamloom import _parse_yaml


class ConversionError(ValueError):
    pass


@dataclass
class _Emitter:
    imports: dict[str, set[str]] = field(default_factory=dict)

    def imported(self, module: str, name: str) -> str:
        self.imports.setdefault(module, set()).add(name)
        return name

    def value(self, value: Any) -> str:
        return pprint.pformat(value, sort_dicts=False, width=88)

    def call(self, name: str, /, *args: str, **kwargs: str | None) -> str:
        values = [
            *args,
            *(f'{key}={value}' for key, value in kwargs.items() if value is not None),
        ]
        if not values:
            return f'{name}()'
        if (
            all('\n' not in value for value in values)
            and len(name) + sum(map(len, values)) < 76
        ):
            return f'{name}({", ".join(values)})'
        body = ''.join(f'    {value},\n' for value in values)
        return f'{name}(\n{body})'

    def mapping(self, values: Mapping[str, str]) -> str:
        if not values:
            return '{}'
        return (
            '{\n'
            + ''.join(
                f'    {key!r}: {_indent(value, 4)},\n' for key, value in values.items()
            )
            + '}'
        )


def _indent(value: str, spaces: int) -> str:
    indentation = ' ' * spaces
    return value.replace('\n', f'\n{indentation}')


ACTION_REGISTRY: dict[str, tuple[str, str, dict[str, str]]] = {
    'actions/checkout': ('yamloom.actions.github.scm', 'Checkout', {}),
    'actions/setup-python': ('yamloom.actions.toolchains.python', 'SetupPython', {}),
    'astral-sh/setup-uv': ('yamloom.actions.toolchains.python', 'SetupUV', {}),
    'actions/setup-node': ('yamloom.actions.toolchains.node', 'SetupNode', {}),
    'pnpm/action-setup': ('yamloom.actions.toolchains.node', 'SetupPnpm', {}),
    'actions/setup-go': ('yamloom.actions.toolchains.go', 'SetupGo', {}),
    'actions/setup-java': ('yamloom.actions.toolchains.java', 'SetupJava', {}),
    'actions/setup-dotnet': ('yamloom.actions.toolchains.dotnet', 'SetupDotnet', {}),
    'ruby/setup-ruby': ('yamloom.actions.toolchains.ruby', 'SetupRuby', {}),
    'shivammathur/setup-php': ('yamloom.actions.toolchains.php', 'SetupPhp', {}),
    'oven-sh/setup-bun': ('yamloom.actions.toolchains.javascript', 'SetupBun', {}),
    'actions-rust-lang/setup-rust-toolchain': (
        'yamloom.actions.toolchains.rust',
        'SetupRust',
        {},
    ),
    'taiki-e/install-action': (
        'yamloom.actions.toolchains.rust',
        'InstallRustTool',
        {},
    ),
    'mpi4py/setup-mpi': ('yamloom.actions.toolchains.system', 'SetupMPI', {}),
    'actions/upload-artifact': (
        'yamloom.actions.github.artifacts',
        'UploadArtifact',
        {'name': 'artifact_name'},
    ),
    'actions/download-artifact': (
        'yamloom.actions.github.artifacts',
        'DownloadArtifact',
        {'name': 'artifact_name'},
    ),
    'actions/cache': ('yamloom.actions.github.cache', 'Cache', {}),
    'actions/attest-build-provenance': (
        'yamloom.actions.github.attest',
        'AttestBuildProvenance',
        {},
    ),
    'softprops/action-gh-release': ('yamloom.actions.github.release', 'Release', {}),
    'googleapis/release-please-action': (
        'yamloom.actions.github.release',
        'ReleasePlease',
        {},
    ),
    'pypa/gh-action-pypi-publish': (
        'yamloom.actions.packaging.python',
        'PypiPublish',
        {},
    ),
    'PyO3/maturin-action': ('yamloom.actions.packaging.python', 'Maturin', {}),
    'codecov/codecov-action': ('yamloom.actions.ci.coverage', 'Codecov', {}),
}


def _kwargs(
    data: Mapping[str, Any], emitter: _Emitter, *, aliases: Mapping[str, str] = {}
) -> dict[str, str]:
    return {
        aliases.get(key, key.replace('-', '_')): emitter.value(value)
        for key, value in data.items()
    }


def _step_options(step: Mapping[str, Any], emitter: _Emitter) -> dict[str, str]:
    aliases = {
        'if': 'condition',
        'continue-on-error': 'continue_on_error',
        'timeout-minutes': 'timeout_minutes',
        'working-directory': 'working_directory',
    }
    return _kwargs(
        {
            key: value
            for key, value in step.items()
            if key not in {'run', 'uses', 'with'}
        },
        emitter,
        aliases=aliases,
    )


def _accepts_value(annotation: object, value: object) -> bool:
    if annotation in {inspect.Parameter.empty, Any, object}:
        return True
    if isinstance(annotation, str):
        if 'list[' in annotation:
            return isinstance(value, list)
        if 'Mapping[' in annotation:
            return isinstance(value, Mapping)
        if 'bool' in annotation.lower():
            return isinstance(value, bool)
        if 'int' in annotation.lower():
            return isinstance(value, int) and not isinstance(value, bool)
        return isinstance(value, str) or value is None
    if value is None:
        return type(None) in get_args(annotation)
    origin = get_origin(annotation)
    if origin is Union:
        return any(_accepts_value(option, value) for option in get_args(annotation))
    if origin is list:
        return isinstance(value, list)
    if origin is not None:
        try:
            return isinstance(value, origin)
        except TypeError:
            return True
    if annotation is bool:
        return isinstance(value, bool)
    if annotation is int:
        return isinstance(value, int) and not isinstance(value, bool)
    if isinstance(annotation, type):
        return isinstance(value, annotation)
    return True


def _action_step(step: Mapping[str, Any], emitter: _Emitter) -> str:
    uses = str(step['uses'])
    action_name, separator, version = uses.rpartition('@')
    if not separator or action_name.startswith(('.', 'docker://')):
        action_name, version = uses, None
    options = dict(step.get('with') or {})
    common = _step_options(step, emitter)
    registry = ACTION_REGISTRY.get(action_name)
    if registry is not None:
        module, class_name, aliases = registry
        cls = getattr(__import__(module, fromlist=[class_name]), class_name)
        signature = inspect.signature(cls.__new__)
        supported = set(signature.parameters) - {'cls'}
        try:
            type_hints = get_type_hints(cls.__new__)
        except NameError:
            type_hints = {
                key: parameter.annotation
                for key, parameter in signature.parameters.items()
            }
        converted = {
            aliases.get(key, key.replace('-', '_')): emitter.value(value)
            for key, value in options.items()
        }
        raw_converted = {
            aliases.get(key, key.replace('-', '_')): value
            for key, value in options.items()
        }
        candidate = {**converted, **common, 'version': emitter.value(version)}
        values_compatible = all(
            _accepts_value(type_hints.get(key, inspect.Parameter.empty), value)
            for key, value in raw_converted.items()
        )
        if set(candidate) <= supported and values_compatible:
            emitter.imported(module, class_name)
            return emitter.call(class_name, **candidate)

    action = emitter.imported('yamloom', 'action')
    name = common.pop('name', 'None')
    return emitter.call(
        action,
        name,
        emitter.value(action_name),
        ref=emitter.value(version) if version else None,
        with_opts=emitter.value(options) if options else None,
        **common,
    )


def _step(step: Mapping[str, Any], emitter: _Emitter) -> str:
    if 'run' in step:
        script = emitter.imported('yamloom', 'script')
        options = _step_options(step, emitter)
        return emitter.call(script, emitter.value(step['run']), **options)
    if 'uses' in step:
        return _action_step(step, emitter)
    raise ConversionError(f'Step must contain run or uses: {step!r}')


def _permissions(value: Any, emitter: _Emitter) -> str:
    permissions = emitter.imported('yamloom', 'Permissions')
    if value == 'read-all':
        return f'{permissions}.read_all()'
    if value == 'write-all':
        return f'{permissions}.write_all()'
    if value == {}:
        return f'{permissions}.none()'
    if not isinstance(value, Mapping):
        raise ConversionError(f'Unsupported permissions value: {value!r}')
    return emitter.call(permissions, **_kwargs(value, emitter))


def _container(value: Any, emitter: _Emitter) -> str:
    container = emitter.imported('yamloom', 'Container')
    if isinstance(value, str):
        return emitter.call(container, emitter.value(value))
    if not isinstance(value, Mapping) or 'image' not in value:
        raise ConversionError(f'Unsupported container: {value!r}')
    data = dict(value)
    image = emitter.value(data.pop('image'))
    if credentials := data.pop('credentials', None):
        credentials_class = emitter.imported('yamloom', 'Credentials')
        data['credentials'] = emitter.call(
            credentials_class,
            emitter.value(credentials['username']),
            emitter.value(credentials['password']),
        )
    return emitter.call(container, image, **_kwargs(data, emitter))


def _concurrency(value: Any, emitter: _Emitter) -> str:
    concurrency = emitter.imported('yamloom', 'Concurrency')
    if isinstance(value, str):
        return emitter.call(concurrency, emitter.value(value))
    if not isinstance(value, Mapping) or 'group' not in value:
        raise ConversionError(f'Unsupported concurrency value: {value!r}')
    data = dict(value)
    group = emitter.value(data.pop('group'))
    return emitter.call(concurrency, group, **_kwargs(data, emitter))


def _defaults(value: Any, emitter: _Emitter) -> str:
    if not isinstance(value, Mapping) or set(value) != {'run'}:
        raise ConversionError('Only defaults.run is currently supported')
    defaults = emitter.imported('yamloom', 'Defaults')
    run_defaults = emitter.imported('yamloom', 'RunDefaults')
    return emitter.call(
        defaults,
        run_defaults=emitter.call(run_defaults, **_kwargs(value['run'], emitter)),
    )


def _job(value: Mapping[str, Any], emitter: _Emitter) -> str:
    job = emitter.imported('yamloom', 'Job')
    data = dict(value)
    kwargs: dict[str, str] = {}
    if 'steps' in data:
        kwargs['steps'] = (
            '[\n'
            + ''.join(
                f'    {_indent(_step(step, emitter), 4)},\n'
                for step in data.pop('steps')
            )
            + ']'
        )
    if 'runs-on' in data:
        kwargs['runs_on'] = emitter.value(data.pop('runs-on'))
    if 'if' in data:
        kwargs['condition'] = emitter.value(data.pop('if'))
    if 'permissions' in data:
        kwargs['permissions'] = _permissions(data.pop('permissions'), emitter)
        kwargs['use_recommended_permissions'] = 'False'
    if 'strategy' in data:
        raw_strategy = dict(data.pop('strategy'))
        strategy = emitter.imported('yamloom', 'Strategy')
        strategy_kwargs: dict[str, str] = {}
        if 'matrix' in raw_strategy:
            raw_matrix = dict(raw_strategy.pop('matrix'))
            matrix = emitter.imported('yamloom', 'Matrix')
            matrix_kwargs = {
                key: emitter.value(raw_matrix.pop(key))
                for key in ('include', 'exclude')
                if key in raw_matrix
            }
            matrix_args = [f'**{emitter.value(raw_matrix)}'] if raw_matrix else []
            strategy_kwargs['matrix'] = emitter.call(
                matrix, *matrix_args, **matrix_kwargs
            )
        strategy_kwargs.update(
            _kwargs(raw_strategy, emitter, aliases={'fail-fast': 'fast_fail'})
        )
        kwargs['strategy'] = emitter.call(strategy, **strategy_kwargs)
    if 'container' in data:
        kwargs['container'] = _container(data.pop('container'), emitter)
    if 'services' in data:
        kwargs['services'] = emitter.mapping(
            {
                name: _container(container, emitter)
                for name, container in data.pop('services').items()
            }
        )
    if 'environment' in data:
        environment = emitter.imported('yamloom', 'Environment')
        raw_environment = data.pop('environment')
        if isinstance(raw_environment, Mapping):
            raw_environment = dict(raw_environment)
            kwargs['environment'] = emitter.call(
                environment,
                emitter.value(raw_environment.pop('name')),
                **_kwargs(raw_environment, emitter),
            )
        else:
            kwargs['environment'] = emitter.call(
                environment, emitter.value(raw_environment)
            )
    if 'concurrency' in data:
        kwargs['concurrency'] = _concurrency(data.pop('concurrency'), emitter)
    if 'defaults' in data:
        kwargs['defaults'] = _defaults(data.pop('defaults'), emitter)
    if 'secrets' in data:
        secrets = data.pop('secrets')
        job_secrets = emitter.imported('yamloom', 'JobSecrets')
        kwargs['secrets'] = (
            f'{job_secrets}.inherit()'
            if secrets == 'inherit'
            else emitter.call(job_secrets, emitter.value(secrets))
        )
    aliases = {
        'continue-on-error': 'continue_on_error',
        'timeout-minutes': 'timeout_minutes',
        'with': 'with_opts',
    }
    if 'needs' in data and isinstance(data['needs'], str):
        data['needs'] = [data['needs']]
    kwargs.update(_kwargs(data, emitter, aliases=aliases))
    return emitter.call(job, **kwargs)


EVENT_CLASSES = {
    'branch_protection_rule': 'BranchProtectionRuleEvent',
    'check_run': 'CheckRunEvent',
    'check_suite': 'CheckSuiteEvent',
    'discussion': 'DiscussionEvent',
    'discussion_comment': 'DiscussionCommentEvent',
    'image_version': 'ImageVersionEvent',
    'issue_comment': 'IssueCommentEvent',
    'issues': 'IssuesEvent',
    'label': 'LabelEvent',
    'merge_group': 'MergeGroupEvent',
    'milestone': 'MilestoneEvent',
    'pull_request': 'PullRequestEvent',
    'pull_request_review': 'PullRequestReviewEvent',
    'pull_request_review_comment': 'PullRequestReviewCommentEvent',
    'pull_request_target': 'PullRequestEvent',
    'push': 'PushEvent',
    'registry_package': 'RegistryPackageEvent',
    'release': 'ReleaseEvent',
    'watch': 'WatchEvent',
    'workflow_run': 'WorkflowRunEvent',
}
SIMPLE_EVENTS = {
    'create',
    'delete',
    'deployment',
    'deployment_status',
    'fork',
    'gollum',
    'page_build',
    'public',
    'status',
}


def _typed_input(value: Mapping[str, Any], emitter: _Emitter, class_name: str) -> str:
    cls = emitter.imported('yamloom', class_name)
    data = dict(value)
    input_type = data.pop('type', 'string')
    if input_type == 'choice':
        options = emitter.value(data.pop('options'))
        return emitter.call(f'{cls}.choice', options, **_kwargs(data, emitter))
    return emitter.call(f'{cls}.{input_type}', **_kwargs(data, emitter))


def _cron_field(token: str, class_name: str, emitter: _Emitter) -> str | None:
    if token == '*':
        return None
    cls = emitter.imported('yamloom', class_name)
    if token.startswith('*/') and token[2:].isdigit():
        return emitter.call(f'{cls}.every', token[2:])
    if '-' in token:
        start, separator, end = token.partition('-')
        if separator and start.isdigit() and end.isdigit():
            return emitter.call(f'{cls}.between', start, end)
    values = token.split(',')
    if all(value.isdigit() for value in values):
        parsed: int | list[int] = (
            int(values[0]) if len(values) == 1 else [int(value) for value in values]
        )
        return emitter.call(cls, emitter.value(parsed))
    raise ConversionError(f'Cron field is not representable by Yamloom: {token!r}')


def _schedule(value: Any, emitter: _Emitter) -> str:
    if not isinstance(value, list):
        raise ConversionError('schedule must be a list of cron mappings')
    cron_class = emitter.imported('yamloom', 'Cron')
    crons: list[str] = []
    field_classes = ('Minute', 'Hour', 'Day', 'Month', 'DayOfWeek')
    field_names = ('minute', 'hour', 'day', 'month', 'day_of_week')
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {'cron'}:
            raise ConversionError(f'Unsupported schedule item: {item!r}')
        parts = str(item['cron']).split()
        if len(parts) != 5:
            raise ConversionError(
                f'Cron expression must contain five fields: {item["cron"]!r}'
            )
        kwargs = {
            name: expression
            for name, expression in zip(
                field_names,
                (
                    _cron_field(token, class_name, emitter)
                    for token, class_name in zip(parts, field_classes)
                ),
            )
            if expression is not None
        }
        crons.append(emitter.call(cron_class, **kwargs))
    schedule = emitter.imported('yamloom', 'ScheduleEvent')
    return emitter.call(
        schedule,
        crons='[\n' + ''.join(f'    {_indent(cron, 4)},\n' for cron in crons) + ']',
    )


def _events(value: Any, emitter: _Emitter) -> str:
    events = emitter.imported('yamloom', 'Events')
    if isinstance(value, str):
        value = {value: None}
    elif isinstance(value, list):
        value = {name: None for name in value}
    if not isinstance(value, Mapping):
        raise ConversionError(f'Unsupported on value: {value!r}')
    kwargs: dict[str, str] = {}
    for raw_name, configuration in value.items():
        name = raw_name.replace('-', '_')
        if name in SIMPLE_EVENTS:
            kwargs[name] = 'True'
        elif name in EVENT_CLASSES:
            cls = emitter.imported('yamloom', EVENT_CLASSES[name])
            config = dict(configuration or {})
            types = config.pop('types', [])
            event_kwargs = _kwargs(config, emitter)
            event_kwargs.update(
                {event_type.replace('-', '_'): 'True' for event_type in types}
            )
            kwargs[name] = emitter.call(cls, **event_kwargs)
        elif name == 'repository_dispatch':
            cls = emitter.imported('yamloom', 'RepositoryDispatchEvent')
            config = dict(configuration or {})
            if set(config) - {'types'}:
                raise ConversionError(
                    f'Unsupported repository_dispatch keys: {list(config)}'
                )
            kwargs[name] = emitter.call(
                cls,
                types=emitter.value(config['types']) if 'types' in config else None,
            )
        elif name == 'workflow_dispatch':
            cls = emitter.imported('yamloom', 'WorkflowDispatchEvent')
            config = dict(configuration or {})
            inputs = config.pop('inputs', None)
            if config:
                raise ConversionError(
                    f'Unsupported workflow_dispatch keys: {list(config)}'
                )
            kwargs[name] = emitter.call(
                cls,
                inputs=emitter.mapping(
                    {
                        key: _typed_input(item, emitter, 'WorkflowDispatchInput')
                        for key, item in inputs.items()
                    }
                )
                if inputs
                else None,
            )
        elif name == 'workflow_call':
            cls = emitter.imported('yamloom', 'WorkflowCallEvent')
            config = dict(configuration or {})
            call_kwargs: dict[str, str] = {}
            if inputs := config.pop('inputs', None):
                call_kwargs['inputs'] = emitter.mapping(
                    {
                        key: _typed_input(item, emitter, 'WorkflowInput')
                        for key, item in inputs.items()
                    }
                )
            if secrets := config.pop('secrets', None):
                secret_cls = emitter.imported('yamloom', 'WorkflowSecret')
                call_kwargs['secrets'] = emitter.mapping(
                    {
                        key: emitter.call(secret_cls, **_kwargs(item, emitter))
                        for key, item in secrets.items()
                    }
                )
            if outputs := config.pop('outputs', None):
                output_cls = emitter.imported('yamloom', 'WorkflowOutput')
                call_kwargs['outputs'] = emitter.mapping(
                    {
                        key: emitter.call(
                            output_cls,
                            emitter.value(item['value']),
                            description=emitter.value(item['description'])
                            if 'description' in item
                            else None,
                        )
                        for key, item in outputs.items()
                    }
                )
            if config:
                raise ConversionError(f'Unsupported workflow_call keys: {list(config)}')
            kwargs[name] = emitter.call(cls, **call_kwargs)
        elif name == 'schedule':
            kwargs[name] = _schedule(configuration, emitter)
        else:
            raise ConversionError(f'Unsupported event: {raw_name}')
    return emitter.call(events, **kwargs)


def convert_workflow(source: str, *, workflow_name: str = 'workflow.yml') -> str:
    """Convert one GitHub workflow YAML document to executable Yamloom Python."""
    parsed = json.loads(_parse_yaml(source))
    if not isinstance(parsed, dict):
        raise ConversionError('Workflow document must be a mapping')
    if 'on' not in parsed or 'jobs' not in parsed:
        raise ConversionError("Workflow must contain 'on' and 'jobs'")

    emitter = _Emitter()
    workflow = emitter.imported('yamloom', 'Workflow')
    sync = emitter.imported('yamloom', 'sync')
    data = dict(parsed)
    jobs = emitter.mapping(
        {name: _job(job, emitter) for name, job in data.pop('jobs').items()}
    )
    kwargs: dict[str, str] = {'jobs': jobs, 'on': _events(data.pop('on'), emitter)}
    if 'permissions' in data:
        kwargs['permissions'] = _permissions(data.pop('permissions'), emitter)
    if 'concurrency' in data:
        kwargs['concurrency'] = _concurrency(data.pop('concurrency'), emitter)
    if 'defaults' in data:
        kwargs['defaults'] = _defaults(data.pop('defaults'), emitter)
    aliases = {'run-name': 'run_name'}
    kwargs.update(_kwargs(data, emitter, aliases=aliases))
    workflow_expression = emitter.call(workflow, **kwargs)

    imports = '\n'.join(
        f'from {module} import {", ".join(sorted(names))}'
        for module, names in sorted(emitter.imports.items())
    )
    mapping = emitter.mapping({workflow_name: workflow_expression})
    return f'{imports}\n\n\n{sync}({mapping})\n'


__all__ = ['ConversionError', 'convert_workflow']
