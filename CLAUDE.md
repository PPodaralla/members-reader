# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`members-reader` is a dependency-free, pip-installable Python package (src layout, setuptools via `pyproject.toml`) that reads a members CSV and lists names sorted by last name. It targets Python >=3.9, so avoid 3.10+ only syntax (`X | Y` types, `match`, `slots=True`); use `from __future__ import annotations` and `typing.List/Optional`.

## Commands

```
pip install -e ".[dev]"                 # install with pytest + ruff
pytest                                  # tests + doctests (docstrings and README.md)
pytest tests/test_core.py::test_name    # single test
ruff check .                            # lint
members-reader examples/sample_members.csv   # run the CLI (or python -m members_reader)
```

## Architecture

- `src/members_reader/core.py`: all logic (`read_members`, `sort_members`, `Member`, exceptions). It must never print or call `sys.exit`, since other applications import it.
- `src/members_reader/cli.py`: thin argparse wrapper that handles output and exit codes. `__main__.py` enables `python -m members_reader`.
- `__init__.py` defines the public API via `__all__`; new public names must be re-exported there and documented in `README.md`.
- Only `first_name` and `last_name` CSV columns are required; other columns map to optional `Member` fields.

## Notes

- `pytest` runs with `--doctest-modules --doctest-glob=README.md`, so code examples in docstrings and the README are executed and must stay correct.
- `/members.csv` (1000 rows of local data) is gitignored; only `examples/sample_members.csv` is published.
