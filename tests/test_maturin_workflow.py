from yamloom import Events, Workflow, WorkflowDispatchEvent
from yamloom.workflows.maturin import (
    MaturinBuildSuite,
    MaturinPlatform,
    MaturinTarget,
)


def test_profiles_and_target_exclusions() -> None:
    platform = MaturinPlatform(
        'custom',
        'Custom',
        (MaturinTarget('ubuntu-latest', 'x86_64', skip_python_versions=('pypy3.11',)),),
    )
    suite = MaturinBuildSuite(
        python_profile='all', minimum_python='3.10', platforms=(platform,), sdist=False
    )
    assert suite.resolved_python_versions == (
        '3.10',
        '3.11',
        '3.12',
        '3.13',
        '3.14',
        '3.14t',
        'pypy3.11',
    )
    workflow = Workflow(
        on=Events(workflow_dispatch=WorkflowDispatchEvent()), jobs=suite.jobs()
    )
    rendered = str(workflow)
    assert 'pypy3.11' not in rendered
    assert 'Build wheels' in rendered


def test_callbacks_and_sdist() -> None:
    platform = MaturinPlatform(
        'linux', 'Linux', (MaturinTarget('ubuntu-22.04', 'x86_64'),), '2_28'
    )
    suite = MaturinBuildSuite(
        manifest_path='python/Cargo.toml',
        platforms=(platform,),
        setup_steps=lambda _platform: (),
        maturin_options=lambda _platform: {
            'before_script_linux': 'dnf install -y openmpi'
        },
    )
    workflow = Workflow(
        on=Events(workflow_dispatch=WorkflowDispatchEvent()), jobs=suite.jobs()
    )
    rendered = str(workflow)
    assert '--manifest-path python/Cargo.toml' in rendered
    assert 'before-script-linux' in rendered
    assert 'sdist:' in rendered
