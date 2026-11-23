"""Command-line interface: ``members-reader [PATH]``."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import __version__
from .core import MembersReaderError, format_name, read_members, sort_members


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="members-reader",
        description="Print member names from a CSV file, sorted by last name.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="members.csv",
        help="CSV file with first_name and last_name columns (default: %(default)s)",
    )
    parser.add_argument(
        "--unsorted",
        action="store_true",
        help="keep the order of the file instead of sorting by last name",
    )
    parser.add_argument(
        "--encoding", default="utf-8", help="file encoding (default: %(default)s)"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Run the CLI. Returns the process exit code (0 ok, 1 error)."""
    args = build_parser().parse_args(argv)
    try:
        members = read_members(args.path, encoding=args.encoding)
    except FileNotFoundError:
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 1
    except (MembersReaderError, UnicodeDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if not args.unsorted:
        members = sort_members(members)
    for member in members:
        print(format_name(member))
    return 0


if __name__ == "__main__":
    sys.exit(main())
