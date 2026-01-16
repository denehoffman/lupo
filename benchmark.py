from lupo import Events, Job, PullRequestEvent, PushEvent, Workflow, WorkflowDispatchEvent, action, script
from lupo.actions import checkout
from lupo.expressions import context
from lupo.toolchains import install_rust_tool, setup_rust

print(
    Workflow(
        name='CodSpeed Benchmarks',
        jobs={
            'benchmarks': Job(
                [
                    checkout(),
                    script('Install OpenMPI', 'sudo apt install -y openmpi-bin openmpi-doc libopenmpi-dev'),
                    setup_rust(toolchain='stable'),
                    install_rust_tool(tool=['cargo-codspeed']),
                    script('Build benchmark targets', 'cargo codspeed build --profile dist-release'),
                    action(
                        name='Run benchmarks',
                        action='CodSpeedHQ/action',
                        ref='v4',
                        with_opts={
                            'mode': 'simulation',
                            'run': 'cargo codspeed run',
                            'token': context.secrets['CODSPEED_TOKEN'],
                        },
                    ),
                ]
            )
        },
        on=Events(
            push=PushEvent(branches=['main']),
            pull_request=PullRequestEvent(),
            workflow_dispatch=WorkflowDispatchEvent(),
        ),
    )
)
