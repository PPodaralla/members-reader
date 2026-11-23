# members-reader

[![CI](https://github.com/PPodaralla/members-reader/actions/workflows/ci.yml/badge.svg)](https://github.com/PPodaralla/members-reader/actions/workflows/ci.yml)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

A small, dependency-free Python library and command-line tool that reads a
members CSV file and lists the members' names sorted by last name.

## Installation

```bash
pip install git+https://github.com/PPodaralla/members-reader
```

Or, from a local clone (editable, with test tools):

```bash
git clone https://github.com/PPodaralla/members-reader
cd members-reader
pip install -e ".[dev]"
```

Requires Python 3.9 or newer. There are no runtime dependencies.

## Quickstart

### Command line

```bash
members-reader examples/sample_members.csv
```

```
Marleen Abramovici
Crystie Achrameev
Orville Ainscow
...
```

You can also run it as a module: `python -m members_reader examples/sample_members.csv`.

| Option | Description |
| --- | --- |
| `PATH` | CSV file to read (default: `members.csv`) |
| `--unsorted` | Keep file order instead of sorting by last name |
| `--encoding ENC` | File encoding (default: `utf-8`) |
| `--version` | Show the version |

Exit code is `0` on success and `1` on error (message printed to stderr).

### Python API

```python
from members_reader import read_members, sort_members

members = sort_members(read_members("examples/sample_members.csv"))
print(members[0].full_name)
print(members[0].email)
```

```pycon
>>> from members_reader import read_members, sort_members
>>> members = sort_members(read_members("examples/sample_members.csv"))
>>> members[0].full_name
'Marleen Abramovici'

```

## CSV format

The file needs a header row. `first_name` and `last_name` are **required**;
the other columns are optional and become `None` on the `Member` if absent.

```csv
id,first_name,last_name,email,gender,ip_address
1,Gilly,Windless,gwindless0@nhs.uk,Female,210.106.96.230
```

See [`examples/sample_members.csv`](examples/sample_members.csv). The sample
data is fictional mock data.

## API reference

Everything below is importable from `members_reader`.

### `read_members(path, encoding="utf-8") -> list[Member]`

Reads the file and returns the members in file order.

Raises `FileNotFoundError` if `path` doesn't exist, and `MissingColumnsError`
if a required column is missing (including an empty file).

### `sort_members(members) -> list[Member]`

Returns a new list sorted by last name, then first name, ignoring case. The
input is not modified.

### `format_name(member) -> str`

Returns `"First Last"`. Also available as `member.full_name`.

### `Member`

Frozen dataclass with fields `first_name`, `last_name`, `id`, `email`,
`gender`, `ip_address` (all but the first two default to `None`) and a
`full_name` property.

### Exceptions

- `MembersReaderError`: base class for every error raised by this library.
- `MissingColumnsError(MembersReaderError, ValueError)`: has a `.missing`
  tuple with the absent column names.

The package ships type hints (`py.typed`), so editors and `mypy` understand
the API.

## Development

```bash
pip install -e ".[dev]"
pytest              # tests and README/docstring examples
ruff check .        # lint
```

CI runs the tests on Python 3.9 to 3.13 for every push and pull request.

## Contributing

Issues and pull requests are welcome. Please add a test for any change in
behavior and note it in [CHANGELOG.md](CHANGELOG.md).

## License

[MIT](LICENSE)
