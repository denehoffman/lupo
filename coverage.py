from lupo import (
    Events,
    Job,
    PullRequestEvent,
    PushEvent,
    Workflow,
    WorkflowCallEvent,
    WorkflowDispatchEvent,
    WorkflowSecret,
    action,
    script,
)
from lupo.actions import checkout, download_artifact, upload_artifact
from lupo.toolchains import install_rust_tool, setup_rust, setup_uv

coverage_rust = Job(
    [
        checkout(),
        script('Install MPICH', 'sudo apt install -y clang mpich libmpich-dev'),
        setup_rust(toolchain='nightly'),
        install_rust_tool(tool=['just', 'cargo-llvm-cov']),
        script('Generate Rust code coverage', 'just coverage-rust'),
        upload_artifact(path='coverage-rust.lcov', artifact_name='coverage-rust'),
    ],
    runs_on='ubuntu-latest',
    env={'CARGO_TERM_COLOR': 'always'},
)

coverage_python = Job(
    [
        checkout(),
        setup_uv(),
        setup_rust(toolchain='stable'),
        install_rust_tool(tool=['just']),
        script('Generate Python code coverage', 'just coverage-python'),
        upload_artifact(path='coverage-python.xml', artifact_name='coverage-python'),
    ],
    runs_on='ubuntu-latest',
)

upload_coverage = Job(
    [
        checkout(),
        download_artifact(merge_multiple=True),
        action(
            'Upload coverage reports to Codecov',
            'codecov/codecov-action',
            ref='v5',
            with_opts={
                'token': '${{ secrets.CODECOV_TOKEN }}',
                'files': 'coverage-rust.lcov,coverage-python.xml',
                'fail_ci_if_error': True,
                'verbose': True,
                'root_dir': '${{ github.workspace }}',
            },
        ),
    ],
    runs_on='ubuntu-latest',
    needs=['coverage-rust', 'coverage-python'],
)

workflow = Workflow(
    name='Coverage',
    jobs={'coverage-rust': coverage_rust, 'coverage-python': coverage_python, 'upload-coverage': upload_coverage},
    on=Events(
        pull_request=PullRequestEvent(paths=['**.rs', '**.py', '.github/workflows/coverage.yml']),
        push=PushEvent(branches=['main'], paths=['**.rs', '**.py', '.github/workflows/coverage.yml']),
        workflow_call=WorkflowCallEvent(secrets={'codecov_token': WorkflowSecret(required=True)}),
        workflow_dispatch=WorkflowDispatchEvent(),
    ),
)

print(workflow)
