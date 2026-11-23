"""Minimal example of using members-reader as a library.

Run from the project root:  python examples/basic_usage.py
"""

from pathlib import Path

from members_reader import MembersReaderError, read_members, sort_members

path = Path(__file__).with_name("sample_members.csv")

try:
    members = sort_members(read_members(path))
except (FileNotFoundError, MembersReaderError) as exc:
    raise SystemExit(f"Could not load members: {exc}") from exc

for m in members[:5]:
    print(f"{m.full_name} <{m.email}>")
