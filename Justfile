default:
    just --list

develop:
    CARGO_INCREMENTAL=true maturin develop --uv

check:
    cargo clippy
    ty check
    ruff check
    ruff format

fix:
    cargo clippy --fix
    ruff check --fix
