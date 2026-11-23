"""Core logic: read a members CSV file and sort / format the records.

Nothing in this module prints or exits, so it is safe to use inside other
applications. See :mod:`members_reader.cli` for the command-line front end.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Union

__all__ = [
    "Member",
    "MembersReaderError",
    "MissingColumnsError",
    "REQUIRED_COLUMNS",
    "format_name",
    "read_members",
    "sort_members",
]

#: Columns that must be present in the CSV header.
REQUIRED_COLUMNS = ("first_name", "last_name")

PathLike = Union[str, "Path"]


class MembersReaderError(Exception):
    """Base class for every error raised by this library."""


class MissingColumnsError(MembersReaderError, ValueError):
    """The CSV header does not contain all of :data:`REQUIRED_COLUMNS`.

    Attributes:
        missing: Names of the required columns that were not found.
    """

    def __init__(self, missing: Iterable[str], path: PathLike) -> None:
        self.missing = tuple(missing)
        super().__init__(
            f"{path}: missing required column(s): {', '.join(self.missing)}"
        )


@dataclass(frozen=True)
class Member:
    """A single row of the members file.

    Only ``first_name`` and ``last_name`` are required. Other columns are
    ``None`` when the CSV does not contain them.
    """

    first_name: str
    last_name: str
    id: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    ip_address: Optional[str] = None

    @property
    def full_name(self) -> str:
        """``"<first_name> <last_name>"``."""
        return format_name(self)


def format_name(member: Member) -> str:
    """Return the member's name as ``"First Last"``."""
    return f"{member.first_name} {member.last_name}"


def read_members(path: PathLike, encoding: str = "utf-8") -> List[Member]:
    """Read a members CSV file.

    Args:
        path: Location of the CSV file. It must have a header row containing
            at least ``first_name`` and ``last_name``. The optional columns
            ``id``, ``email``, ``gender`` and ``ip_address`` are read if present.
        encoding: Text encoding of the file.

    Returns:
        The members, in file order.

    Raises:
        FileNotFoundError: ``path`` does not exist.
        MissingColumnsError: a required column is missing from the header
            (this includes an empty file).
    """
    with open(path, newline="", encoding=encoding) as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in header]
        if missing:
            raise MissingColumnsError(missing, path)

        return [
            Member(
                first_name=row["first_name"],
                last_name=row["last_name"],
                id=row.get("id"),
                email=row.get("email"),
                gender=row.get("gender"),
                ip_address=row.get("ip_address"),
            )
            for row in reader
        ]


def sort_members(members: Iterable[Member]) -> List[Member]:
    """Return members sorted by last name, then first name (case-insensitive).

    The input is not modified.
    """
    return sorted(
        members, key=lambda m: (m.last_name.lower(), m.first_name.lower())
    )
