"""members-reader: read a members CSV file and list names sorted by last name.

Example:
    >>> from members_reader import read_members, sort_members
    >>> for m in sort_members(read_members("examples/sample_members.csv"))[:2]:
    ...     print(m.full_name)
    Marleen Abramovici
    Crystie Achrameev
"""

from importlib.metadata import PackageNotFoundError, version

from .core import (
    REQUIRED_COLUMNS,
    Member,
    MembersReaderError,
    MissingColumnsError,
    format_name,
    read_members,
    sort_members,
)

try:
    __version__ = version("members-reader")
except PackageNotFoundError:  # running from a source tree without installing
    __version__ = "0.0.0"

__all__ = [
    "Member",
    "MembersReaderError",
    "MissingColumnsError",
    "REQUIRED_COLUMNS",
    "__version__",
    "format_name",
    "read_members",
    "sort_members",
]
