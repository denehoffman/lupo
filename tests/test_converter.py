import json
import runpy
from pathlib import Path

from yamloom._yamloom import _parse_yaml
from yamloom.converter import convert_workflow


SOURCE = """
name: Checks
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * 1-5'
  repository_dispatch:
    types: [rebuild]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    environment: test
    strategy:
      fail-fast: false
      matrix:
        python-version: ['3.12', '3.13']
    steps:
      - uses: actions/checkout@v6
      - name: New checkout option
        uses: actions/checkout@v6
        with:
          future-input: yes
      - uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          components: clippy
      - name: Test
        run: pytest -q
        env:
          TOKEN: ${{ secrets.TOKEN }}
"""


def normalized(source: str) -> dict:
    return json.loads(_parse_yaml(source))


def test_converter_uses_native_action_and_generic_fallback(
    tmp_path: Path, monkeypatch
) -> None:
    generated = convert_workflow(SOURCE, workflow_name='checks.yml')
    assert 'Checkout(version=' in generated
    assert 'action(\n' in generated
    assert "'actions/checkout'" in generated
    assert "'future-input': 'yes'" in generated
    assert "'components': 'clippy'" in generated

    generator = tmp_path / '.yamloom.py'
    generator.write_text(generated)
    monkeypatch.chdir(tmp_path)
    runpy.run_path(str(generator), run_name='__main__')
    rendered = (tmp_path / '.github/workflows/checks.yml').read_text()
    rendered = rendered.split('\n', 1)[1]
    actual = normalized(rendered)
    expected = normalized(SOURCE)
    # Yamloom normalizes one-element forms and generated permissions, while preserving meaning.
    assert actual['name'] == expected['name']
    assert actual['on'] == expected['on']
    assert actual['jobs']['test']['strategy'] == expected['jobs']['test']['strategy']
    actual_steps = actual['jobs']['test']['steps']
    expected_steps = expected['jobs']['test']['steps']
    assert [step.get('uses') for step in actual_steps] == [
        step.get('uses') for step in expected_steps
    ]
    assert [step.get('run') for step in actual_steps] == [
        step.get('run') for step in expected_steps
    ]
    assert actual_steps[1]['with'] == expected_steps[1]['with']
    assert actual_steps[2]['with'] == expected_steps[2]['with']
